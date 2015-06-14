from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

from flask_todomvc import settings
from flask_todomvc.extensions import db
from flask_todomvc.models import Todo
from flask_todomvc.todos import bp as todos
import json

app = Flask(__name__, static_url_path='')
app.config.from_object(settings)
app.config.from_envvar('TODO_SETTINGS', silent=True)
app.debug = True

app.register_blueprint(todos)

db.init_app(app)

def init_db():
  with app.app_context():
    db.create_all()

@app.route('/')
def index():
  _todos = Todo.query.all()
  todo_list = map(Todo.to_json, _todos)
  return render_template('index.html', todos=todo_list)

if __name__ == '__main__':
  init_db()
  app.run(port=8000)
