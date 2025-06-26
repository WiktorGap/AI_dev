from flask import Blueprint

ai_model = Blueprint('ai_model',__name__)

from . import views