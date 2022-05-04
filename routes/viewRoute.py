from apiflask import APIBlueprint
from flask import render_template, request
from routes.priceRoute import *
from routes.currencyRoute import *

view_blueprint = APIBlueprint('views', __name__, enable_openapi=False)


@view_blueprint.route('transactiontype')
def transactiontype():
    return render_template('transactionTypeView.html')


@view_blueprint.route('/currency')
def currency():
    return render_template('currencyView.html')


@view_blueprint.route('/wallet')
def wallet():
    return render_template('walletView.html')


@view_blueprint.route('/price')
def price():
    currency_response = get_all_currencies()
    if currency_response.status_code == 200:
        cur_items = currency_response.json['results']
        return render_template('priceView.html', currencies=cur_items)
    return render_template('priceView.html')
