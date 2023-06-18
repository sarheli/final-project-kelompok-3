from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson import ObjectId
import jwt
import datetime
from datetime import datetime, timedelta
import hashlib


app = Flask(__name__)

client = MongoClient('mongodb+srv://finalproject1290:admin@cluster0.2stcpcn.mongodb.net/?retryWrites=true&w=majority')
db = client['FINAL3']  
collection = db["ulasan"]  


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
def dashboard_pasien():
    # an endpoint for retrieving a user's profile information
    # and all of their posts
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # if this is my own profile, True
        # if this is somebody else's profile, False
        # status = username == payload["id"]

        user_info = db.pasien.find_one({"username": payload['id']}, {"_id": False})
        return render_template("dashboard.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/login")
def login():
    msg = request.args.get("msg")
    return render_template("login_pasien.html", msg=msg)

@app.route('/login', methods=['POST'])
def login_pasien():
    username_receive = request.form["username"]
    password_receive = request.form["password"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    print(username_receive, pw_hash)
    result = db.pasien.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            "role" : "pasien",
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )

@app.route("/login/registrasi", methods=["GET"])
def registrasi():
    msg = request.args.get("msg")
    return render_template("registrasi_pasien.html", msg=msg)

@app.route('/registrasi', methods=['POST'])
def registrasi_pasien():
    name = request.form['name']
    username = request.form['username']
    address = request.form['address']
    phone = request.form['phone']
    password = request.form['password']
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        "name": name,
        "username": username,
        "address": address,
        "phone": phone,
        "password": pw_hash,
    }
    
    # print(doc)
    db.pasien.insert_one(doc)
    return jsonify({"result": "success"})

@app.route('/pasien/dashboard')
def pasien_page():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']}, {'_id': False})

        if payload['role'] != "pasien":
            return redirect('/dashboard/data_dokter')

        return render_template('halaman_pasien.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
    

@app.route('/dashboard/data_dokter')
def dokter():
    dokters = list(db.dokter.find({}))
    
    for doct in dokters:
        doct['_id'] = str(doct['_id'])
    
    return render_template('data_dokter.html', dokters=dokters)

@app.route('/dashboard/rekam_medis')
def medis():
    return render_template('rekam_medis.html')

@app.route('/dashboard/data_pasien')
def pasien():
    return render_template('data_pasien.html')

@app.route('/dashboard/data_antrian')
def antrian():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']}, {'_id': False})

        if payload['role'] != "admin":
            return redirect('/pasien/dashboard')

        data_antrian = list(db.booking.find({}))
        for data in data_antrian:
            data['pasien'] = db.pasien.find_one({'_id' : data['id_pasien']})
            data['dokter'] = db.dokter.find_one({'_id' : data['id_dokter']})

        print(data_antrian)

        return render_template('data_antrian.html', user_info=user_info, data_antrian=data_antrian)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/pasien/booking')
def booking():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']}, {'_id': False})

        if payload['role'] != "pasien":
            return redirect('/dashboard/data_dokter')

        data_dokter = list(db.dokter.find({}))
        for dokter in data_dokter:
            dokter['_id'] = str(dokter['_id'])

        return render_template('booking.html', user_info=user_info, data_dokter=data_dokter)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))


@app.route('/pasien/riwayat')
def riwayat():
    return render_template('halaman_riwayat_.html')

# @app.route('/user')
# def user():
#     return render_template('user.html')


@app.route('/dokter/tambah', methods=['POST'])
def tambah_dokter():
    nama = request.form['nama']
    spesialis = request.form['spesialis']   
    jadwal = request.form['jadwal']
    foto = request.form['foto']
    
    doc = {
        "nama": nama,
        "spesialis": spesialis,
        "jadwal": jadwal,
        "foto" :foto
    }
    
    db.dokter.insert_one(doc)
    return jsonify({"result": "success"})

@app.route('/dokter/hapus/<id_dokter>')
def hapus_dokter(id_dokter):
    db.dokter.delete_one({'_id' : ObjectId(id_dokter)})
    
    return redirect('/dashboard/data_dokter')

