from apiflask import Schema
from apiflask.fields import Integer, String, DateTime, Float
from apiflask.validators import Length, OneOf


class TransactionCreateSchema(Schema):
    date = DateTime(required=True)
    token_amount = Float(required=True)
    fiat_amount = Float()
    fee_amount = Float()
    description = String()
    receive_from = String()
    send_to = String()
    type_id = Integer(required=True)
    token_id = Integer(required=True)
    fiat_id = Integer()
    fee_id = Integer()
    wallet_id = Integer(required=True)


class TransactionOutSchema(Schema):
    id = Integer()
    token_amount = Float()
    fiat_amount = Float()
    fee_amount = Float()
    description = String()
    receive_from = String()
    send_to = String()
    type_id = Integer()
    token_id = Integer()
    fiat_id = Integer()
    fee_id = Integer()
    wallet_id = Integer()
