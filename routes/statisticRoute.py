from apiflask import APIBlueprint
from extenstions import db
from models.transactionModel import Transaction
from models.transactionTypeModel import TransactionType
from models.currencyModel import Currency
from sqlalchemy import func
from flask import jsonify
from utils.configuration import *

statistic_blueprint = APIBlueprint('statistic', __name__, enable_openapi=True)


@statistic_blueprint.get('/totalamount')
def get_total_amount():
    # ToDo: Add filter for wallets
    results = []
    accounting_curreny = get_accounting_currency()
    print(id)
    input_query = db.session.query(Transaction.input_id.label('cur_id'),
                                   func.sum(Transaction.input_amount).label('total')) \
        .group_by(Transaction.input_id)

    paginated_items = input_query.all()
    for item in paginated_items:
        if(item.cur_id !=accounting_curreny.id):
            currency_query = db.session.query(Currency).get(item.cur_id)
            output_query = db.session.query(func.sum(Transaction.output_amount).label('total')) \
                .filter(Transaction.output_id == item.cur_id).one_or_none()
            total_out = 0.0
            if output_query[0] is not None:
                total_out = output_query.total
            result = {
                'currency_name': currency_query.name,
                'currency_id': item.cur_id,
                'currency_long_name': currency_query.long_name,
                'deposit_amount': item.total,
                'withdraw_amount': total_out,
                'current_amount': item.total - total_out
            }
            results.append(result)
    return jsonify({
        'success': True,
        'page_count': 1,
        'page': 1,
        'results': results,
        'total_count': len(results)
    })


# ToDo: make this sense?
@statistic_blueprint.get('/amount')
def get_amount():
    results = []
    input_query = db.session.query(Transaction.input_id.label('cur_id'),
                                   func.sum(Transaction.input_amount).label('total')) \
        .group_by(Transaction.input_id)

    paginated_items = input_query.all()
    for item in paginated_items:
        currency_query = db.session.query(Currency).filter(Currency.id == item.cur_id).first()
        output_query = db.session.query(func.sum(Transaction.output_amount).label('total')) \
            .filter(Transaction.output_id == item.cur_id).one_or_none()
        total_out = 0.0
        if output_query is None:
            total_out = output_query.total
        result = {
            'currency_name': currency_query.name,
            'deposit_currency_id': item.cur_id,
            'currency_long_name': currency_query.long_name,
            'deposit_amount': item.total,
            'whitdraw_amount': total_out,
        }
        results.append(result)
    return jsonify({
        'success': True,
        'page_count': 1,
        'page': 1,
        'results': results,
        'total_count': len(results)
    })
