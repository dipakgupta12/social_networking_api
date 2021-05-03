from rest_framework.test import APITestCase
from api.posts.models import Post, User
from rest_framework import status
from django.urls import reverse


class UserTest(APITestCase):
    USER_LOGIN_ENDPOINT = "/auth/login/"
    USER_REGISTER_ENDPOINT = "/api/users/"
    USER_DETAIL = {
        "first_name": "John",
        "last_name": "Son",
        "email": "john@gmail.com",
        "password": "123456278",
        "username": "Johnson"
    }

    def setUp(self):
        print("setup")

    def test_user_registation(self):
        print("User registration test - started")
        response = self.client.post(
            self.USER_REGISTER_ENDPOINT, data=self.USER_DETAIL, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data)
        self.assertGreater(response.data["id"], 0)
        print("User registration test - finished")

    def test_user_registation_invalid_email(self):
        print("User registration invalid email test - started")
        user_detail = self.USER_DETAIL
        user_detail["email"] = "anyinvalidemail.com"
        response = self.client.post(
            self.USER_REGISTER_ENDPOINT, data=user_detail, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("User registration invalid email test - finished")

    def test_user_login(self):
        print("User login test - started")

        """ Register a user"""
        response = self.client.post(
            self.USER_REGISTER_ENDPOINT, data=self.USER_DETAIL, format='json')

        """ Login with the user"""
        login_payload = {
            "username": self.USER_DETAIL["username"],
            "password": self.USER_DETAIL["password"]
        }
        response = self.client.post(
            self.USER_LOGIN_ENDPOINT, data=login_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertTrue(response.data["token"])
        print("User login test - finished")


class PostTest(APITestCase):
    POST_ENDPOINT = "/api/posts/"
    USER_LOGIN_ENDPOINT = "/auth/login/"
    USER_REGISTER_ENDPOINT = "/api/users/"
    POST_LIKE_UNLIKE_ENDPOINT = "/api/posts/like_unlike/"
    USER_DETAIL = {
        "first_name": "John",
        "last_name": "Son",
        "email": "john@gmail.com",
        "password": "123456278",
        "username": "Johnson"
    }

    def setUp(self):
        print("setup")
        self.superuser = User.objects.create_superuser('apple', 'admin@123')
        self.client.post(self.USER_REGISTER_ENDPOINT,
                         self.USER_DETAIL, format='json')

        login_payload = {
            "username": self.USER_DETAIL["username"],
            "password": self.USER_DETAIL["password"]
        }
        resp_user_login = self.client.post(
            self.USER_LOGIN_ENDPOINT, login_payload, format='json')
        jwt_token = f"JWT {resp_user_login.data.get('token')}"
        self.client.credentials(HTTP_AUTHORIZATION=jwt_token)

    def test_create_post(self):
        print("Post create test - started")
        post_detail = {
            "title": "My new code example",
            "description": "You can use any of REST framework's test case classes as you would for the regular Django test case classes. The self.client attribute will be an APIClient instance."
        }
        response = self.client.post(
            self.POST_ENDPOINT, data=post_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data)
        self.assertGreater(response.data["id"], 0)
        print("Post create test - finished")

    def test_getall_post(self):
        print("Post getall test - started")

        """Create a post"""
        post_detail = {
            "title": "My new code example 2",
            "description": "You can use any of REST framework's test case classes as you would for the regular Django test case classes. The self.client attribute will be an APIClient instance."
        }
        self.client.post(
            self.POST_ENDPOINT, data=post_detail, format='json')

        """Get all post"""
        response = self.client.get(
            self.POST_ENDPOINT, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        print("Post getall test - finished")

    def test_getone_post(self):
        print("Post getone test - started")

        """ Create a post"""
        post_detail = {
            "title": "My new code example 3",
            "description": "You can use any of REST framework's test case classes as you would for the regular Django test case classes. The self.client attribute will be an APIClient instance."
        }
        response = self.client.post(
            self.POST_ENDPOINT, data=post_detail, format='json')

        """ Get the same post"""
        post_id = response.data.get("id")
        response = self.client.get(
            f"{self.POST_ENDPOINT}{post_id}/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), post_detail.get("title"))
        print("Post getone test - finished")

    def test_like_unlike_post(self):
        print("Post like-unlike test - started")

        """Create a post"""
        post_detail = {
            "title": "My new code example 3",
            "description": "You can use any of REST framework's test case classes as you would for the regular Django test case classes. The self.client attribute will be an APIClient instance."
        }
        response = self.client.post(
            self.POST_ENDPOINT, data=post_detail, format='json')

        post_id = response.data.get("id")

        """Like that post"""
        post_action_detail = {
            "post": post_id,
            "action": "L"  # like
        }
        response = self.client.post(
            self.POST_LIKE_UNLIKE_ENDPOINT, data=post_action_detail, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(response.data["action"], post_action_detail["action"])

        """UnLike the same post"""
        post_action_detail = {
            "post": post_id,
            "action": "UN"  # unlike
        }
        response = self.client.post(
            self.POST_LIKE_UNLIKE_ENDPOINT, data=post_action_detail, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(response.data["action"], post_action_detail["action"])
        self.assertEqual(response.data["post"], post_id)
        print("Post like-unlike test - finished")
