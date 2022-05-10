from sqlalchemy.orm import relationship
from extenstions import db



class Configuration(db.Model):
    # ToDo: Create view for configuration

    # ToDo: Autocreate price if new transition was created?
    id = db.Column(db.Integer, primary_key=True, unique=True)
    key = db.Column(db.String, unique=True, nullable=False)
    value = db.Column(db.String, nullable=False)
    description = db.Column(db.String)


    def __repr__(self):
        return "<Configuration(id='{}', key='{}', value='{}', description='{}')>" \
            .format(self.id,
                    self.key,
                    self.value,
                    self.description)
