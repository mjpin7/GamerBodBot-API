from flask_restful import Resource
from flask import make_response, Response
from flask_jwt_extended import (
    jwt_required,
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity
)
from random import randint

class Meme(Resource):
    @jwt_required
    def get(self):
        rand_num = randint(1, 429)
        response = make_response("https://github.com/mjpin7/GamerBodBot-API/tree/master/files/pics{}.jpg".format(rand_num), 200)
        response.headers.extend({'Content-Type': 'image/jpeg'})
        return response