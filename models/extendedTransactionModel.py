from extenstions import db


class ExtendedTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    extended_type_id = db.Column(db.Integer, db.ForeignKey('extended_type.id'), nullable=False)

    def __repr__(self):
        return "<ExtendedTransaction(id='{}', transaction_id='{}', value='{}'," \
               "extended_type_id:'{}')>" \
            .format(self.id,
                    self.transaction_id,
                    self.value,
                    self.extended_type_id)

    def __init__(self, data):
        self.transaction_id = data['transaction_id']
        self.value = data['value']
        self.extended_type_id = data['extended_type_id']

    def __init__(self, transaction_id, value, extended_type_id):
        self.transaction_id = transaction_id
        self.value = value
        self.extended_type_id = extended_type_id
