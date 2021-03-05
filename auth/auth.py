from flask import Blueprint, app, render_template, redirect, request, session, flash, url_for
from .models import User
from database import db_session
# from main import UPLOADS_DIR
from utils import check_image_file, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os

auth = Blueprint("auth", __name__)
UPLOADS_DIR = 'static/media'

@auth.route('/')
def redirect_login():
    return redirect('login')

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        profile = request.files['profile']
        is_valid_image, extenstion = check_image_file(profile.filename)
        if not is_valid_image:
            flash('Upload valid image!!!')
            return redirect('profile')
        image_path = os.path.join(UPLOADS_DIR, '{}.{}'.format(username,extenstion))
        try:
            profile.save(image_path)
        except:
            os.mkdir(os.path.join(os.getcwd(), 'static/media'))
            profile.save(image_path)
        image_path = image_path.replace('static/','')
        user.profile = image_path
        db_session.commit()
        flash('Profile updated!!!')

    return render_template('auth/profile.html', user=user, username=username)

@auth.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']
        old_password = request.form['oldPassword']
        if new_password == '' or confirm_password == '' or old_password == '':
            flash('Please fill up the form!!!')
            return redirect('password')
        if not check_password_hash(user.password, old_password):
            flash('Old password didn\'t match!!!')
            return redirect('password')
        if new_password != confirm_password:
            flash('New password validation failed. Please check if new and confirm password are same or not!!!')
            return redirect('password')
        user.password = generate_password_hash(new_password, 'sha256')
        db_session.commit()
        flash('Password changed!!!')
        return redirect(url_for('index'))

    return render_template('auth/password.html', user=user, username=username)

@auth.route('/pin', methods=['GET', 'POST'])
@login_required
def pin():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        try:
            new_pin = request.form['newPin']
            if len(new_pin) !=4 :
                flash('Pin must be 4 digit!!!')
                return redirect('pin')
            new_pin = int(new_pin)
            confirm_pin = int(request.form['confirmPin'])
            old_pin = int(request.form['oldPin'])
        except:
            flash('Pin must be 4 digit!!!')
            return redirect('pin')
        if user.pin != old_pin:
            flash('Old pin didn\'t match!!!')
            return redirect('pin')
        if new_pin != confirm_pin:
            flash('New pin validation failed. Please check if new and confirm pin are same or not!!!')
            return redirect('pin')
        user.pin = new_pin
        db_session.commit()
        flash('Pin changed!!!')
        return redirect(url_for('index'))

    return render_template('auth/pin.html', user=user, username=username)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # redirect to home page as user is already logged in
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash('Enter Credential!!!')
            return redirect('login')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                session['username'] = username
                flash('Login Successfull!!!')
                return redirect(url_for('index'))
            else:
                flash('Invalid Credential!!!')
                return redirect('login')
        else:
            flash('Invalid Credential!!!')
            return redirect('login')
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pin = request.form['pin']
        profile = request.files['profile']
        if username == '' or password == '' or pin == '' or profile == '':
            flash('Enter Credential!!!')
            return redirect('signup')
        if len(pin) != 4:
            flash('PIN must be 4 digit number')
            return redirect('signup')
        try:
            pin = int(pin)
        except:
            flash('PIN must be 4 digit number')
            return redirect('signup')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken!!!')
            return redirect('signup')
        else:
            is_valid_image, extenstion = check_image_file(profile.filename)
            if not is_valid_image:
                flash('Upload valid image!!!')
                return redirect('signup')
            password = generate_password_hash(password, 'sha256')

            image_path = os.path.join(UPLOADS_DIR, '{}.{}'.format(username,extenstion))
            try:
                profile.save(image_path)
            except:
                os.mkdir(os.path.join(os.getcwd(), 'static/media'))
                profile.save(image_path)
            image_path = image_path.replace('static/','')
            user = User(username=username, password=password, pin=pin, image_path=image_path)
            db_session.add(user)
            db_session.commit()
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('auth/signup.html')

@auth.route('/logout', methods=['GET'])
def logout():
    if 'username' not in session:
        flash('You have already been logged out!!!')
        return redirect('login')
    session.clear()
    flash('You have been logged out!!!')
    return redirect('login')

