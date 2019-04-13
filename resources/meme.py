from flask_restful import Resource
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

        return {'meme': "files/pics/{}.jpg".format(rand_num)}, 200, {'Content-Type': 'image/jpeg'}