# Attire The Closet


Attire The Closet is a dynamic full-stack web application designed to revolutionize how we interact with our wardrobes. 

## About the Developer
Attire was created by Luisa Napier. See more about the developer on [Linkedin](https://www.linkedin.com/in/luisanapier/).

## Features

- User sign up. Creates a new account.
    ![alt text](https://github.com/luisanapier/closet-project/blob/main/static/Welcome-page.png)

- User log in. Username and passwords are checked if matches with an account from the user database.
-  ![alt text](https://github.com/luisanapier/closet-project/blob/main/static/Log-in-page.png)

-  Upload new files. To upload a new piece and store in user database, it's required the input of type to specify if it's a shirt, pants, skirt, dress, shoes or accessorie, a primary color or predominant color, occasion and season. Another non-required keywords are secondary color and pattern. The file then will be stored in the user database and displayed in their closet.
![alt text](https://github.com/luisanapier/closet-project/blob/main/static/Closet.png)

- Create different outfit options. A few keywords are also required to make a new outfit, in this case being occasion, season and a title. Users can also choose to add glasses, bags and hats separately, the title is used in case the user wants to favorite the outfit in their database. After the user clicks on the button to create outfit, it's possible to keep generating different outfit options.
- ![alt text](https://github.com/luisanapier/closet-project/blob/main/static/Create-outfit.png)
- ![alt text](https://github.com/luisanapier/closet-project/blob/main/static/Outfit-again.png)

- View all favorite outfits. Querying from the database all users favorite outfits.
- ![alt text](https://github.com/luisanapier/closet-project/blob/main/static/Favorites1.png)


> One of the most exhilarating aspects of building Attire was the challenge of querying articles from the database and using them to generate outfits. This process, while demanding, was also incredibly rewarding.


## Tech

Attire The Closet used this programming languages and tools to work properly:

- Python
- JavaScript
- Jinja2
- SQLAlchemy
- AJAX
- HTML
- CSS
- Cloudinary API
- BootStrap


And of course Attire itself is open source with a [public repository](https://github.com/luisanapier/closet-project) on GitHub.

## For version 2.0

- Password hashing: Passwords will be hashed before being saved to the database
- Unitest
- Delete a file: option to delete a file from closet.
