from apiflask import Schema
from apiflask.fields import Integer, String, Float, DateTime


class PriceCreateSchema(Schema):
    date = DateTime(required=True)
    price = Float(required=True)
    source = String()
    currency_id = Integer(required=True)


class PriceOutSchema(Schema):
    id = Integer()
    date = DateTime()
    price = Float()
    currency_id = Integer()
    source = String()

prices_out_schema = PriceOutSchema(many=True)