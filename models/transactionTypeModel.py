from flask_sqlalchemy import SQLAlchemy
from extenstions import db


class TransactionType(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    deposit = db.Column(db.Boolean, default=True)
    interest =db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<TransactionType(id='{}', name='{}', deposit='{}', description='{}')>" \
            .format(self.id, self.type, self.deposit, self.description)

    def __init__(self, data):
        self.type = data['name']
        if 'deposit' in data:
            self.deposit = data['deposit']
        else:
            self.deposit=True
        if 'interest' in data:
            self.interest = data['interest']
        else:
            self.interest=False
        if 'description' in data:
            self.description = data['description']
        else:
            self.description=""
