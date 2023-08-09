from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    """A User."""

    __tablename__ = "users" 

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
 
    articles = db.Relationship("Articles", back_populates="user")
    outfits = db.Relationship("Outfit", back_populates="user")

    def __repr__(self):
        return f'User User: {self.user_id} username: {self.username}'

class Articles(db.Model):
    """Articles of clothing"""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    type = db.Column(db.String, nullable=False)
    resource_url = db.Column(db.String, nullable=False)
    color_primary = db.Column(db.String, nullable=False)
    color_sec = db.Column(db.String)
    pattern = db.Column(db.String)
    occasion = db.Column(db.String, default="Any", nullable=False)
    season = db.Column(db.String, default="Any", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.Relationship("User", back_populates="articles")

    def __repr__(self):
        return f'Articles Article: {self.article_id} type: {self.type}'

class Outfit(db.Model):
    """"""

    __tablename__ = "outfit"

    outfit_id = db.Column(db.Integer, 
                          autoincrement=True,
                          primary_key=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.Relationship("User", back_populates="outfits")

    def __repr__(self):
        return f'Outfit Outfit: {self.outfit_id} User: {self.user_id}'

class OutfitArticles(db.Model):

    __tablename__ = "outfit_articles"

    outfit_art_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'), nullable=False)
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.outfit_id'), nullable=False)

    
    def __repr__(self):
        return f'Outfit_Articles Article: {self.article_id} Outfit Id: {self.outfit_id}'

class UserFavorites(db.Model):

    __tablename__ = "user_favorites"

    user_fav_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.outfit_id'), nullable=False)
    user_id = user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f'User_favorites Outfit Id: {self.outfit_id} User: {self.user_id}'
    

def connect_to_db(flask_app, db_uri="postgresql:///attires", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db! :)")


if __name__ == "__main__":
    connect_to_db(app)
