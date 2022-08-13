from typing import Tuple

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Task


def get_user_and_credentials(username: str = "testuser", password: str = "testpassword") -> Tuple[User, str]:
    """
    Create a user and its credentials for testing.
    :return: A tuple of a User and its credentials (string).
    """
    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    return (user, token.key)


def create_test_task(user: User, title: str = "test task", description: str = "test description"):
    return Task.objects.create(user=user, title=title, description=description)


class TestCreate(APITestCase):
    def setUp(self):
        """
        Creates a test user for auth
        """
        user, token = get_user_and_credentials()
        self.test_user = user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_create_ok(self):
        """
        Tests that a user can successfully create a task
        """
        data = {
            "title": "test task",
            "description": "test description",
        }
        response = self.client.post("/todo/tasks", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(title="test task").exists())


class TestRemove(APITestCase):
    def setUp(self):
        """
        Creates a test user for auth
        """
        user, token = get_user_and_credentials()
        self.test_user = user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.test_task = create_test_task(user=self.test_user)
        self.test_task_2 = create_test_task(user=self.test_user)

    def test_remove_ok(self):
        """
        Tests that a user can successfully delete a task
        """
        response = self.client.delete(f"/todo/tasks/{self.test_task.pk}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=self.test_task.pk).exists())

    def test_remove_other_users_task(self):
        """
        Tests that a user cannot delete another user's tasks
        """
        user, token = get_user_and_credentials(username="test user 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.delete(f"/todo/tasks/{self.test_task_2.pk}")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.test_task_2.pk).exists())

class TestUpdate(APITestCase):
    def setUp(self):
        """
        Creates a test user for auth
        """
        user, token = get_user_and_credentials()
        self.test_user = user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.test_task = create_test_task(user=self.test_user)

    def test_update_ok(self):
        """
        Tests that a user can successfully update a task
        """
        data = {
            "completed": True
        }
        response = self.client.patch(f"/todo/tasks/{self.test_task.pk}", data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.test_task.completed,
                            Task.objects.get(pk=self.test_task.pk).completed)

    def test_update_other_users_task(self):
        """
        Tests that a user cannot update another user's tasks
        """
        user, token = get_user_and_credentials(username="test user 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        data = {
            "title": "modified task"
        }
        response = self.client.patch(f"/todo/tasks/{self.test_task.pk}", data)
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(Task.objects.get(pk=self.test_task.pk).title, "modified task")

class TestList(APITestCase):
    def setUp(self):
        """
        Creates a test user for auth
        """
        user, token = get_user_and_credentials()
        self.test_user = user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.tasks = [create_test_task(user=self.test_user, title=f"test task {i}") for i in range(5)]

    def test_list_ok(self):
        """
        Tests that a user can successfully get his tasks list
        """
        response = self.client.get("/todo/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.tasks))

    def test_see_other_user_tasks(self):
        """
        Tests that a user can see only his tasks
        """
        new_user, token = get_user_and_credentials(username="test user 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        create_test_task(user=new_user)

        response = self.client.get("/todo/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

class TestDetail(APITestCase):
    def setUp(self):
        """
        Creates a test user for auth
        """
        user, token = get_user_and_credentials()
        self.test_user = user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.test_task = create_test_task(user=self.test_user)

    def test_detail_ok(self):
        """
        Tests that a user can successfully get a task detail
        """
        response = self.client.get(f"/todo/tasks/{self.test_task.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.test_task.title)

    def test_update_other_users_task(self):
        """
        Tests that a user cannot see another user's tasks
        """
        user, token = get_user_and_credentials(username="test user 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get(f"/todo/tasks/{self.test_task.pk}")
        self.assertEqual(response.status_code, 404)