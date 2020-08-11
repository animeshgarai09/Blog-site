import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



app=Flask(__name__)
app.config['SECRET_KEY']='BlogIT-project'

#####################################
########## DATABASE SETUP ###########
#####################################

basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)


#####################################
####### LOGIN MANAGER SETUP #########
#####################################

loginManager= LoginManager()
loginManager.init_app(app)
loginManager.login_view='core.login'

from project.core.views import core
from project.user.views import user
from project.blogpost.views import blogpost
app.register_blueprint(core)
app.register_blueprint(user)
app.register_blueprint(blogpost)
