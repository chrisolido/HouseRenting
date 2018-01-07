from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from users.models import *


def create_superuser():
    """
    Creates and retuns a superuser - instance of settings.MONGOENGINE_USER_DOCUMENT
    """
    new_admin = User(
        username="admin@example.com",
        email="2606449422@qq.com", #Small Circle's email
        name="admin",
        is_active=True,
        is_staff=True,
        is_superuser=True,
        phone="06787654"
    )
    new_admin.set_password('foobar')
    new_admin.save()
    return new_admin


def create_user():
    """
    Creates and returns a regular user - object of settings.MONGOENGINE_USER_DOCUMENT
    """
    new_user = User(
        username="user@example.com",
        email="2606449422@qq.com", #Small Circle's email
        name="user",
        is_active=True,
        is_staff=True,
        is_superuser=True,
        phone="06787654"
    )
    new_user.set_password('foobar')
    new_user.save()
    # print(new_user)
    return new_user


# class ObtainAuthTokenTestCase(APITestCase):
#     def setUp(self):
#         User.drop_collection()
#         Token.drop_collection()
#         self.new_user = create_user()
#         self.url = reverse("api:auth")
#
#     def doCleanups(self):
#         print(User.objects.all())
#         User.drop_collection()
#
#     def test_post_correct_credentials(self):
#         c = APIClient()
#
#         response = c.post(self.url, {"username": "user@example.com", "password": "foobar"})
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertRegexpMatches(response.content.decode('UTF-8'), r'{"token":"\S+"}')
#
#         token = Token.objects.get(user=self.new_user)
#         self.assertRegexpMatches(token.key, "\S+")
#
#     def test_post_incorrect_credentials(self):
#         c = APIClient()
#
#         response = c.post(self.url, {"username": "user@example.com", "password": ""})
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        User.drop_collection()
        Token.drop_collection()
        self.new_user = create_superuser()
        self.url = reverse("api:user-list")
        self.auth_header = 'Token 2c7e9e9465e917dcd34e620193ed2a7447140e5b'

        Token.objects.create(key='2c7e9e9465e917dcd34e620193ed2a7447140e5b', user=self.new_user)

    def doCleanups(self):
        print(User.objects.all())
        print(Token.objects.all())
        # User.drop_collection()
        # Token.drop_collection()

    def test_get_unauthorized(self):
        User.drop_collection()
        Token.drop_collection()
        c = APIClient()

        response = c.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_authorized(self):
        c = APIClient()

        response = c.get(self.url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_username(self):
        for user in User.objects.all():
           print("username is "+user.username)
