from extenstions import db


class ExtendedType(db.Model):
    # ToDo: default Table -> Create some default values
    id = db.Column(db.Integer, primary_key=True, unique=True)
    key = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<ExtendedType(id='{}', key='{}', description='{}')>" \
            .format(self.id,
                    self.key,
                    self.description)