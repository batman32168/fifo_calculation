from models.configurationModel import *
from models.currencyModel import *
from models.extendedTypeModel import *
from extenstions import db
from sqlalchemy import func


def get_accounting_currency():
    # ToDo: Create configuration Value in database
    cur_id = db.session.query(Configuration.value).filter(
        func.Lower(Configuration.key) == 'accounting currency').one_or_none()
    if cur_id is None:
        return db.session.query(Currency).order_by(Currency.id).first()
    return db.session.query(Currency).get(cur_id)


def get_average_buy_price():
    #todo: Create configuration value
    id = db.session.query(ExtendedType.id).filter(
        func.Lower(ExtendedType.key) == 'average buy price').one_or_none()
    if id is None:
        #todo: failure?
        pass
    return db.session.query(ExtendedType).get(id)

def get_average_sold_price():
    #todo: Create configuration value
    id = db.session.query(ExtendedType.value).filter(
        func.Lower(ExtendedType.key) == 'average sold price').one_or_none()
    if id is None:
        #todo: failure?
        pass
    return db.session.query(ExtendedType).get(id)

def get_part_sale_quantity():
    #todo: Create configuration value
    id = db.session.query(ExtendedType.value).filter(
        func.Lower(ExtendedType.key) == 'part sale quantity').one_or_none()
    if id is None:
        # todo: failure?
        pass

    return db.session.query(ExtendedType).get(id)
