from apiflask import APIFlask
from routes import currencyRoute, priceRoute, walletRoute, transactionTypeRoute, transactionRoute, viewRoute, statisticRoute
from extenstions import db
from flask_bootstrap import Bootstrap4
from flask import render_template, request
import os
from dotenv import load_dotenv

load_dotenv()

api_app = APIFlask(__name__)
api_app.secret_key = os.getenv('SECRECT_KEY')
Bootstrap4(api_app)

api_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

if os.getenv('DATABASE_LOG').upper() == 'TRUE':
    api_app.config['SQLALCHEMY_ECHO'] = True
    api_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
else:
    api_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api_app.config['SQLALCHEMY_ECHO'] = False


db.init_app(api_app)
api_app.register_blueprint(currencyRoute.currency_blueprint, url_prefix='/api/v0')
api_app.register_blueprint(priceRoute.price_blueprint, url_prefix='/api/v0')
api_app.register_blueprint(walletRoute.wallet_blueprint, url_prefix='/api/v0')
api_app.register_blueprint(transactionTypeRoute.transactionType_blueprint, url_prefix='/api/v0')
api_app.register_blueprint(transactionRoute.transaction_blueprint, url_prefix='/api/v0')
api_app.register_blueprint(statisticRoute.statistic_blueprint, url_prefix='/api/v0')
api_app.register_blueprint(viewRoute.view_blueprint, url_prefix='/view')

with api_app.app_context():
    db.create_all()

@api_app.route('/')
def index():
    return render_template('base.html')

if __name__ == "__main__":
    api_app.run()
