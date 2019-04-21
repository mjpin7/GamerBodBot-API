from db import db

class BacklogItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(80))
    status = db.Column(db.String(20))

    def __init__(self, _id, game, status):
        self.id = _id
        self.game = game
        self.status = status

    def json(self):
        return{
            'id': self.id,
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
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_by_game(cls, _id, _game):
        return cls.query.filter_by(id=_id, game=_game).first()
    