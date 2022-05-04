from flask_sqlalchemy import SQLAlchemy
from extenstions import db


class TransactionType(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    deposit = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return "<TransactionType(id='{}', type='{}', deposit='{}', description='{}')>" \
            .format(self.id, self.type, self.deposit, self.description)

    def __init__(self, data):
        self.type = data['type']
        self.deposit = data['deposit']
        self.description = data['description']
