import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserLogin, UserRegister, TokenRefresher
from resources.meme import Meme

##
#
# CONFIGS
#
##
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get('SECRET_KEY')
api = Api(app)

jwt = JWTManager(app)

##
#
# CALLBACKS FOR JWT ERRORS
#
##
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Change to evironment var
        return {'is_admin': True}
    
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.unauthorized_loader
def unauth_loader_callback():
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_loader_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'token_invalid'
    }), 401

##
#
# ENDPOINTS
#
##
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresher, '/refresh')
api.add_resource(TokenRefresher, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)