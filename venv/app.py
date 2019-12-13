from flask import Flask, render_template, request, json, session, redirect
from flask_session import Session
from flask_redis import FlaskRedis
from Classes.stf_reader import STFReader
from Classes.session import SRSession

sesh = SRSession()

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if the user is logged in - if not, redirect to login page
    loggedin = sesh.get('somekey')
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
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
