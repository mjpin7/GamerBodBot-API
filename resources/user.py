from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity
)
from bcrypt import hashpw, gensalt

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
)
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
)

##
#
# Register resource. Registers the user in with jwt (returns an access and refresh token) and saves to db
#
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400
        
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, 201

##
#
# Log in resource. Logs the user in with jwt (returns an access and refresh token)
#
class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in db
        user = UserModel.find_by_username(data['username'])

        # check password (what "authenticate" method used to do)
        if user and safe_str_cmp(hashpw(data['password'].encode('utf-8'), user.password.encode('utf-8')), user.password.encode('utf-8')):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        
        return {'message': 'Invalid credentials'}, 401

# For future use
class TokenRefresher(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200