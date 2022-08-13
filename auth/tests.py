from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestRegistration(APITestCase):
    def test_register(self):
        """
        Tests that a user can successfully register
        """
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_unique_username(self):
        """
        Tests that a username cannot be repeated
        """
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("username" in response.data)
        self.assertTrue("already exists" in response.data["username"][0])

    def test_register_no_password(self):
        """
        Tests that a user cannot register without providing a password
        """
        data = {
            "username": "testuser",
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username="testuser").exists())


class TestLogin(APITestCase):
    def setUp(self):
        """
        Creates a test user for logging in
        """
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login(self):
        """
        Tests that a user can successfully login
        """
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post("/auth/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.data)
        self.assertEqual(self.test_user, Token.objects.get(key=response.data["token"]).user)

    def test_login_wrong_password(self):
        """
        Tests that a wrong password cannot login
        """
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post("/auth/login", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse("token" in response.data)

    def test_login_wrong_username(self):
        """
        Tests that a wrong username cannot login
        """
        data = {
            "username": "wronguser",
            "password": "testpassword"
        }
        response = self.client.post("/auth/login", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse("token" in response.data)