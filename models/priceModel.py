from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from extenstions import db


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    source = db.Column(db.String)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = relationship("Currency")

    def __repr__(self):
        return "<Transaction(id='{}', date='{}', price='{}'," \
               "source:'{}', currency_id:'{}')>" \
            .format(self.id,
                    self.date,
                    self.price,
                    self.source,
                    self.currency_id)

    def __init__(self, data):
        self.date = data['date']
        self.price = data['price']
        self.currency_id = data['currency_id']
        try:
            self.source = data['source']
        except:
            self.source=""

    def get_price(self):
        return self.price

    def get_date(self):
        return self.date

    def get_source(self):
        return self.source

    def get_id(self):
        return self.id

    def get_currency_id(self):
        return self.currency_id
