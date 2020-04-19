from flask import Flask,render_template,url_for,request,session,redirect,flash

import os, sqlite3
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY']="slqjfhdqildtyaè_tqfék^)à_içfwdgçqe'çt'"



@app.route('/')
def index():
    return render_template("squelette.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST' :
        if request.form['login'] != None and request.form['password']!= None :
            with sqlite3.connect('static/bdd.db') as conn:
                c=conn.cursor()
                c.execute(f"""SELECT id,login,level,lastconn,last10techs FROM 'user'
                WHERE login='{request.form['login']}' AND password='{request.form['password']}';
                """)
                result = c.fetchall()
                if len(result) >1 :
                    session['error_message'] = "Il y a un problème de connexion !"
                    return redirect(url_for('login'))
                elif len(result)==0 :
                    session['error_message'] = "Le couple login/mot de passe n'est pas présent dans la bdd"
                    return redirect(url_for('login'))
                else :
                    for r in result :
                        session['userid'],session['login'],session['userlevel'],session['lastconn'],session['last10techs']=r
                        session.modified = True
            return render_template("squelette.html")
        else :
            session['error_message']="Il y a un problème de connexion !"
            session.modified = True
            return redirect(url_for('login'))
    else :
        if 'login' in session :
            return redirect(url_for('index'))
        else :
            if 'error_message' not in session :
                session['error_message']=''
                session.modified=True
            return render_template('login.html')

@app.route('/logout')
def logout() :
    session.clear()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register() :
    if request.method=='POST' :
        flash(u'Vous êtes bien enregistré !')
        return render_template("login.html")
    else :
        flash(u'Vous êtes bien enregistré !')
        return render_template("register.html")



@app.route('/random')
@app.route('/random/<int:level>')
def randomTechs(level=5) :
    with sqlite3.connect('static/bdd.db') as conn :
        c=conn.cursor()
        request= c.execute(f"SELECT id FROM 'techs' WHERE level>={level}")
        listPossible=[l[0] for l in request]
        numTech=choice(listPossible)
        request= c.execute(f"SELECT name,sound,video, level FROM 'techs' WHERE id={numTech}")
        for r in request :
            name,sound,video,lvl=r
        sound=url_for('static',filename=f'{lvl}Kyu/'+sound)
        video = url_for('static', filename=f'{lvl}Kyu/' + video)
    return render_template('randomTech.html',name=name,sound=sound,video=video,level=level)

if __name__ == '__main__':
    app.run()
