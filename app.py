# coding=UTF-8

from flask import Flask,render_template,request
from sqlalchemy import *
import flask_cors
from common import redisInit
app = Flask(__name__)
cors = flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zxc110@121.196.111.9:3306/secs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
r=redisInit.get_connection  ()
print(app.config['SQLALCHEMY_DATABASE_URI'])
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db=engine.connect()

if __name__ == '__main__':

    app.run(debug=True)
