from flask import Blueprint

school_news_mod = Blueprint('school_news_mod',__name__)

from . import view