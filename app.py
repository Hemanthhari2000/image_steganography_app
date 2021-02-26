from flask import *
import os

import algo as algo

app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
def home():
    if os.path.isfile('static/output.png'):
        os.remove('static/output.png')

    if os.path.isfile('static/input.png'):
        os.remove('static/input.png')

    return render_template('index.html', encoded=False)


@app.route('/upload', methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files['uploadedImage']
        if uploaded_file.filename != '':
            uploaded_file.save('static/input.png')
            data = str(request.form.get('dataEncode'))
            algo.imgEncode(data)
        return render_template('index.html', encoded=True)
    return render_template('upload.html')


@app.route('/decode', methods=["POST", "GET"])
def decode():
    if request.method == "POST":
        uploaded_file = request.files['decodeImage']
        if uploaded_file.filename != "":
            uploaded_file.save('static/output.png')
            data = str(algo.imgDecode())
        return render_template('index.html', encoded=False, decoded=True, data=data)
    return render_template('decode.html')


@app.route('/input_image')
def input_image():
    return send_from_directory('static', 'input.png')


@app.route('/output_image')
def output_image():
    return send_from_directory('static', 'output.png')


@app.route('/download')
def download_files():
    path = 'static/output.png'
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
