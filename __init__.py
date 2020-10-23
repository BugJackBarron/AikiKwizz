from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager,UserMixin,login_user,login_required,current_user,logout_user
from wtforms import StringField, PasswordField, SubmitField, SelectField,widgets, HiddenField
from wtforms.validators import DataRequired, length, InputRequired, EqualTo
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import datetime

from werkzeug import security

import os, sqlite3
from random import choice

###      CONFIGURATION DE L'APP     ###
app = Flask(__name__)
app.config['SECRET_KEY']="cesttressecret"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///static/bddsqlalchemy.sqlite3'
###________CONFIGURATION DES MODULES_____________###
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


###_________________CLASSES DES TABLES POUR SQLALCHEMY________________________________###
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





class Tech(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    video = db.Column(db.String(80), unique=True,nullable=False)
    sound = db.Column(db.String(80), unique=True,nullable=False)
    keywords = db.Column(db.Text)
    level = db.Column(db.Integer, nullable=False)

###________________FORMULAIRES WTFORMS______________________________###


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    login = StringField('Choisissez un login', validators=[InputRequired(message='Champ requis')])
    password = PasswordField('Choisissez un mot de passe', validators=[InputRequired(message='Champ requis'),length(min = 2 ,max=80,message="Le mote de passe doit avoir une longueur comprise entre 8 et 80 caractères.")])
    check_password = PasswordField('Vérification du mot de passe', validators=[InputRequired(message='Champ requis'),EqualTo('password',message = 'Les mots de passe ne coincident pas !')])
    level = SelectField('Votre grade actuel', choices=[ ('6','Aucun'),
                                                        ('5', '5ème Kyu'),
                                                        ('4', '4ème Kyu'),
                                                        ('3', '3ème Kyu'),
                                                        ('2', '2ème Kyu'),
                                                        ('1', '1er Kyu'),
                                                        ('0', "Grade Dan")],
                        default = 6)

class ValidTechNotConnected(FlaskForm):
    notmemorized = SubmitField('A revoir')
    averagememorized = SubmitField('Connue')
    technumber= HiddenField('techNumber')
    deck = HiddenField('deck')


###____________________MODIFICATIONS DES VUES DE L'ADMIN POUR Flask-Admin_______________________###

class MemoryView(ModelView):#nécessaire pour avoir la vue des clés primaires
    form_columns = ['id_user', 'id_tech', 'memory_level', 'seen_last']

class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if current_user.is_authenticated :
            return current_user.login == 'admin'
        else :
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tech, db.session))
admin.add_view(MemoryView(Memory, db.session))

###__________________LOGIN MANAGER POUR Flask-Login____________________________###

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

###______________________VUES_________________________###

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(login=form.login.data).first()
        if user :
            if security.check_password_hash(user.password, form.password.data ) :
                login_user(user)
                if current_user.login=="admin" :
                    return redirect(url_for('admin.index'))
                else :
                    return redirect(url_for('index'))
            flash(u'La combinaison login/mot de passe est inconnue!')
    return render_template("login.html",form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    print(f"Etat {form.validate_on_submit()}")
    print(form.errors)
    if form.validate_on_submit() :
        user = User.query.filter_by(login=form.login.data).first()
        if user is None:
            user = User(login=form.login.data,
                        password=security.generate_password_hash(form.password.data, method='sha256'),
                        level=int(form.level.data))
            db.session.add(user)
            newuser=User.query.filter_by(login=form.login.data).first()
            techs=Tech.query.all()
            for response in techs :
                memory=Memory(id_user=newuser.id,id_tech=response.id,memory_level=0)
                db.session.add(memory)
            db.session.commit()
            return redirect(url_for('login'))
        else :
            flash(u'Il y a un problème avec l\'inscription !')
            form.login.errors.append('Ce pseudo est déjà pris !')
    return render_template("register.html",form=form)


@app.route('/myprofile')
@login_required
def myprofile():
    return f'{current_user.login} is {current_user.level} Kyu'


@app.route('/addtech')
@login_required
def addtech() :
    pass


@app.route('/gettech')
@app.route('/gettech/<int:techid>')
@login_required
def gettech(techid=0) :
    pass


@app.route('/change_password')
@login_required
def change_password() :
    pass


@app.route('/quizz')
@app.route('/quizz/<int:level>')
def make_quizz(**kwargs) :
    ###Ne pas oublier de changer la ligne ci-dessous pour changer pour les utilisateurs authentifiés !

    if current_user.is_anonymous or current_user.is_authenticated:
        if 'level' in kwargs.keys():
            session['deck'] = make_deck(kyu=[kwargs['level']])
            return redirect(url_for('unregistered_quizz'))
        else :
            return redirect(url_for('index'))
    else :
        return redirect(url_for('myprofile'))



@app.route("/unregistered_quizz/",methods=['GET','POST'])
def unregistered_quizz():
    form = ValidTechNotConnected()
    deck=session.get('deck',None)
    if form.validate_on_submit() :
        deck = [int(t) for t in deck]
        if len(deck)==0 :
            return "a plus"
        if form.averagememorized.data :
              if deck :
                deck.remove(session['tirage'])
                session['memorized']+=1
        tirage = choice(deck)
        tech = Tech.query.filter_by(id=tirage).first()
        return render_template('randomTech.html',tech=tech, form=form)

    else :
        session['memorized']=0
        print(f"Deck : {deck}")
        tirage=choice(deck)
        print(f"Tirage : {tirage} Type : {type(tirage)}")
        session['tirage']=tirage
        tech=Tech.query.filter_by(id = tirage).first()
        print(f"Requete :{tech}")
        print(f"nom : {tech.name}")
        return render_template('randomTech.html',tech=tech,form=form)


def make_deck(**kwargs) :
    current_deck=set()
    if 'kyu' in kwargs.keys() :
        for level in kwargs['kyu'] :
            if current_user.is_authenticated :
                ### A modifier pour prendre en compte la validité de la carte
                cards = Tech.query.filter_by(level=level, ).all()
            else :
                cards = Tech.query.filter_by(level=level).all()
            for card in cards :
                current_deck.add(card.id)
    return list(current_deck)


if __name__ == '__main__':
    app.run()