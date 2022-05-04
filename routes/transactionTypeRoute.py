from apiflask import APIBlueprint
from apiflask import APIFlask, doc
from models.transactionTypeModel import TransactionType
from extenstions import db
from schemas.transactionTypeSchema import *
from sqlalchemy import select
from flask import jsonify, request

transactionType_blueprint = APIBlueprint('transactionType', __name__, enable_openapi=True)


@transactionType_blueprint.get('/transactiontype')
def get_all_tt():
    page = request.args.get('page', 1, type=int)
    raw_result = get_filter(request.args)
    paginated_items = (raw_result)
    results = [{
        'id': tt.id,
        'type': tt.type,
        'deposit': tt.deposit,
        'description': tt.description
    } for tt in paginated_items]
    return jsonify({
        'success': True,
        'page_size': len(paginated_items),
        'page': page,
        'results': results,
    })


@transactionType_blueprint.get('/transactiontype/<transactiontype_id>')
@transactionType_blueprint.doc(summary='Get a single currency', description='Get the data from the given currency id')
@transactionType_blueprint.output(TransactionTypeOutSchema)
def get_tt(transactiontype_id):
    raw_result = db.session.query(TransactionType).get_or_404(transactiontype_id)
    return raw_result

@transactionType_blueprint.post('/transactiontype')
@transactionType_blueprint.input(TransactionTypeInSchema)
@transactionType_blueprint.output(TransactionTypeOutSchema)
def create_new_tt(data):
    new_tt = TransactionType(data)
    try:
        db.session.add(new_tt)
        db.session.flush()
        db.session.refresh(new_tt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return new_tt


@transactionType_blueprint.post('/transactiontype/<transactiontype_id>')
@transactionType_blueprint.input(TransactionTypeInSchema)
@transactionType_blueprint.output(TransactionTypeOutSchema)
def update_tt(transactiontype_id, data):
    tt_object = db.session.query(TransactionType).get_or_404(transactiontype_id)
    try:
        temp_tt = TransactionType(data)
        tt_object.type = temp_tt.type
        tt_object.deposit = temp_tt.deposit
        tt_object.description = temp_tt.description
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return tt_object


@transactionType_blueprint.delete('/transactiontype/<transactiontype_id>')
def delete_tt(transactiontype_id):
    try:
        tt_object = db.session.query(TransactionType).get_or_404(transactiontype_id)
        db.session.delete(tt_object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return {'Messages':'transactiontype with id {} delete successfully'.format(transactiontype_id)}


def get_filter(args):
    builder = TransactionType.query
    for key in args:
        if hasattr(TransactionType, key):
            vals = args.getlist(key)  # one or many
            builder = builder.filter(getattr(TransactionType, key).in_(vals))
    if 'page' not in args:
        items = builder.all()
    else:
        if 'items' not in args:
            items = builder.paginate(int(request.args['page'])).items
        else:
            items = builder.paginate(page=int(request.args['page']),
                                     per_page=int(request.args['items'])).items
    return items
