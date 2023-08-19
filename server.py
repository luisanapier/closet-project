from flask import (Flask, render_template, redirect, request)
from model import connect_to_db, db
import crud

app = Flask(__name__)


@app.route('/')
def homepage():
    
    return render_template("homepage.html")

@app.route('/login')
def login():

    username = request.args.get("username")
    password = request.args.get("password")

    user = crud.check_user(username) 
    if user:
        if password == user.password:
            return render_template('closet.html', username=username)
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

    
@app.route('/closet')
def show_closet():



    crud.add_articles(type=type, resource_url=resource_url,
                       color_primary=color_primary, color_sec=color_sec,
                       pattern=pattern, occasion=occasion,
                       season=season, user_id=user_id)
    crud.create_outfit(title=title, user_id=user_id)
    crud.outfit_articles(article_id=article_id, outfit_id=outfit_id)
    return render_template('closet.html')

@app.route('/favorites')
def show_favorites():
    
    crud.user_favorite(outfit_id=outfit_id, user_id=user_id)
    return render_template('/favorites.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)