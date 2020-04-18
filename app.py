from flask import Flask,render_template,url_for
import os, sqlite3
from random import choice

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/random/<int:level>')
def randomTechs(level) :
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
    return render_template('randomTech.html',name=name,sound=sound,video=video)

if __name__ == '__main__':
    app.run()
