from .models import Task
from app.database import db

def create_task(data):
    task = Task(title=data['title'], description=data['description'])

    db.session.add(task)
    db.session.commit()
    return task.to_json()

def retrieve_tasks():
    return Task.query.all()

def retrieve_task(task_id):
    return db.session.get(Task, task_id)

def update_task(task_id, data):
    task = db.session.get(Task, task_id)
    if task:
        task.title = data['title']
        task.description = data['description']
        db.session.commit()
    return task

def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        