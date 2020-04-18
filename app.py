from flask import Flask
import os, sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/toto')
def toto():
    return 'toto'
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

if __name__ == '__main__':
    app.run()
