from flask_sqlalchemy import SQLAlchemy
from extenstions import db


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return "<WalletPlatform(id='{}', name='{}', url='{}', description='{}')>" \
            .format(self.id, self.name, self.url, self.description)

    def __init__(self, data):
        self.name = data['name']
        try:
            self.description = data['description']
        except:
            self.description = ""
        try:
            self.url = data['url']
        except:
            self.url =""