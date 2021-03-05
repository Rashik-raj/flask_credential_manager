from flask import Blueprint, app, render_template, redirect, request, session, flash, url_for
from sqlalchemy.sql import expression
from .models import Credential, User
from database import db_session
from utils import login_required
# from main import UPLOADS_DIR
from werkzeug.security import generate_password_hash, check_password_hash
import os

credential = Blueprint("credential", __name__)

@credential.route('/')
def redirect_home():
    return redirect(url_for('index'))

@credential.route('/add', methods=['POST'])
@login_required
def add():
    if request.method == 'POST':
        username = session['username']
        user = User.query.filter_by(username=username).first()
        url = request.form['url']
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if url == '' or name == '' or username == '' or password == '':
            flash('Please fill up the form!!!')
            return redirect(url_for('index'))
        credential = Credential(user.id, url, name, username, password)
        db_session.add(credential)
        db_session.commit()
    return redirect(url_for('index'))

@credential.route('/edit', methods=['POST'])
@login_required
def edit():
    if request.method == 'POST':
        session_username = session['username']
        credential_id = request.form['editCredentialId']
        url = request.form['editUrl']
        name = request.form['editName']
        username = request.form['editUsername']
        password = request.form['editPassword']
        try:
            pin = int(request.form['editPin'])
        except:
            flash('Pin must be 4 digit number!!!')
            return redirect(url_for('index'))
        if credential_id == '' or url == '' or name == '' or username == '' or password == '':
            flash('Please fill up the form!!!')
            return redirect(url_for('index'))
        credential = Credential.query.filter_by(id=credential_id).first()
        user = User.query.filter_by(id=credential.user).first()
        if user.username != session_username:
            flash('You don\'t have permission to edit other\'s credential!!!')
            return redirect(url_for('index'))
        if user.pin != pin:
            flash('Pin mis-matched!!!')
            return redirect(url_for('index'))
        credential.url = url
        credential.name = name
        credential.username = username
        credential.password = password
        db_session.commit()
    return redirect(url_for('index'))

@credential.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    username = session['username']
    credential = Credential.query.filter_by(id=id).first()
    user = User.query.filter_by(id=credential.user).first()
    if user.username != username:
        flash('You don\'t have permission to delete other\'s credential!!!')
        return redirect(url_for('index'))
    db_session.delete(credential)
    db_session.commit()
    flash('Credential deleted successfully!!!')
    return redirect(url_for('index'))