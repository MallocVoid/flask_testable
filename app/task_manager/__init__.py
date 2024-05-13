from flask import Blueprint

task_manager = Blueprint('task_manager', __name__, url_prefix='/tasks')

from . import routes