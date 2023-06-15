from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from flask_session import Session
import jwt
import datetime
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
Session(app)

client = MongoClient('mongodb+srv://SAR11:SARHELI@cluster0.c4knhwy.mongodb.net/?retryWrites=true&w=majority')
db = client['FINAL3']  
collection = db['kelompok3'] 

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"


SECRET_KEY = "PROJECTFINAL"
TOKEN_KEY = "mytoken"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/super-admin/login')
def login_admin():
    return render_template('login_admin.html')
    

@app.route('/pasien/login', methods=['GET', 'POST'])
def login_pasien():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = collection.find_one({'username': username, 'password': password})

        if user:
            session['username'] = username
            return redirect(url_for('/dashboard'))
        else:
            return 'Login failed. Invalid username or password.'

    return render_template('login_pasien.html')

@app.route('/pasien/login/registrasi/Pasien', methods=['GET','POST'])
def register_pasien():
    if request.method == 'POST':
        # Menerima data yang dikirim melalui POST request
        username = request.form.get('username_give')
        password = request.form.get('password_give')

        # Lakukan proses registrasi dengan menyimpan data ke MongoDB
        data = {
            'username': username,
            'password': password
        }
        collection.insert_one(data)

        # Setelah berhasil mendaftar, arahkan pengguna ke halaman login
        return redirect('/pasien/login')
    else:
        return render_template('registrasi_pasien.html')


@app.route('/dashboard/data_dokter')
def dokter():
    return render_template('data_dokter.html')

@app.route('/dashboard/rekam_medis')
def medis():
    return render_template('rekam_medis.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)