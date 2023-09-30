from collections import defaultdict, OrderedDict
from flask import Flask, render_template, redirect, request, session, jsonify
from model import Articles, connect_to_db, UserFavorites

import crud
import os
import cloudinary
import random

CLOUDINARY_KEY = "672335896611927"
CLOUDINARY_SECRET = "wijc7z2ohAnkXMwj6yZY8FbpNv0"
CLOUD_NAME = "drf73nnrz"

app = Flask(__name__)
app.secret_key="DEV"

cloudinary.config(
    cloud_name = CLOUD_NAME,
    api_key = CLOUDINARY_KEY,
    api_secret = CLOUDINARY_SECRET,
    secure = True

)
import cloudinary.uploader
import cloudinary.api


ARTICLE_ORDER = {
    'hat': 0, 
    'glasses': 1,
    'bag': 2, 
    'jacket': 3, 
    'sweater': 4, 
    'dress': 5, 
    'shirt': 6,
    'pants': 7, 
    'skirt': 8, 
    'shoes': 9,
}


@app.route('/')
def homepage():
    if "user" in session:
        return redirect("/closet")
    else:
        return render_template("homepage.html")

@app.route('/login')
def login():

    username = request.args.get("username")
    password = request.args.get("password")

    user = crud.check_user(username) 
    
    if user:
        if password == user.password:
            session["user"] = {
                'id': user.user_id,
                'name': user.name
            }
            return redirect("/closet")
        else:
            return redirect('/login')
    else:
        print("Username or password doesn't match. Try again")
    

@app.route('/register', methods=["POST"])
def register():

    username = request.form.get("username")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    username_exists = crud.check_user(username)
    if username == username_exists.username:
        print("Username already exists, please try a different one.")
        return redirect('/register')
    else:
        crud.create_user(email=email, username=username, password=password, name=name)
        return render_template('closet.html', username=username)

