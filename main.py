from flask import Flask, render_template, session, request
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from database import init_db, Base
from auth.auth import auth
from credential.credential import credential
from auth.models import User
from credential.models import Credential
from utils import login_required
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.secret_key = config('SECRET_KEY')
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(credential, url_prefix="/credential")
# app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
ROWS_PER_PAGE = 2

@app.route('/')
@login_required
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    username = session['username']
    user = User.query.filter_by(username=username).first()
    credentials = Credential.query.filter_by(user=user.id)
    pagination = Pagination(page=page, total=credentials.count(), search=False, record_name='credentials', show_single_page=True)
    return render_template('home.html', credentials=credentials, username=username, pagination=pagination)

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=8000, debug=True)
 