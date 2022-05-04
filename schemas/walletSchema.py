from apiflask import Schema
from apiflask.fields import Integer, String


class WalletInSchema(Schema):
    name = String(required=True)
    url = String()
    description = String()


class WalletOutSchema(Schema):
    id = Integer()
    name = String()
    url = String()
    description = String()
