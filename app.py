from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
