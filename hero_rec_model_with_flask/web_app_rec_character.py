from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from fastai.vision.all import *
import os

current_path = os.getcwd()
model_path = os.path.join(current_path, 'character_rec_model.pkl')


UPLOAD_FOLDER = os.path.join(current_path, 'static', 'upload_folder')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

learn = load_learner(model_path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    isUploaded = False
    file_url = None
    prediction = None

    if request.method == 'POST':
        file = request.files.get('fileToUpload')
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            isUploaded = True

            prediction = learn.predict(filepath)

            
            file_url = url_for('static', filename=f'upload_folder/{filename}')

    return render_template("upload.html", uploaded=isUploaded, path=file_url, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
