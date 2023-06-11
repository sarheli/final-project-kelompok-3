from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Periksa data login yang dikirim dari form
        username = request.form['username']
        password = request.form['password']

        # Lakukan validasi login sesuai kebutuhan Anda
        if username == 'admin' and password == '12345':
            # Jika login berhasil, alihkan ke halaman sukses atau halaman lainnya
            return redirect('/success')
        else:
            # Jika login gagal, tampilkan pesan error atau alihkan kembali ke halaman login
            error_message = 'Username atau password salah. Silakan coba lagi.'
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/super-admin/login')
def login_admin():
    return render_template('login_admin.html')
    

@app.route('/pasien/login')
def login_pasien():
    return render_template('login_pasien.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)
