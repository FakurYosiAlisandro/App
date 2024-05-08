from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route("/")
def home():
    uploads = sorted(os.listdir(app.config['UPLOAD_PATH']), key=lambda x: os.path.getctime(os.path.join(app.config['UPLOAD_PATH'], x)))
    uploads = ['uploads/' + file for file in uploads]
    uploads.reverse()
    return render_template("home.html", uploads=uploads)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_PATH'], filename)

        # Check if the file already exists and delete it
        existing_file = [fn for fn in os.listdir(app.config['UPLOAD_PATH']) if fn != filename]
        if existing_file:
            os.remove(os.path.join(app.config['UPLOAD_PATH'], existing_file[0]))

        f.save(filepath)
        return redirect(url_for("home"))

@app.route('/static/<path:path>')
def send_static(path):
    return send_file(os.path.join(app.config['UPLOAD_PATH'], path))

if __name__ == "__main__":
    app.config['UPLOAD_PATH'] = 'static/uploads'
    app.run(debug=True)
