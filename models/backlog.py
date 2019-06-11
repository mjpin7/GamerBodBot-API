from db import db

class BacklogItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    game = db.Column(db.String(80))
    status = db.Column(db.String(20))

    def __init__(self, user_id, game, status):
        self.user_id = user_id
        self.game = game.capitalize()
        self.status = status

    def json(self):
        return{
            'user_id': self.user_id,
            'game': self.game,
            'status': self.status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all_by_id(cls, _id):
        return cls.query.filter_by(user_id=_id).all()

    @classmethod
    def find_by_game(cls, _id, _game):
        return cls.query.filter_by(user_id=_id, game=_game).first()

    @classmethod
    def find_by_status(cls, _id, _status):
        return cls.query.filter_by(user_id=_id, status=_status).all()
    