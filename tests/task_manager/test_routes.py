import json
import unittest
from unittest.mock import patch
from flask_testing import TestCase
from flask import jsonify
from app import create_app, db
from config import TestingConfig
from app.task_manager.models import Task

class TestRoutes(TestCase):
    def create_app(self):
        return create_app(TestingConfig)
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            task1 = Task(title='Test Task 1', description='Test Description 1')
            task2 = Task(title='Test Task 2', description='Test Description 2')
            db.session.add(task1)
            db.session.add(task2)
            db.session.commit()
            self.task1_id = task1.id
            self.task2_id = task2.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_task_creation(self):
        with self.app.app_context():
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()

            self.assertEqual(task.title, 'Test Task')
            self.assertEqual(task.description, 'Test Description')

    # Alternate test for creating a task 
    # using a mock for the create_task function return value
    @patch('app.task_manager.routes.create_task')
    def test_create_task(self, mock_create_task):
        # Arrange
        mock_retval = {
            'id': 1,
            'title': 'Test task',
            'description': 'This is a test task'
        }
        mock_create_task.return_value = mock_retval

        # Act
        input_data = {
            'title': 'Test task',
            'description': 'This is a test task'
        }
        response = self.client.post('/tasks/', data=json.dumps(input_data), content_type='application/json')

        # Assert
        mock_create_task.assert_called_once_with(input_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), mock_retval)

    def test_retrieve_all(self):
        # Arrange
        # Performed in the setUp function

        # Act
        response = self.client.get('/tasks/')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_retrieve(self):
        # Arrange
        # Performed in the setUp function

        # Act
        response = self.client.get(f'/tasks/{self.task1_id}')
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Test Task 1')
        self.assertEqual(data['description'], 'Test Description 1')

    def test_update(self):
        # Arrange
        new_data = {'title': 'Updated Task', 'description': 'Updated Description'}
        
        # Act
        response = self.client.put(f'/tasks/{self.task1_id}', data=json.dumps(new_data), content_type='application/json')
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Updated Task')
        self.assertEqual(data['description'], 'Updated Description')

    @patch('app.task_manager.routes.delete_task')
    def test_delete(self, mock_delete_task):
        # Arrange
        task_id = 1
        mock_delete_task.return_value = None

        # Act
        response = self.client.delete(f'/tasks/{task_id}')

        # Assert
        mock_delete_task.assert_called()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Task deleted'})
        
if __name__ == '__main__':
    unittest.main()