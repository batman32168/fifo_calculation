from apiflask import APIBlueprint
from apiflask import APIFlask
from models.walletModel import Wallet
from extenstions import db
from schemas.walletSchema import *
from sqlalchemy import select
from flask import jsonify, request

wallet_blueprint = APIBlueprint('wallet', __name__, enable_openapi=True)


@wallet_blueprint.get('/wallet')
def get_all_wallets():
    page = request.args.get('page', 1, type=int)
    complete = db.session.query(Wallet).count()
    raw_result = get_filter(request.args)
    paginated_items = (raw_result)
    results = [{
        'id': wal.id,
        'name': wal.name,
        'url': wal.url,
        'description': wal.description
    } for wal in paginated_items]
    return jsonify({
        'success': True,
        'page_count': len(paginated_items),
        'page': page,
        'results': results,
        'total_count': complete
    })


@wallet_blueprint.get('/wallet/<wallet_id>')
@wallet_blueprint.output(WalletOutSchema)
def get_wallet(wallet_id):
    raw_result = db.session.query(Wallet).get_or_404(wallet_id)
    return raw_result


@wallet_blueprint.post('/wallet')
@wallet_blueprint.input(WalletInSchema)
@wallet_blueprint.output(WalletOutSchema)
def create_new_wallet(data):
    new_wallet = Wallet(data)
    try:
        db.session.add(new_wallet)
        db.session.flush()
        db.session.refresh(new_wallet)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return new_wallet


@wallet_blueprint.post('/wallet/<wallet_id>')
@wallet_blueprint.input(WalletInSchema)
@wallet_blueprint.output(WalletOutSchema)
def update_wallet(wallet_id, data):
    wallet_object = db.session.query(Wallet).get_or_404(wallet_id)
    try:
        temp_wallet = Wallet(data)
        wallet_object.name = temp_wallet.name
        wallet_object.url = temp_wallet.url
        wallet_object.description = temp_wallet.description
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return wallet_object


@wallet_blueprint.delete('/wallet/<wallet_id>')
def delete_wallet(wallet_id):
    try:
        wallet_object = db.session.query(Wallet).get_or_404(wallet_id)
        db.session.delete(wallet_object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    return {'Messages': 'wallet with id {} delete successfully'.format(wallet_id)}


def get_filter(args):
    builder = Wallet.query
    for key in args:
        if hasattr(Wallet, key):
            vals = args.getlist(key)  # one or many
            builder = builder.filter(getattr(Wallet, key).in_(vals))
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
