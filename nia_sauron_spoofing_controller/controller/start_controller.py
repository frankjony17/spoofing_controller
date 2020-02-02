from flask import Blueprint

start = Blueprint('start', __name__)


@start.route('/')
def index():
    return 'Welcome to Spoofing Controller API, read documentation in /docs ' \
           'for further questions.', 200