@app.route('/upload-file', methods=["POST"])
def upload_file():
    file = request.files['additem'] 
    result = cloudinary.uploader.upload(file,
                        api_key=CLOUDINARY_KEY,
                        api_secret=CLOUDINARY_SECRET,
                        cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    type = request.form.get("type")
    color_primary = request.form.get("color_primary")
    color_sec = request.form.get("color_sec")
    pattern = request.form.get("pattern")
    occasion = request.form.get("occasion")
    season = request.form.get("season")
    
    user_in_session()
    
    user = session["user"]    
    crud.add_articles(user_id=user["id"], type=type, resource_url=img_url,
                       color_primary=color_primary, color_sec=color_sec,
                       pattern=pattern, occasion=occasion,
                       season=season)
    
    return redirect('/closet')

@app.route('/closet')
def view_closet():
    user_in_session()
    
    user = session["user"] # = {'id': 1, 'name': 'Luisa'}
    all_clothing_items = Articles.query.filter(Articles.user_id==user['id']).all()

    return render_template('closet.html', article_items=all_clothing_items, name=user["name"])

@app.route('/create-outfit', methods=["GET", "POST"])
def build_an_outfit():
    if request.method == "GET":
        return render_template('create-outfit.html')

    user_in_session()
    
    return redirect('/create-outfit')


@app.route('/view_outfit', methods=['POST'])
def show_outfit():
    user_in_session()

    if request.method == "GET":
        return render_template('view_outfit.html')


    user_occasion = request.json.get("occasion")
    current_season = request.json.get("season")
    color_option = request.json.get("color")
    title = request.json.get("title")
    user_wants_hat = request.json.get("wantHat")
    user_wants_glasses = request.json.get("wantGlasses")
    user_wants_bags = request.json.get("wantBag")
    type_of_outfit = request.json.get("typeOfOutfit")

    # add to accessories_to_exclude any accessory types the user doesn't want
    accessories_to_exclude = []


    if user_wants_hat == False:
        accessories_to_exclude.append("hat")
    if user_wants_bags == False:
        accessories_to_exclude.append("bag")
    if user_wants_glasses == False:
        accessories_to_exclude.append("glasses")

    user = session["user"]
    
    all_clothing_items = Articles.query.filter(
        Articles.user_id==user['id'],
        Articles.occasion==user_occasion,
        Articles.season==current_season,
        ~Articles.type.in_(accessories_to_exclude),
    ).all()


    outfit = crud.create_outfit(title=title, user_id=user['id'])

    articles = {}

    for item in all_clothing_items:
        if item.type not in articles:
            articles[item.type] = []
        
        articles[item.type].append(item)
        

    shirts = articles.get("shirt")
    pants = articles.get("pants")
    skirts = articles.get("skirt")
    dresses = articles.get("dress")
    sweaters = articles.get("sweater")
    jackets = articles.get("jacket")
    shoes = articles.get("shoes")
    hats = articles.get("hat")
    bags = articles.get("bag")
    glasses = articles.get("glasses")

    result = defaultdict(dict)

    if user_wants_hat == True:

        if hats:
            hat = random.choice(hats)
            crud.outfit_articles(hat.article_id, outfit.outfit_id)
            result['hat']['url'] = hat.resource_url
            result['hat']['id'] = hat.article_id

    if user_wants_bags == True:

        if bags:
            bag = random.choice(bags)
            crud.outfit_articles(bag.article_id, outfit.outfit_id)
            result['bag']['url'] = bag.resource_url
            result['bag']['id'] = bag.article_id

    if user_wants_glasses == True:
        
        if glasses:
            glass = random.choice(glasses)
            crud.outfit_articles(glass.article_id, outfit.outfit_id)
            result['glasses']['url'] = glass.resource_url
            result['glasses']['id'] = glass.article_id

    if type_of_outfit == "shirt-pants": 
        if shirts:
            shirt = random.choice(shirts)
            crud.outfit_articles(shirt.article_id, outfit.outfit_id)
            result['shirt']['url'] = shirt.resource_url
            result['shirt']['id'] = shirt.article_id
            if current_season=="winter" or current_season == "fall":
                sweater = random.choice(sweaters)
                jacket = random.choice(jackets)
                crud.outfit_articles(sweater.article_id, outfit.outfit_id)
                crud.outfit_articles(jacket.article_id, outfit.outfit_id)
                result['jacket']['url'] = jacket.resource_url
                result['jacket']['id'] = jacket.article_id
                result['sweater']['url'] = sweater.resource_url
                result['sweater']['id'] = sweater.article_id
                
        if pants:
            pant = random.choice(pants)
            crud.outfit_articles(pant.article_id, outfit.outfit_id)
            result['pants']['url'] = pant.resource_url
            result['pants']['id'] = pant.article_id
    elif type_of_outfit == "shirt-skirt":
        if shirts:
            shirt = random.choice(shirts)
            crud.outfit_articles(shirt.article_id, outfit.outfit_id)
            result['shirt']['url'] = shirt.resource_url
            result['shirt']['id'] = shirt.article_id
            if current_season=="winter" or current_season == "fall":
                sweater = random.choice(sweaters)
                sweater = sweater.resource_url
                crud.outfit_articles(sweater.article_id, outfit.outfit_id)
                crud.outfit_articles(jacket.article_id, outfit.outfit_id)
                jacket = random.choice(jackets)
                result['jacket']['url'] = jacket.resource_url
                result['jacket']['id'] = jacket.article_id
        if skirts:
            skirt = random.choice(skirt)
            crud.outfit_articles(skirt.article_id, outfit.outfit_id)
            result['skirt']['url'] = skirt.resource_url
            result['skirt']['id'] = skirt.article_id
    else: 
        if dresses:
            dress = random.choice(dresses)
            crud.outfit_articles(dress.article_id, outfit.outfit_id)
            result['dress']['url'] = dress.resource_url
            result['dress']['id'] = dress.article_id
    
    if shoes:
        shoe = random.choice(shoes)
        crud.outfit_articles(shoe.article_id, outfit.outfit_id)
        result['shoes']['url'] = shoe.resource_url
        result['shoes']['id'] = shoe.article_id
        
    return jsonify(sorted(result.items(), key=lambda x: ARTICLE_ORDER.get(x[0], 0)))

@app.route('/favorite-elements', methods=["POST"])
def get_elements():
    items = [request.json.get("0", None)]
    article = crud.return_outfit_article(int(items[0]))

    outfit_id = (article.outfit_articles[-1].outfit_id)

    crud.check_favorite(outfit_id=outfit_id, user_id=session['user']['id'])

    crud.user_favorite(outfit_id=outfit_id, user_id=session['user']['id'])

    return jsonify("success")



@app.route('/favorites', methods=["GET","POST"])
def show_favorites():
    query_favorites = UserFavorites.query.filter(UserFavorites.user_id==session['user']['id']).all()

    fav_dict = {}

    for item in query_favorites:
        fav_dict[(item.outfit_id, item.outfits.title)] = item.outfits.outfit_articles

        #     article.articles
    
    return render_template('favorites.html', fav_dict=fav_dict)



def user_in_session():
    if "user" not in session:
        return redirect("/")
    

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)