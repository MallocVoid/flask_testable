import unittest
from app import create_app, db
from app.task_manager.models import Task
from app.task_manager.services import create_task, retrieve_tasks, retrieve_task, update_task, delete_task
from config import TestingConfig

class ServicesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.task_data = {'title': 'Test Task', 'description': 'Test Description'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_task(self):
        # Arrange
        # Performed in the setUp function

        # Act
        task = create_task(self.task_data)

        # Assert
        self.assertEqual(task['title'], 'Test Task')
        self.assertEqual(task['description'], 'Test Description')

    def test_retrieve_tasks(self):
        # Arrange
        # Performed in the setUp function

        # Act
        create_task(self.task_data)
        tasks = retrieve_tasks()

        # Assert
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, 'Test Task')

    def test_retrieve_task(self):
        # Arrange
        # Performed in the setUp function

        # Act
        task = create_task(self.task_data)
        retrieved_task = retrieve_task(task['id'])

        # Assert
        self.assertEqual(retrieved_task.title, 'Test Task')
        self.assertEqual(retrieved_task.description, 'Test Description')

    def test_update_task(self):
        # Arrange
        # Performed in the setUp function

        # Act
        task = create_task(self.task_data)
        new_data = {'title': 'Updated Task', 'description': 'Updated Description'}
        updated_task = update_task(task['id'], new_data)

        # Assert
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.description, 'Updated Description')

    def test_delete_task(self):
        # Arrange
        # Performed in the setUp function

        # Act
        task = create_task(self.task_data)
        delete_task(task['id'])
        tasks = retrieve_tasks()

        # Assert
        self.assertEqual(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()