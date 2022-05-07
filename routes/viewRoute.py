from apiflask import APIBlueprint
from flask import render_template, request
from routes.priceRoute import *
from routes.transactionTypeRoute import *
from routes.walletRoute import *
from routes.currencyRoute import *

view_blueprint = APIBlueprint('views', __name__, enable_openapi=False)


@view_blueprint.route('transactiontype')
def transactiontype():
    return render_template('transactionTypeView.html')


@view_blueprint.route('/currency')
def currency():
    return render_template('currencyView.html')



@view_blueprint.route('/transaction')
def transaction():
    cur_items= None
    wallet_items =None
    tt_items = None
    response = get_all_currencies()
    if response.status_code == 200:
        cur_items = response.json['results']
    response = get_all_wallets()
    if response.status_code == 200:
        wallet_items = response.json['results']
    response = get_all_tt()
    if response.status_code == 200:
        tt_items = response.json['results']
    return render_template('transactionView.html', currencies=cur_items, transaction_types = tt_items, wallets=wallet_items)

@view_blueprint.route('/wallet')
def wallet():
    return render_template('walletView.html')


@view_blueprint.route('/price')
def price():
    cur_items = None
    wallets = None
    tt = None
    response = get_all_currencies()
    if response.status_code == 200:
        cur_items = response.json['results']
        response =None
    response = get_all_wallets()
    if response.status_code == 200:
        cur_items = response.json['results']
        response = None
    response = get_all_tt()
    if response.status_code == 200:
        cur_items = response.json['results']
        response = None
    return render_template('priceView.html', currencies=cur_items, wallets=wallets, transaction_types=tt)


