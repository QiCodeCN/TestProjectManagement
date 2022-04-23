# -*- coding:utf-8 -*-
from flask import Flask
from apis.user import app_user
from apis.product import app_product
from apis.application import app_application
from apis.testmanager import test_manager
from apis.dashboard import test_dashboard
from flask_cors import CORS
from configs import format
from flask import make_response, render_template

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(app_application)
app.register_blueprint(test_manager)
app.register_blueprint(test_dashboard)

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.errorhandler(413)
def request_entity_too_large(err):
    '''自定义的处理错误方法'''
    resp_failed = format.resp_format_failed
    resp_failed["message"] = '文件超出大小限制10M'
    return resp_failed

@app.after_request
def after_request(response):
    if response.status_code != 200:
        headers = {'content-type': 'application/json'}
        res = make_response(format.resp_format_failed)
        res.headers = headers

        return res
    return response

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(port=8086)

