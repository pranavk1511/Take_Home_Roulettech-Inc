# backend/todo/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Todo

class TodoAPITestCase(APITestCase):
    def setUp(self):
        self.todo1 = Todo.objects.create(title="Test Task 1", description="Test Description 1", completed=False)
        self.todo2 = Todo.objects.create(title="Test Task 2", description="Test Description 2", completed=True)

    def test_list_todos(self):
        url = reverse('todo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_todo(self):
        url = reverse('todo-detail', args=[self.todo1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.todo1.title)

    def test_create_todo(self):
        url = reverse('todo-list')
        data = {
            "title": "New Test Task",
            "description": "New Test Description",
            "completed": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 3)
        self.assertEqual(Todo.objects.get(id=response.data['id']).title, "New Test Task")

    def test_update_todo(self):
        url = reverse('todo-detail', args=[self.todo1.id])
        data = {
            "title": "Updated Test Task",
            "description": "Updated Test Description",
            "completed": True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, "Updated Test Task")

    def test_delete_todo(self):
        url = reverse('todo-detail', args=[self.todo1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 1)
