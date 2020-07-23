from flask import render_template,redirect,url_for,flash,request
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from .. import db
from ..email import mail_message

@auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password', 'danger')
    
    title = "Login | Blog"
    return render_template("auth/login.html", form = form , title = title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))

@auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    title  = "New User"
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        fullname = form.fullname.data
        password = form.password.data
        new_user = User(email = email,username = username, fullname = fullname, password =password)
        new_user.save_user()

        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html',form = form)