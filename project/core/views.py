from flask import render_template, Blueprint, request,url_for,redirect
from flask_login import login_user,logout_user,login_required, current_user
from project import db 
from project.models import user
from project.core.forms import LoginForm, SignupForm



core=Blueprint('core',__name__)

@core.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return render_template('index.html')

@core.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form=SignupForm()

    if form.validate_on_submit():
        users=user(email=form.email.data,fullname=form.fullname.data, password=form.password.data)
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('core.login'))

    return render_template('signup.html',form=form)

@core.route('/login' ,methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
        
    form=LoginForm()

    if form.validate_on_submit():

        users=user.query.filter_by(email=form.email.data).first()
        if users.checkPassword(form.password.data) and users is not None:
            login_user(users)

            next=request.args.get('next')
            if next == None or next[0]=='/':
                next=url_for('user.dashboard')
            
            return redirect(next)
        else:
            form.email.errors.append('Email or password must be wrong')

        
    return render_template('login.html',form=form)

@core.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@core.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'),404