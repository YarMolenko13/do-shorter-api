from flask import Flask, request, redirect, render_template
from flask_restful import Api, Resource, reqparse
import hashlib

from db import Postgers

import random
app = Flask(__name__)
api = Api(app)
db = Postgers()
# client = app.test_client()

class Url(Resource):
    def get(self, token):
        try:
            long_url = db.select(token)
            db.count_plus(token)
            return redirect(long_url)
        except:
            return 404


class Statistics(Resource):
    def get(self, token):
        return db.select_count(token)


def get_hex(url):
    hash = hashlib.sha224(url.encode('utf-8'))
    hex_dig = hash.hexdigest()
    return hex_dig[0:6]

def do_short(hex):
    base_url = request.url
    new_url = base_url + str(hex)
    return new_url

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        hex = get_hex(long_url[-5])
        if db.is_unic(hex):
            new_url = do_short(hex)
            db.insert(long_url, new_url, hex)
            return render_template('index.html', long_url=new_url), 201
        else:
            # если токен не уникальный
            hex = get_hex(long_url[0:6])
            new_url = do_short(hex)
            db.insert(long_url, new_url, hex)
            return render_template('index.html', long_url=new_url), 201
    return render_template('index.html')


api.add_resource(Url, "/<string:token>")
api.add_resource(Statistics, "/statistics/<string:token>")

if __name__ == '__main__':
    app.run()