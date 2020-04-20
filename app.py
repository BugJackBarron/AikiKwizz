from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager,UserMixin,login_user,login_required,current_user,logout_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, length
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import datetime

from werkzeug import security

import os, sqlite3
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY']="cesttressecret"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///static/bddsqlalchemy.sqlite3'

db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin, db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    level = db.Column(db.Integer, default=6)
    last_10_techs = db.Column(db.Text)
    connected_last = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    def __repr__(self) :
        return f'''Id :{self.id} 
                    login : {self.login}
                    password :{self.password}
                    level : {self.level}
                    last connection :{self.connected_last}'''


class Memory(db.Model) :
    id_user = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key=True)
    id_tech = db.Column(db.Integer,db.ForeignKey('tech.id'), primary_key=True)
    memory_level = db.Column(db.Integer, default=0, nullable=False)
    seen_last = db.Column(db.DateTime,default=datetime.datetime.fromisoformat('2020-01-01'),nullable=False)


class MemoryView(ModelView):#nécessaire pour avoir la vue des clés primaires
    form_columns = ['id_user', 'id_tech', 'memory_level', 'seen_last']


class Tech(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    video = db.Column(db.String(80), unique=True,nullable=False)
    sound = db.Column(db.String(80), unique=True,nullable=False)
    keywords = db.Column(db.Text)
    level = db.Column(db.Integer, nullable=False)


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if current_user.is_authenticated :
            print('auth')
            return current_user.login == 'admin'
        else :
            print('pasauth')
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tech, db.session))
admin.add_view(MemoryView(Memory, db.session))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("squelette.html")


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(login=form.login.data).first()
        if user :
            if security.check_password_hash(user.password, form.password.data ) :
                login_user(user)
                return redirect(url_for('myprofile'))
    return render_template("login.html",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register')
@login_required
def register():
    return render_template("squelette.html")

@app.route('/myprofile')
@login_required
def myprofile():
    return f'{current_user.login} is {current_user.level} Kyu'


if __name__ == '__main__':
    app.run(debug=True)

