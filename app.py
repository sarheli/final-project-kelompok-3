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

client = MongoClient('mongodb+srv://finalproject1290:admin@cluster0.2stcpcn.mongodb.net/?retryWrites=true&w=majority')
db = client['FINAL3']  


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

@app.route('/super-admin/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        print(pw_hash)
        admin=db.admin.find_one({
            "username": username,
            "password": pw_hash,
        })
        
        if admin : 
            payload={
                'id': username,
                'role' : 'admin',
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
            } 
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            
            return jsonify(
                {
                    "result": "success",
                    "role":'admin',
                    "token": token,
                }
            )
        else: 
            return jsonify(
                {
                    "result": "faild",
                    "msg": 'akun tidak di temukan',
                }
            )
        
    return render_template('login_admin.html')
    

@app.route('/dashboard')
def dashboard_admin():
    token = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        admin = db.admin.find_one({'username' : payload['id']})
        
        if payload['role'] != 'admin':
            return redirect(url_for('login_pasien'), msg="You are not allowed to access this page!")
        
        return render_template('dashboard.html', admin=admin)
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('login_admin'), msg="Session expired!")


@app.route('/pasien/login', methods=['GET', 'POST'])
def login_pasien():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.pasien.find_one({'username': username, 'password': password})

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
        db.pasien.insert_one(data)

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