from db import db
from bcrypt import hashpw, gensalt

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.LargeBinary)

    def __init__(self, username, password):
        self.username = username
        self.password = hashpw(password.encode('utf-8'), gensalt())

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()