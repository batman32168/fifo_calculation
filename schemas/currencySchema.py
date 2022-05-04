from apiflask import Schema
from apiflask.fields import Integer, String


class CurrencyCreateSchema(Schema):
    long_name = String(required=True)
    name = String(required=True)
    api_key = String()
    price_url = String()


class CurrencyOutSchema(Schema):
    id = Integer()
    long_name = String()
    name = String()
    api_key = String()
    price_url = String()
