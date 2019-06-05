import os
import requests
import json
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
            # Make request to game db api to get game information
            resp = requests.get("https://api-v3.igdb.com/search/", data={"search": json['game'], "fields": ["name", "game.url", "game.summary", "game.rating"]}, headers={"user-key": os.environ.get('GAME_API_KEY')})
            
            if resp.status_code == 200:
                gameInfo = resp.json()
                return {'message': "{} backlog item:\n```{}\n\nStatus: {}\n\nSummary: {}\n\nRating: {}\n\nView More: {}```".format(json['user_id'], json['game'], json['status'], gameInfo['game']['summary'], gameInfo['game']['rating'], gameInfo['game']['url'])}
            else:
                return {'message': "{} backlog item:\n```{}\n\nStatus: {}```".format(json['user_id'], json['game'], json['status'])}

            

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
        itemsFin = BacklogItemModel.find_by_status(user_id, "finished")
        itemsPlay = BacklogItemModel.find_by_status(user_id, "playing")
        itemsUnpl = BacklogItemModel.find_by_status(user_id, "unplayed")

        if itemsFin or itemsPlay or itemsUnpl:
            msg = "\t{}'s Backlog:\n```".format(user_id)
            flag = True
        
        if itemsFin:
            msg += "Finished:\n"
            for item in itemsFin:
                json = item.json()
                msg += '{}\n'.format(json['game'].title())
            msg += "\n"
        

        if itemsPlay:
            msg += "Playing:\n"
            for item in itemsPlay:
                json = item.json()
                msg += '{}\n'.format(json['game'].title())
            msg += "\n"

        

        if itemsPlay:
            msg += "Unplayed:\n"
            for item in itemsUnpl:
                json = item.json()
                msg += '{}'.format(json['game'].title())
            msg += "\n"
        
        if flag:
            msg += "\n```"
            return {'message': msg}


        return {'message': 'User {} has no backlog items'.format(user_id)}
        
        

