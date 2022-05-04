from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from extenstions import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.Date, nullable=False)
    token_amount = db.Column(db.Float, nullable=False)
    fiat_amount = db.Column(db.Float, default=0.0)
    fee_amount = db.Column(db.Float, default=0.0)
    description = db.Column(db.String)
    receive_from = db.Column(db.String)
    send_to = db.Column(db.String)
    type_id = db.Column(db.Integer, db.ForeignKey('transaction_type.id'), nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    fiat_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    fee_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)

    def __repr__(self):
        return "<Transaction(id='{}', date='{}', token_amount='{}', token_id:'{}', " \
               "description:'{}', fiat_amount='{}', fiat_id='{}'," \
               "receive_from:'{}', send_to:'{}', wallet_id:'{}'" \
               "fee_amount:'{}', fee_id:'{}')>" \
            .format(self.id,
                    self.date,
                    self.token_amount,
                    self.token_id,
                    self.description,
                    self.fiat_amount,
                    self.fiat_id,
                    self.receive_from,
                    self.send_to,
                    self.wallet_id,
                    self.fee_amount,
                    self.fee_id)

    def __init__(self, data):
        self.date = data['date']
        self.token_amount = data['token_amount']
        self.fiat_amount = data['fiat_amount']
        self.fiat_amount = data['fee_amount']
        self.description = data['description']
        self.receive_from = data['receive_from']
        self.send_to = data['send_to']
        self.type_id = data['type_id']
        self.token_id = data['token_id']
        self.fiat_id = data['fiat_id']
        self.fee_id = data['fee_amount']
        self.wallet_id = data['wallet_id']
