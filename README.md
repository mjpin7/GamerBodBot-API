![Python](https://img.shields.io/badge/Python-3.6-informational.svg)

# GamerBodBot-API

This repo contains source code for my REST-API to be used by my bot [GamerBotBot](https://github.com/mjpin7/GamerBodBot). The API is deployed on Heroku and is currently being used. It uses a user system to authenticate users to access endpoints. Also connects to a PostgreSQL database for various storage.

## Contents
* [Dependancies](#dependancies)
* [Endpoints](#endpoints)

---

## <a name="dependancies"></a>Dependancies
#### Flask
- Used as the web framework for the api

#### Flask-JWT Extended
- This is used for the user authentication of the api
- Creates user tokens to access endpoints

#### Flask-SQLAlchemy
- Flask wrapper for the SQLAlchemy package
- Allows management of database in classes and objects
- Models held in models folder

#### Flask-RESTful
- An extenstion to flask that helps create REST APIs

#### bcrypt
- Used for encryption of users passwords

#### uwsgi
- Used for serving the python application to Heroku

#### psycopg2
- PostgreSQL adapter for Python

## <a name="endpoints"></a>Endpoints
- /register
    - Registers a user into the API
    - Puts user in database
    - Required info:
    > ```{"username": "<username>", "password": "<password>"}```
- /login
    - Logs user into the API (provides a valid user with a JWT token)
    - Required info:
    > ```{"username": "<username>", "password": "<password>"}```
- /refresh
    - Provides a new (but not fresh) token to a valid user
    - Used once a token expires
- /meme
    - Returns a random meme to the user
