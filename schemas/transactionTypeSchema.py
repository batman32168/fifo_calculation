from apiflask import Schema
from apiflask.fields import Integer, String, Boolean


class TransactionTypeInSchema(Schema):
    type = String(required=True)
    description = String()
    deposit = Boolean(required=True, default=True)


class TransactionTypeOutSchema(Schema):
    id = Integer()
    type = String()
    description = String()
    deposit = Boolean()
