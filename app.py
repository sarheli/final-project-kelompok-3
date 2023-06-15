from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

SECRET_KEY = "PROJECTFINAL"
TOKEN_KEY = "mytoken"

MONGODB_CONNECTION_STRING = "mongodb+srv://finalproject387:finalproject@cluster0.86upttf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.dbfinal


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/super-admin/login')
def login_admin():
    return render_template('login_admin.html')
    

@app.route('/pasien/login')
def login_pasien():
   
        return render_template('login_pasien.html')


@app.route('/pasien/login/registrasi/Pasien', methods=['GET', 'POST'])
def registrasi_pasien():
    # nama = request.form['nama']
    # username = request.form['username']
    # telpon = request.form['telpon']
    # password = request.form['password']
    # retype_password = request.form['retype_password']
    # alamat = request.form['alamat']

    # # Lakukan validasi data
    # if password != retype_password:
    #     return 'Konfirmasi password tidak sesuai'

    # # Simpan data ke basis data atau lakukan tindakan lainnya

    # return 'Registrasi berhasil! Selamat datang, ' + nama

    
    return render_template('registrasi_pasien.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/data_dokter')
def dokter():
    return render_template('data_dokter.html')

@app.route('/dashboard/rekam_medis')
def medis():
    return render_template('rekam_medis.html')

@app.route('/dashboard/data_antrian')
def antri():
    return render_template('data_antrian.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)