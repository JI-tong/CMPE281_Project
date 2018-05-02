from flask import Flask, render_template, url_for, request, session, redirect
# from flask.ext.pymongo import PyMongo
import bcrypt

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'mongologinexample'
# app.config['MONGO_URI'] = 'mongodb://pretty:printed@ds021731.mlab.com:21731/mongologinexample'

#mongo = PyMongo(app)

@app.route('/')
def index():
    if 'uname' in session:
        return 'You are logged in as ' + session['uname']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # users = mongo.db.users
    login_user = users.find_one({'name' : request.form['uname']})

    if login_user:
        if bcrypt.hashpw(request.form['psw'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['uname'] = request.form['uname']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['uname']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['psw'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['uname'], 'password' : hashpass})
            session['uname'] = request.form['uname']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)