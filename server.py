from flask import (Flask, render_template, redirect, request)
from model import connect_to_db, db
import crud

app = Flask(__name__)


@app.route('/')
def homepage():
    
    return render_template("homepage.html")

@app.route('/login')
def login():

    return render_template('homepage.html')

@app.route('/register', methods=["POST"])
def register():

    username = request.form.get("username")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    crud.create_user(email, username, password, name)
    return render_template('homepage.html', username=username, name=name,
                           email=email, password=password)


@app.route('/closet')
def show_closet():

    return render_template('closet.html')

@app.route('/favorites')
def show_favorites():

    return render_template('/favorites.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)