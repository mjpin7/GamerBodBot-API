import os
from flask_restful import Resource, reqparse
from models.backlog import BacklogItemModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity
)

_backlog_parser = reqparse.RequestParser()
_backlog_parser.add_argument('game',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
)
_backlog_parser.add_argument('status',
                            type=str,
                            required=False,
                            help="This field can be left blank"
)

class Backlog(Resource):
    @jwt_required
    def post(self, user_id):
        data = _backlog_parser.parse_args()

        if BacklogItemModel.find_by_game(user_id, data['game']):
            return {'message': 'User {} already has game "{}" in their backlog'.format(user_id, data['game'])}
        
        item = BacklogItemModel(user_id, **data)
        item.save_to_db()

        return {'message': 'Backlog item {} with status {} was successfully created for user {}'.format(data['game'], data['status'], user_id)}
    
    @jwt_required
    def get(self, user_id):
        data = _backlog_parser.parse_args()
        item = BacklogItemModel.find_by_game(user_id, data['game'])

        if item:
            json = item.json()
            return {'message': "{} backlog item: {} status {}".format(json['user_id'], json['game'], json['status'])}

        return {'message': 'Game {} was not found in user {}\'s backlog'.format(data['game'], user_id)}
    
    @jwt_required
    def put(self, user_id):
        data = _backlog_parser.parse_args()

        item = BacklogItemModel.find_by_game(user_id, data['game'])

        if item is None:
            return {'message': 'Backlog item {} does not exist. Can not change status'.format(data['game'])}
        
        item.status = data['status']
        item.save_to_db()

        if data['status'] == "playing":
            return {"message": "{} has started playing {}".format(user_id, data['game'])}
        elif data['status'] == "finished":
            return {"message": "{} has completed {}!".format(user_id, data['game'])}
        

    @jwt_required
    def delete(self, user_id):
        data = _backlog_parser.parse_args()

        item = BacklogItemModel.find_by_game(user_id, data['game'])

        if item is None:
            return {'message': 'Backlog item {} does not exist. Can not delete'.format(data['game'])}
        
        item.delete_from_db()

        return {'message': 'Backlog item {} deleted'.format(data['game'])}

class BacklogList(Resource):
    def get(self, user_id):
        items = BacklogItemModel.find_all_by_id(user_id)

        if len(items) == 0:
            return {'message': 'User {} has no items in their backlog'}
        
        return {'message': items}

