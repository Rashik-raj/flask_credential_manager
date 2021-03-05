from functools import wraps
from flask import g, flash, url_for, redirect, request, session
from werkzeug.utils import secure_filename

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be signed in for this page.')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def check_image_file(filename):
    allowed_files = ['png', 'jpeg', 'jpg']
    flag = False
    extention = secure_filename(filename).split('.')[-1]
    if extention in allowed_files:
        flag = True
    return flag, extention
