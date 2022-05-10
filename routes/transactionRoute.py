from apiflask import APIBlueprint
from models.currencyModel import Currency
from models.transactionModel import Transaction
from models.extendedTransactionModel import  ExtendedTransaction
from extenstions import db
from schemas.transactionSchema import *
from flask import jsonify, request
from utils.configuration import *

transaction_blueprint = APIBlueprint('transaction', __name__, enable_openapi=True)


@transaction_blueprint.get('/transaction')
def get_all_transactions():
    page = request.args.get('page', 1, type=int)
    complete = db.session.query(Transaction).count()
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
                'currency_id': tt.fee_id,
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
def get_transaction(transaction_id):
    raw_result = db.session.query(Transaction).get_or_404(transaction_id)
    return raw_result





@transaction_blueprint.post('/transaction')
def create_new_transaction():
    data = request.json
    new_tt = Transaction(data)
    accounting_currency = get_accounting_currency()
    update_extended =''
    ref_currency = db.session.query(Currency).get(new_tt.input_id)
    if ref_currency is None:
        return {'messages': 'input currency not found.'}, 406
    if(int(new_tt.input_id) == accounting_currency.id):
        update_extended = 'input'
    ref_currency = db.session.query(Currency).get(new_tt.output_id)
    if ref_currency is None:
        return {'messages': 'output currency not found.'}, 406
    if(int(new_tt.output_id) == accounting_currency.id):
        update_extended = 'output'
    ref_currency = db.session.query(Currency).get(new_tt.fee_id)
    if ref_currency is None:
        return {'messages': 'fee currency not found.'}, 406
    try:
        db.session.add(new_tt)
        db.session.flush()
        db.session.refresh(new_tt)
        if update_extended != '':
            create_extended_values(new_tt,update_extended)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    pos = TransactionOutSchema()
    return pos.dump(new_tt)


@transaction_blueprint.post('/transaction/<transaction_id>')
@transaction_blueprint.input(TransactionCreateSchema)
@transaction_blueprint.output(TransactionOutSchema)
def update_transaction(transaction_id, data):
    trans_object = db.session.query(Transaction).get_or_404(transaction_id)
    try:
        temp_trans = Transaction(data)
        trans_object.date = temp_trans.date
        trans_object.input_amount = temp_trans.input_amount
        trans_object.output_amount = temp_trans.output_amount
        trans_object.fee_amount = temp_trans.fee_amount
        trans_object.description = temp_trans.description
        trans_object.receive_from = temp_trans.receive_from
        trans_object.send_to = temp_trans.send_to
        trans_object.type_id = temp_trans.type_id
        trans_object.input_id = temp_trans.input_id
        trans_object.output_id = temp_trans.output_id
        trans_object.fee_id = temp_trans.fee_id
        trans_object.wallet_id = temp_trans.wallet_id
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return trans_object


@transaction_blueprint.delete('/transaction/<transaction_id>')
def delete_transaction(transaction_id):
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


def create_extended_values(tt, update_value):
    # todo: failure?
    ext_type_id =0
    value =0.0
    if update_value=='input':
        ext_type_id = get_average_buy_price().id
        value = tt.input_amount / tt.output_amount

    if update_value == 'output':
        ext_type_id = get_average_buy_price().id
        value = tt.output_amount / tt.input_amount
    ext = ExtendedTransaction(value=value, extended_type_id = ext_type_id, transaction_id=tt.id)
    db.session.add(ext)

