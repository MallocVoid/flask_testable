from flask import request, jsonify
from . import task_manager
from .services import create_task, retrieve_tasks, retrieve_task, update_task, delete_task
from .models import Task

@task_manager.route('/', methods=['POST'])
def create():
    data = request.json
    task = create_task(data)
    return jsonify(task), 201

@task_manager.route('/', methods=['GET'])
def retrieve_all():
    tasks = retrieve_tasks()
    return jsonify([task.to_json() for task in tasks]), 200

@task_manager.route('/<task_id>', methods=['GET'])
def retrieve(task_id):
    task = retrieve_task(task_id)
    if task:
        return task.to_json(), 200
    return jsonify({'message': 'Task not found'}), 404

@task_manager.route('/<task_id>', methods=['PUT'])
def update(task_id):
    data = request.json
    task = update_task(task_id, data)
    if task:
        return task.to_json(), 200
    return jsonify({'message': 'Task not found'}), 404

@task_manager.route('/<task_id>', methods=['DELETE'])
def delete(task_id):
    delete_task(task_id)
    return jsonify({'message': 'Task deleted'}), 200