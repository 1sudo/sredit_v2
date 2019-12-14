from flask import Flask, render_template, request, json, session, redirect
from flask_session import Session
from flask_redis import FlaskRedis
from Classes.stf_reader import STFReader
from Classes.session import SRSession
from Classes.db import Query
from var_dump import var_dump


sesh = SRSession()

app = Flask(__name__)

SESSION_TYPE = 'redis'
SESSION_PERMANENT = False
app.config.from_object(__name__)
Session(app)

qm = Query

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if the user is logged in - if not, redirect to login page
    loggedin = sesh.get('username')
    if loggedin == 'no':
        return redirect('/login', code=302)
    else:
        if request.method == 'POST':
            length = request.content_length
            if length > 50000000:
                return "Uploaded STF files should be less than 50MB!"
            else:
                file = request.files.get('contents')
                contents = file.read(length)
                reader = STFReader()
                stf_data = reader.read_stf(contents)
                return render_template('index.html', stf_data=stf_data)
        else:
            return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        errors = []
        params = {}
        params['username'] = request.form.get('username')
        params['password'] = request.form.get('password')

        account = qm.get_account("", params['username'])

        if hasattr(account, 'username'):
            hash = qm.get_hash("", params['password'], account.salt)
            if account.password == hash:
                sesh.set('id', account.id)
                sesh.set('project_name', account.project_name)
                sesh.set('username', account.username)
                sesh.set('admin_level', account.admin_level)
                return redirect('/', code=302)
            else:
                errors.append('Password incorrect!')
                return render_template('login.html', errors=errors)
        else:
            errors.append('Username does not exist!')
            return render_template('login.html', errors=errors)

        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        errors = []
        params = {}
        params['project_name'] = request.form.get('project_name')
        params['email'] = request.form.get('email')
        params['username'] = request.form.get('username')
        params['password'] = request.form.get('password')
        params['password_confirm'] = request.form.get('password_confirm')

        email_check = qm.check_email("", params['email'])
        username_check = qm.check_username("", params['username'])

        if params['password'] != params['password_confirm']:
            errors.append('Passwords do not match!')
            return render_template('register.html', errors=errors)
        elif email_check == "found":
            errors.append('Email address exists!')
            return render_template('register.html', errors=errors)
        elif username_check == "found":
            errors.append('Username exists!')
            return render_template('register.html', errors=errors)
        else:
            qm.create_account("", params)
            sesh.set('project_name', params['project_name'])
            sesh.set('username', params['username'])
            sesh.set('admin_level', 0)
            return redirect('/', code=302)
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    sesh.set('project_name', 'null')
    sesh.set('username', 'no')
    sesh.set('admin_level', 0)
    return redirect('/login', code=302)


if __name__ == "__main__":
    app.run(debug=True)
