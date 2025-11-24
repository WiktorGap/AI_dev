# 1. Zaktualizuj importy: dodaj send_file
from flask import render_template, request, send_file 
from . import ai_model
from .forms import EnterPhoto
import io
import base64
import os
# from fastai.vision.all import *

current = os.path.dirname(__file__)
model_path_gym = os.path.join(current, 'models_of_ai', 'gym_model.pkl')
#learn = load_learner(model_path_gym)

@ai_model.route('/gym_exercise_photo_rec', methods=['GET', 'POST'])
def gym_exercise_photo_rec():
    form = EnterPhoto()
    uploaded_image = None
    prediction = None

    if form.validate_on_submit():
        file = form.photo.data  
        img_bytes = file.read()  

      
        encoded_img = base64.b64encode(img_bytes).decode('utf-8')
        uploaded_image = encoded_img


    return render_template('ai_mod/gym_exercise_photo_rec.html',
                           form=form,
                           uploaded_image=uploaded_image,
                           prediction=prediction)


@ai_model.route('/download_instruction')
def download_instruction():
   
    path_to_file = os.path.join(current, 'instrukcja.txt')
    
    
    if not os.path.exists(path_to_file):
        return "Błąd: Plik instrukcji nie został znaleziony na serwerze.", 404

    return send_file(
        path_to_file,
        as_attachment=True,             # Wymusza pobieranie
        download_name='how_to_run.txt'  # Nazwa pliku, jaką zobaczy użytkownik przy pobieraniu
    )