@app.route('/dokter/edit/<id_dokter>', methods=['GET', 'POST'])
def edit_dokter(id_dokter):
    if request.method == 'GET':
        dokter = db.dokter.find_one({'_id' : ObjectId(id_dokter)})
        dokter['_id'] = str(dokter['_id'])  
        
        return render_template('edit_dokter.html', dokter=dokter)
    
    nama = request.form['nama']
    spesialis = request.form['spesialis']   
    jadwal = request.form['jadwal']
    foto = request.form['foto']
    
    db.dokter.update_one({'_id': ObjectId(id_dokter)}, {'$set' : {
        "nama": nama,
        "spesialis": spesialis,
        "jadwal": jadwal,
        "foto" : foto
    }})
    
    return jsonify({"result": "success"})

@app.route('/update_profile', methods=['GET'])
def save_img():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=['HS256']
        )
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        
        new_doc = {
            "profile_name": name_receive, 
            "profile_info": about_receive
            }
        
        if "file_give" in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one(
            {"username": payload["id"]}, 
            {"$set": new_doc}
            )
        return jsonify({
            'result': 'success', 
            'msg': 'Your profile has been updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
    
@app.route('/user/<username>', methods=['GET'])
def user(username):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
             algorithms=['HS256']
        )
        status = username == payload.get('id')  
        user_info = db.users.find_one(
            {'username': username}, 
            {'_id': False}
        )
        return render_template(
            'user.html', 
            user_info=user_info, 
            status=status
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
    


@app.route('/approve_request', methods=['POST'])
def approve_request():
    request_id = ObjectId(request.form['request_id'])
    pet_id = ObjectId(request.form['pet_id'])
    db.admin.update_one({'_id': request_id}, {'$set': {'status': 'approved'}})
    db.pasien.update_one({'_id': pet_id}, {'$set': {'status': True}})
    return redirect(url_for('antrian'))

@app.route('/decline_request', methods=['POST'])
def decline_request():
    request_id = ObjectId(request.form['request_id'])
    db.request_list.update_one({'_id': request_id}, {'$set': {'status': 'declined'}})
    return redirect(url_for('antrian'))

@app.route("/pasien/ulasan", methods=["GET"])
def ulasan_pasien():
    msg = request.args.get("msg")
    return render_template("ulasan_pasien.html", msg=msg)

@app.route("/pasien/ulasan", methods=["GET"])
def tambah_ulasan():
    rating = int(request.form["rating"])
    nama = request.form["nama"]
    ulasan = request.form["ulasan"]

    # Simpan ulasan ke dalam database MongoDB
    ulasan_data = {
        "rating": rating,
        "nama": nama,
        "ulasan": ulasan
    }
    collection.insert_one(ulasan_data)

    return jsonify({"message": "Ulasan berhasil disimpan"})

@app.route("/pasien/ulasan", methods=["GET"])
def get_ulasan():
    ulasan_list = []
    for ulasan in collection.find():
        ulasan_list.append({
            "rating": ulasan["rating"],
            "nama": ulasan["nama"],
            "ulasan": ulasan["ulasan"]
        })

    return jsonify(ulasan_list)


@app.route('/book', methods=['POST'])
def book():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.pasien.find_one({'username': payload['id']})
        print(user_info)

        if payload['role'] != "pasien":
            return redirect('/dashboard/data_dokter')
        
        id_dokter = request.form.get('id_dokter')
        tanggal = request.form.get('tanggal')
        keluhan = request.form.get('keluhan')

        data_count = db.booking.count_documents({})

        doc = {
            "nomor_antrian" : f'A0{data_count+1}',
            "id_pasien" : user_info['_id'],
            "id_dokter" : ObjectId(id_dokter),
            "keluhan" : keluhan,
            "tanggal" : tanggal,
            "status" : 'pending',
            "status_rekam_medis" : False
        }

        db.booking.insert_one(doc)

        return jsonify({'result' : 'success'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)