from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CalculationForm
from app.models import User, HistoryRecord
from app.solver import Multiply
import time

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CalculationForm()
    if form.validate_on_submit():
        size     = int(form.size.data)
        if size > 430:
            size = 430
        minnum   = int(form.minnum.data)
        maxnum   = int(form.maxnum.data)
        start    = time.time()
        result   = Multiply(size, minnum, maxnum)
        exectime = round(time.time() - start, 2)
        record   = HistoryRecord(exectime=exectime, result=result, currentuser=current_user)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for("history"))
    return render_template('home.html', title='Home', form=form)

@app.route('/history')
@login_required
def history():
    calcultaion_reqs = current_user.history
    return render_template('history.html', title='History', history=calcultaion_reqs)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
