from apiflask import APIBlueprint
from apiflask import APIFlask
from models.priceModel import Price
from models.currencyModel import Currency
from models.transactionModel import Transaction
from extenstions import db
from schemas.transactionSchema import *
from sqlalchemy import select, func
from flask import jsonify, request

transaction_blueprint = APIBlueprint('transaction', __name__, enable_openapi=True)


@transaction_blueprint.get('/transaction')
def get_all_transactions():
    page = request.args.get('page', 1, type=int)
    complete = db.session.query(Currency).count()
    raw_result = get_filter(request.args)
    paginated_items = (raw_result)
    results = [{
        'id': tt.id,
        'input_amount': tt.input_amount,
        'input_currency':
            {
                'currency_id':  tt.input_id,
                'name':  tt.input_currency.name,
                'long_name':  tt.input_currency.long_name,
            },
        'date': tt.date.strftime("%Y-%m-%dT%H:%M:%S"),
        'output_amount': tt.output_amount,
        'output_currency':
            {
                'currency_id': tt.output_id,
                'name': tt.output_currency.name,
                'long_name': tt.output_currency.long_name
            },
        'fee_amount': tt.fee_amount,
        'fee_currency':
            {
                'currency_id': tt.fee_amount.id,
                'name': tt.fee_currency.name,
                'long_name': tt.fee_currency.long_name
            },
        'description': tt.description,
        'receive_from': tt.receive_from,
        'send_to': tt.send_to,
        'type_id': tt.type_id,
        'wallet_id': tt.wallet_id
    } for tt in paginated_items]
    return jsonify({
        'success': True,
        'page_count': len(paginated_items),
        'page': page,
        'results': results,
        'total_count': complete
    })


@transaction_blueprint.get('/transaction/<transaction_id>')
@transaction_blueprint.output(TransactionOutSchema)
def get_price(transaction_id):
    raw_result = db.session.query(Transaction).get_or_404(transaction_id)
    return raw_result


@transaction_blueprint.post('/transaction')
@transaction_blueprint.input(TransactionCreateSchema)
def create_new_price(data):
    new_tt = Transaction(data)
    ref_currency = db.session.query(Currency).get(new_tt.token_id)
    if ref_currency is None:
        return {'messages': 'token currency not found.'}, 406
    ref_currency = db.session.query(Currency).get(new_tt.fiat_id)
    if ref_currency is None:
        return {'messages': 'fiat currency not found.'}, 406
    ref_currency = db.session.query(Currency).get(new_tt.fee_id)
    if ref_currency is None:
        return {'messages': 'fee currency not found.'}, 406
    try:
        db.session.add(new_tt)
        db.session.flush()
        db.session.refresh(new_tt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    pos = TransactionOutSchema()
    return pos.dump(new_tt)


@transaction_blueprint.post('/transaction/<transaction_id>')
@transaction_blueprint.input(TransactionCreateSchema)
@transaction_blueprint.output(TransactionOutSchema)
def update_price(transaction_id, data):
    trans_object = db.session.query(Transaction).get_or_404(transaction_id)
    try:
        temp_trans = Transaction(data)
        trans_object.date = temp_trans.date
        trans_object.token_amount = temp_trans.token_amount
        trans_object.fiat_amount = temp_trans.fiat_amount
        trans_object.fee_amount = temp_trans.fee_amount
        trans_object.description = temp_trans.description
        trans_object.receive_from = temp_trans.receive_from
        trans_object.send_to = temp_trans.send_to
        trans_object.type_id = temp_trans.type_id
        trans_object.token_id = temp_trans.token_id
        trans_object.fiat_id = temp_trans.fiat_id
        trans_object.fee_id = temp_trans.fee_id
        trans_object.wallet_id = temp_trans.wallet_id
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return trans_object


@transaction_blueprint.delete('/transaction/<transaction_id>')
def delete_price(transaction_id):
    try:
        trans_object = db.session.query(Transaction).get_or_404(transaction_id)
        db.session.delete(trans_object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return {'Messages': 'Transaction with id {} delete successfully'.format(transaction_id)}


def get_filter(args):
    builder = Transaction.query
    for key in args:
        if hasattr(Transaction, key):
            vals = args.getlist(key)  # one or many
            builder = builder.filter(getattr(Transaction, key).in_(vals))
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
