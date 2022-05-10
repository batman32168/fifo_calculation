from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from extenstions import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.Date, nullable=False)
    input_amount = db.Column(db.Float, nullable=False)
    input_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    output_amount = db.Column(db.Float, default=0.0)
    output_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    fee_amount = db.Column(db.Float, default=0.0)
    fee_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('transaction_type.id'), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))
    description = db.Column(db.String)
    receive_from = db.Column(db.String)
    send_to = db.Column(db.String)
    output_currency = relationship("Currency", foreign_keys=[output_id])
    input_currency = relationship("Currency", foreign_keys=[input_id])
    fee_currency = relationship("Currency", foreign_keys=[fee_id])

    def __repr__(self):
        return "<Transaction(id='{}', date='{}', input_amount='{}', input_id:'{}', " \
               "description:'{}', output_amount='{}', output_id='{}'," \
               "receive_from:'{}', send_to:'{}', wallet_id:'{}'" \
               "fee_amount:'{}', fee_id:'{}')>" \
            .format(self.id,
                    self.date,
                    self.input_amount,
                    self.input_id,
                    self.description,
                    self.output_amount,
                    self.output_id,
                    self.receive_from,
                    self.send_to,
                    self.wallet_id,
                    self.fee_amount,
                    self.fee_id)

    def __init__(self, data):
        self.date = data['date']
        self.input_amount = data['input_amount']
        self.input_id = data['input_id']
        if 'output_amount' in data and 'output_id' in data:
            self.output_amount = data['output_amount']
            self.output_id = data['output_id']
        else:
            self.output_amount = 0.00
            self.output_id = data['input_id']
        if 'fee_amount' in data and 'fee_id' in data:
            self.fee_amount = data['fee_amount']
            self.fee_id = data['fee_id']
        else:
            self.fee_amount = 0.00
            self.fee_id = data['input_id']

        if 'description' in data:
            self.description = data['description']
        if 'receive_from' in data:
            self.receive_from = data['receive_from']
        if 'send_to' in data:
            self.send_to = data['send_to']
        if 'type_id' in data:
            self.type_id = data['type_id']
        if 'wallet_id' in data:
            self.wallet_id = data['wallet_id']

