from apiflask import APIBlueprint
from apiflask import APIFlask, doc
from models.priceModel import Price
from models.currencyModel import Currency
from models.transactionModel import Transaction
from extenstions import db
from schemas.transactionSchema import *
from sqlalchemy import select, func
from flask import jsonify, request

transaction_blueprint = APIBlueprint('transaction', __name__, enable_openapi=True)


@transaction_blueprint.get('/transaction')
@transaction_blueprint.doc(summary='Get all currencies', description='Get all currencies include all fields')
def get_all_transactions():
    page = request.args.get('page', 1, type=int)
    raw_result = get_filter(request.args)
    paginated_items = (raw_result)
    results = [{
        'id': tt.id,
        'token_amount': tt.token_amount,
        'date': tt.date.strftime("%Y-%m-%dT%H:%M:%S"),
        'fait_amount': tt.fait_amount,
        'fee_amount': tt.fee_amount,
        'description': tt.description,
        'receive_from': tt.receive_from,
        'send_to': tt.send_to,
        'type_id': tt.type_id,
        'token_id': tt.token_id,
        'fiat_id': tt.fiat_id,
        'fee_id': tt.fee_id,
        'wallet_id': tt.wallet_id
    } for tt in paginated_items]
    return jsonify({
        'success': True,
        'page_size': len(paginated_items),
        'page': page,
        'results': results,
    })


@transaction_blueprint.get('/transaction/<transaction_id>')
@transaction_blueprint.doc(summary='Get a single currency', description='Get the data from the given currency id')
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
    if 'page' not in args:
        items = builder.all()
    else:
        if 'items' not in args:
            items = builder.paginate(int(request.args['page'])).items
        else:
            items = builder.paginate(page=int(request.args['page']),
                                     per_page=int(request.args['items'])).items
    return items
