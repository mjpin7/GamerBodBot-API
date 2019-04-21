import os
from flask_restful import Resource, reqparse
from models.backlog import BacklogItemModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
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
    def post(self, _id):
        data = _backlog_parser.parse_args()

        if BacklogItemModel.find_by_game(_id, data['game']):
            return {'message': 'User {} already has game "{}" in their backlog'.format(_id, data['game'])}
        
        item = BacklogItemModel(**data)
        item.save_to_db()

        return {'message': 'Backlog item {} with status {} was successfully created for user {}'.format(_game, data['status'], _id)}
    
    @jwt_required
    def get(self, _id):
        data = _backlog_parser.parse_args()
        item = BacklogItemModel.find_by_game(_id, data['game'])

        if item:
            return item.json()

        return {'message': 'Game {} was not found in user {}\'s backlog'.format(data['game'], _id)}
    
    @jwt_required
    def put(self, _id):
        data = _backlog_parser.parse_args()

        item = BacklogItemModel.find_by_game(_id, data['game'])

        if item is None:
            item - BacklogItemModel(_id, data['game'], **data)
        else:
            item.status = data['status']

        item.save_to_db()

        return item.json()

