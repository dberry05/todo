#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template, session
import sqlite3
import json
import db_lib as db  # library of custom database functions
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
import os

##############################################################################################
# List all tasks
# curl -i http://localhost:5000/todo/api/v1.0/tasks/all

# List open tasks
# curl -i http://localhost:5000/todo/api/v1.0/tasks

# List types
# curl -i http://localhost:5000/todo/api/v1.0/types

# read a task
# curl -i http://localhost:5000/todo/api/v1.0/tasks/2

# read a task
# curl -i http://localhost:5000/todo/api/v1.0/tasks/computer'

# add a task
# curl -i  -X POST -d "{\"item\":\"Read a book\", \"type\":\"computer\"}" -H "Content-Type: application/json" http://localhost:5000/todo/api/v1.0/tasks

# Update a task
#  curl -i -X PUT -d "{\"done\":true}" -H "Content-Type: application/json" http://localhost:5000/todo/api/v1.0/tasks/2

# curl -i -X PUT -d  "{ \"item\":\"Go to bed early\", \"status\":\"closed\"}" -H "Content-Type: application/json" http://localhost:5000/todo/api/v1.0/tasks/562

# delete a task
# curl -i -X DELETE http://localhost:5000/todo/api/v1.0/tasks/2

##############################################################################################


##############################################################################################
app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/todo/api/v1.0/tasks/all', methods=['GET'])
def get_all_tasks():
    tasks = db.get_all_tasks()
    return jsonify({'tasks': tasks})

@app.route('/print.html', methods=['GET'])
def get_print():
    return render_template('print.html')

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_regular_tasks()
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/types', methods=['GET'])
def get_types():
    types = db.get_types()
    return jsonify({'types': types})


@app.route('/todo/api/v1.0/tasks/<type_name>', methods=['GET'])
def get_tasks_by_type(type_name):
    tasks = db.get_tasks_by_type(type_name)
    print(tasks)
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = db.get_active_tasks()
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# @auth.login_required
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'item' or not 'type' in request.json:
        abort(400)
    task = {
        'id': None,
        'date_opened': datetime.now(),
        'item': request.json['item'],
        'status': 'open',
        'type': request.json['type']
    }
    db.create_task(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = db.get_active_tasks()

    #task = filter(lambda t: t['id'] == task_id, tasks)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
        
    if not request.json:
        abort(400)
    if 'item' in request.json and type(request.json['item']) != str:
        abort(400)
    if 'type' in request.json and type(request.json['type']) is not str:
        abort(400)
    if 'status' in request.json and type(request.json['status']) is not str:
        abort(400)
    task[0]['item'] = request.json.get('item', task[0]['item'])
    task[0]['type'] = request.json.get('type', task[0]['type'])
    task[0]['status'] = request.json.get('status', task[0]['status'])
    task[0]['date_closed'] = None
    db.update_task(task[0])
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=80)
