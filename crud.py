from model import db, connect_to_db, User
 
def create_user(username, name, email, password):
    """Register and return new users."""
 
    new_user = User(email=email, username=username,
                    password=password, name=name)
    
    db.session.add(new_user)
    db.session.commit()
    return new_user


 
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)