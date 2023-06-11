from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

SECRET_KEY = "PROJECTFINAL"
TOKEN_KEY = "mytoken"

MONGODB_CONNECTION_STRING = "mongodb+srv://finalproject1290:Final123@@cluster0.jyp22vw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.dbfinal

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/super-admin/login')
def login_admin():
    return render_template('login_admin.html')
    

@app.route('/pasien/login')
def login_pasien():
    return render_template('login_pasien.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)
