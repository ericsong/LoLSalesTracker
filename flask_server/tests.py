# tests.py
import os
import unittest
from os import path 
import json

base_path = path.dirname(path.realpath(__file__))
cfg_path = path.join(base_path, 'config', 'testing.py')
os.environ['TODO_SETTINGS'] = cfg_path

import server

class TodoTestCase(unittest.TestCase):
  def setUp(self):
    self.client = server.app.test_client()
    self.order = 1
    server.init_db()

  def tearDown(self):
    with server.app.app_context():
      server.db.drop_all()

  def create(self, title, completed=False):
    todo = {
      "title": title,
      "order": self.order,
      "completed": completed
    }

    response = self.client.post(
      '/todos/',
      data=json.dumps(todo),
      content_type='application/json')

    created = json.loads(response.data.decode('utf-8'))
    assert 'id' in created
    assert created['title'] == title
    assert created['order'] == self.order
    assert created['completed'] == completed
    self.order += 1

    return created

  def read(self, id):
    response = self.client.get(
      '/todos/%d' % id,
      content_type = 'application/json')
    
    if response.status_code != 200:
      assert response.status_code == 404
      return None

    return json.loads(response.data.decode('utf-8'))

  def test_create(self):
    todo1 = self.create('Pick up kids')
    assert todo1['title'] == 'Pick up kids'
    assert todo1['order'] == 1
    assert not todo1['completed']

    todo2 = self.create(
      'Buy groceries',
      completed=True)
    assert todo2['title'] == 'Buy groceries'
    assert todo2['order'] == 2
    assert todo2['completed']

    assert todo1['id'] != todo2['id']

  def test_read(self):
    todo1 = self.create('Pick up kids')
    todo2 = self.create(
        'Buy groceries', completed=True)

    read1 = self.read(todo1['id'])
    read2 = self.read(todo2['id'])

    assert read1 == todo1
    assert read2 == todo2

    read3 = self.read(todo2['id'] + 1)
    assert read3 is None

  def test_update(self):
    todo = self.create('Pick up kids')
    id = todo['id']

    updates = dict(**todo)
    updates['completed'] = True
    updates['title'] = 'Pick up *all* kids'

    update1_req = self.client.put(
        '/todos/%d' % id,
        data=json.dumps(updates),
        content_type='application/json')
    updated = json.loads(update1_req.data.decode('utf-8'))

    assert updated == updates
    assert self.read(id) == updates

  def test_delete(self):
    todo = self.create('Pick up kids')
    id = todo['id']
    assert self.read(id) == todo

    self.client.delete(
        '/todos/%d' % id)

    assert self.read(id) is None

  def test_config_settings(self):
    config = server.app.config
    assert config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://todomvc_admin:abc123@localhost:5432/todomvctest'
    assert config['TESTING']
    assert config['DEBUG']

if __name__ == '__main__':
  unittest.main()

