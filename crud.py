from model import db, connect_to_db, User, Articles, Outfit, OutfitArticles, UserFavorites
 
def create_user(username, name, email, password):
    """Register and return new users."""
 
    new_user = User(email=email, username=username,
                    password=password, name=name)
    
    db.session.add(new_user)
    db.session.commit()
    return new_user

def add_articles(type, resource_url, color_primary, color_sec,
                   pattern, occasion, season, user_id):
    
    article = Articles(type=type, resource_url=resource_url,
                       color_primary=color_primary, color_sec=color_sec,
                       pattern=pattern, occasion=occasion,
                       season=season, user_id=user_id)
    
    db.session.add(article)
    db.session.commit()
    return article

def create_outfit(title, user_id):

    outfit = Outfit(title=title, user_id=user_id)

    db.session.add(outfit)
    db.session.commit()
    return outfit
 
def outfit_articles(article_id, outfit_id):

    out_articles = OutfitArticles(article_id=article_id, outfit_id=outfit_id)
    
    db.session.add(out_articles)
    db.session.commit()
    return out_articles

def user_favorite(outfit_id, user_id):

    user_fav = UserFavorites(outfit_id=outfit_id, user_id=user_id)

    db.session.add(user_fav)
    db.session.commit()
    return user_fav

def check_user(username):

    is_user = User.query.filter(User.username == username).first()

    return is_user


if __name__ == '__main__':
    from server import app
    connect_to_db(app)