from apiflask import APIBlueprint
from apiflask import APIFlask
from models.priceModel import Price
from models.currencyModel import Currency
from extenstions import db
from schemas.priceSchema import *
from sqlalchemy import select, func
from flask import jsonify, request

price_blueprint = APIBlueprint('price', __name__, enable_openapi=True)


@price_blueprint.get('/price')
def get_all_prices():
    page = request.args.get('page', 1, type=int)
    complete = db.session.query(Price).count()
    raw_result = get_filter(request.args)
    paginated_items = (raw_result)
    results = [{
        'id': pri.id,
        'price': pri.price,
        'date': pri.date.strftime("%Y-%m-%dT%H:%M:%S"),
        'source': pri.source,
        'currency':
            {
                'currency_id': pri.currency_id,
                'name':pri.currency.name,
                'long_name': pri.currency.long_name
            }
    } for pri in paginated_items]
    return jsonify({
        'success': True,
        'page_count': len(paginated_items),
        'page': page,
        'results': results,
        'total_count': complete
    })

@price_blueprint.get('/price/<price_id>')
@price_blueprint.output(PriceOutSchema, links={'currency_id': {'$ref': '#/currency/<int:currency_id>'}})
def get_price(price_id):
    raw_result = db.session.query(Price).get_or_404(price_id)
    return raw_result

@price_blueprint.post('/price')
#@price_blueprint.input(PriceCreateSchema)
def create_new_price():
    data = request.json
    new_price = Price(data)
    ref_currency = db.session.query(Currency).get(new_price.currency_id)
    if ref_currency is None:
        return {'messages':'currency not found.'},406
    try:
        db.session.add(new_price)
        db.session.flush()
        db.session.refresh(new_price)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    pos = PriceOutSchema()
    return pos.dump(new_price)


@price_blueprint.post('/price/<price_id>')
@price_blueprint.input(PriceCreateSchema)
@price_blueprint.output(PriceOutSchema)
def update_price(price_id,data):
    price_object = db.session.query(Price).get_or_404(price_id)
    try:
        temp_price = Price(data)
        price_object.price = temp_price.get_price()
        price_object.source = temp_price.get_source()
        price_object.date = temp_price.get_date()
        price_object.currency_id = temp_price.get_currency_id()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return price_object


@price_blueprint.delete('/price/<price_id>')
def delete_price(price_id):
    try:
        price_object = db.session.query(Price).get_or_404(price_id)
        db.session.delete(price_object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return {'Messages':'price with id {} delete sucessfull'.format(price_id)}


def get_filter(args):
    builder = Price.query
    for key in args:
        if hasattr(Price, key):
            vals = args.getlist(key)  # one or many
            builder = builder.filter(getattr(Price, key).in_(vals))
    if 'offset' not in args:
        offset = 0
        items = builder.all()
    else:
        offset = int(request.args['offset'])
    if 'limit' not in args:
        limit=25
    else:
        limit = int(request.args['limit'])
    try:
        page = int(offset/limit) +1
    except:
        page=1
    items = builder.paginate(page=page, per_page=limit).items
    return items
