from apiflask import APIBlueprint
from apiflask import APIFlask
from models.currencyModel import Currency
from extenstions import db
from schemas.currencySchema import *
from sqlalchemy import select
from flask import jsonify, request

currency_blueprint = APIBlueprint('currency', __name__, enable_openapi=True)


@currency_blueprint.get('/currency')
def get_all_currencies():
    page = request.args.get('page', 1, type=int)
    complete = db.session.query(Currency).count()
    raw_result = get_filter(request.args)
    paginated_items = (raw_result)
    results = [{
        'id': cur.id,
        'long_name': cur.long_name,
        'name': cur.name,
        'api_key': cur.api_key,
        'price_url': cur.price_url
    } for cur in paginated_items]
    return jsonify({
        'success': True,
        'page_count': len(paginated_items),
        'page': page,
        'results': results,
        'total_count': complete
    })


@currency_blueprint.get('/currency/<currency_id>')
@currency_blueprint.output(CurrencyOutSchema)
def get_currency(currency_id):
    raw_result = db.session.query(Currency).get(currency_id)
    return raw_result


@currency_blueprint.post('/currency')
@currency_blueprint.input(CurrencyCreateSchema)
@currency_blueprint.output(CurrencyOutSchema)
def create_new_currency(data):
    cur = Currency(data)
    try:
        db.session.add(cur)
        db.session.flush()
        db.session.refresh(cur)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return cur


@currency_blueprint.post('/currency/<currency_id>')
@currency_blueprint.input(CurrencyCreateSchema)
@currency_blueprint.output(CurrencyOutSchema)
def update_currency(currency_id, data):
    currency_object = db.session.query(Currency).get(currency_id)
    try:
        temp_cur = Currency(data)
        currency_object.name = temp_cur.name
        currency_object.long_name = temp_cur.long_name
        currency_object.api_key = temp_cur.api_key
        currency_object.price_url = temp_cur.price_url
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return currency_object


@currency_blueprint.delete('/currency/<currency_id>')
def id_currency(currency_id):
    try:
        currency_object = db.session.query(Currency).get(currency_id)
        db.session.delete(currency_object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return {'Messages': 'currency with id {} delete successfully'.format(currency_id)}


def get_filter(args):
    builder = Currency.query
    for key in args:
        if hasattr(Currency, key):
            vals = args.getlist(key)  # one or many
            builder = builder.filter(getattr(Currency, key).in_(vals))
    if 'offset' not in args:
        offset = 0
        items = builder.all()
    else:
        offset = int(request.args['offset'])
    if 'limit' not in args:
        limit = 25
    else:
        limit = int(request.args['limit'])
    try:
        page = int(offset / limit) + 1
    except:
        page = 1
    items = builder.paginate(page=page, per_page=limit).items
    return items
