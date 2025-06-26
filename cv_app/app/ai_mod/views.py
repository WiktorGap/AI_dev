from flask import render_template, request
from . import ai_model
from .forms import EnterPhoto
import io
import base64
import os
from fastai.vision.all import *


current = os.path.dirname(__file__)
model_path_gym = os.path.join(current, 'models_of_ai', 'gym_model.pkl')
learn = load_learner(model_path_gym)

@ai_model.route('/gym_exercise_photo_rec', methods=['GET', 'POST'])
def gym_exercise_photo_rec():
    form = EnterPhoto()
    uploaded_image = None
    prediction = None

    if form.validate_on_submit():
        file = form.photo.data  
        img_bytes = file.read()  

        
        img = PILImage.create(io.BytesIO(img_bytes))
        pred_labels, pred_tensor, pred_probs = learn.predict(img)


        encoded_img = base64.b64encode(img_bytes).decode('utf-8')
        uploaded_image = encoded_img

        top_idxs = pred_probs.argsort(descending=True)[:2]
        top_labels = [learn.dls.vocab[i] for i in top_idxs]
        prediction = ", ".join(top_labels)

    return render_template('ai_mod/gym_exercise_photo_rec.html',
                           form=form,
                           uploaded_image=uploaded_image,
                           prediction=prediction)
