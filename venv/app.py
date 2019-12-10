from flask import Flask, render_template, request, json
from Classes.stf_reader import STFReader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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


if __name__ == "__main__":
    app.run(debug=True)
