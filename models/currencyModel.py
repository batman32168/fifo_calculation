from flask_sqlalchemy import SQLAlchemy
from extenstions import db

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    long_name = db.Column(db.String)
    name = db.Column(db.String, nullable=False, unique=True)
    api_key = db.Column(db.String)
    price_url = db.Column(db.String)


    def __repr__(self):
        return "<Currency(id='{}', name='{}', long_name='{}'," \
               "api_key='{}', price_url='{}')>" \
            .format(self.id,
                    self.name,
                    self.long_name,
                    self.api_key,
                    self.price_url)

    def __init__(self, data):

        self.name = data['name']
        try:
            self.long_name = data['long_name']
        except:
            self.long_name=""
        try:
            self.api_key = data['api_key']
        except:
            self.api_key=""
        try:
            self.price_url = data['price_url']
        except:
            self.price_url=""
