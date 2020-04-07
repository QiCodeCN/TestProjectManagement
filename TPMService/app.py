# -*- coding:utf-8 -*-
from flask import Flask
from apis.user import app_user
from apis.product import app_product
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(app_user)
app.register_blueprint(app_product)

if __name__ == '__main__':
    app.run(debug=True)
