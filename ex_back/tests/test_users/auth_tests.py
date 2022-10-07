import pytest
from typing import TYPE_CHECKING
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


if TYPE_CHECKING:
    from rest_framework.test import APIClient
    from users.models import User, UserManager


class TestRegistration:
    """Tests for user registration api via credentials."""
    endpoint = '/api/auth/register/'
    User = get_user_model()

    @pytest.mark.django_db
    def test_email_username(self,
                            api_client: 'APIClient',
                            user_data):
        """Test user's creation with provided email, username and password.
        User's token and profile must be also created.
        """
        res = api_client.post(self.endpoint, data=user_data)

        assert res.status_code == 201

        user = self.User.objects.get()
        assert self.User.objects.count() == 1
        assert user is not None
        assert user.username == user_data.get('username')
        assert user.email == user_data.get('email')

        token = Token.objects.get(user=user)
        assert Token.objects.count() == 1
        assert token is not None
        assert token.key == res.data['token']

    @pytest.mark.django_db
    def test_username(self,
                      api_client: 'APIClient',
                      user_data):
        """Test user's creation with provided username and password.
        User's token and profile must be also created.
        """
        del user_data['email']
        res = api_client.post(self.endpoint, data=user_data)

        assert res.status_code == 201

        user = self.User.objects.get()
        assert self.User.objects.count() == 1
        assert user is not None
        assert user.username == user_data['username']
        assert user.email is None

        token = Token.objects.get(user=user)
        assert Token.objects.count() == 1
        assert token is not None
        assert token.key == res.data.get('token')

    @pytest.mark.django_db
    def test_email(self,
                   api_client: 'APIClient',
                   user_data):
        """Test user's creation with provided email and password.
        User's token and profile must be also created.
        """
        del user_data['username']
        res = api_client.post(self.endpoint, data=user_data)

        assert res.status_code == 201

        user = self.User.objects.get()
        assert self.User.objects.count() == 1
        assert user is not None
        assert user.email == user_data['email']
        assert user.username is None

        token = Token.objects.get(user=user)
        assert Token.objects.count() == 1
        assert token is not None
        assert token.key == res.data['token']

    @pytest.mark.django_db
    def test_fail_nickname(self, api_client: 'APIClient', user_data):
        """Test registration fails with only password given.
        """
        del user_data['username']
        del user_data['email']
        res = api_client.post(self.endpoint, data=user_data)
        assert res.status_code == 400
        assert self.User.objects.count() == 0
        assert Token.objects.count() == 0

    @pytest.mark.django_db
    def test_fail_password(self, api_client: 'APIClient', user_data):
        """Test registration fails without password given.
        """
        del user_data['password']
        res = api_client.post(self.endpoint, data=user_data)
        assert res.status_code == 400
        assert self.User.objects.count() == 0
        assert Token.objects.count() == 0

    @pytest.mark.django_db
    def test_fail_duplicate_username(self, api_client: 'APIClient', basic_user, user_data):
        """Test duplicate username registration fail.
        """
        del user_data['email']
        res = api_client.post(self.endpoint, data=user_data)
        assert res.status_code == 400

        assert self.User.objects.count() == 1
        assert Token.objects.count() == 1

    @pytest.mark.django_db
    def test_fail_duplicate_email(self, api_client: 'APIClient', basic_user, user_data):
        """Test duplicate email registration fail.
        """
        del user_data['username']
        res = api_client.post(self.endpoint, data=user_data)
        assert res.status_code == 400

        assert self.User.objects.count() == 1
        assert Token.objects.count() == 1


class TestLogin:
    """Tests for user logging in via credentials."""
    endpoint = '/api/auth/login/'
    User = get_user_model()

    # TODO TOKEN CHECK
    @pytest.mark.django_db
    def test_username(self, api_client, basic_user, user_data):
        """Test login with only username and password given."""
        data = {
            'username': user_data['username'],
            'password': user_data['password']
        }
        res = api_client.post(self.endpoint, data=data)
        assert res.status_code == 200

        token = res.data.get('token')
        assert token is not None

    @pytest.mark.django_db
    def test_email(self, api_client, basic_user, user_data):
        """Test login with only email and password given."""
        data = {
            'username': user_data['email'],
            'password': user_data['password']
        }
        res = api_client.post(self.endpoint, data=data)
        assert res.status_code == 200

        token = res.data.get('token')
        assert token is not None

    @pytest.mark.django_db
    def test_username_fail(self, api_client, basic_user, user_data):
        """Test login with wrong username fail."""
        data = {
            'username': 'wrong_username',
            'password': user_data['password']
        }
        res = api_client.post(self.endpoint, data=data)
        assert res.status_code == 400

    @pytest.mark.django_db
    def test_password_fail(self, api_client, basic_user, user_data):
        """Test login with wrong password fail."""
        data = {
            'username': user_data['username'],
            'password': 'wrong_password'
        }
        res = api_client.post(self.endpoint, data=data)
        assert res.status_code == 400


class TestLogout:
    """Testing logging out with auth token."""
    endpoint = '/api/auth/logout/'
    User = get_user_model()

    @pytest.mark.django_db
    def test_logout(self, api_client: 'APIClient', auth_token):
        """Test successfull logging out with right credentials."""
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        res = api_client.post(self.endpoint)
        assert res.status_code == 200

        assert Token.objects.count() == 0

    @pytest.mark.django_db
    def test_bad_credentials(self, api_client: 'APIClient', basic_user):
        """Testing wrong credentials failure."""
        api_client.credentials(HTTP_AUTHORIZATION=f'Token bad_token')
        res = api_client.post(self.endpoint)
        assert res.status_code == 401

        assert Token.objects.count() == 1


class TestUpdateUser:
    endpoint = '/api/auth/update-user/'
    User = get_user_model()

    @pytest.mark.django_db
    def test_core_data(self, api_client: 'APIClient',
                       basic_user, auth_token,
                       user_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        new_data = {
                'username': 'new_username',
                'email': 'new_email@m.com',
                'password': user_data.get('password')
        }

        res = api_client.patch(self.endpoint, data=new_data, format='json')
        assert res.status_code == 200

        assert self.User.objects.count() == 1

        user = self.User.objects.get()
        assert user.username == new_data.get('username')
        assert user.email == new_data.get('email')

    @pytest.mark.django_db
    def test_profile_data(self, api_client: 'APIClient',
                          basic_user, auth_token,
                          user_data):

        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        new_data = {
                'password': user_data.get('password')
        }

        res = api_client.patch(self.endpoint, data=new_data, format='json')
        assert res.status_code == 200

    @pytest.mark.django_db
    def test_password_fail(self, api_client: 'APIClient',
                           basic_user, auth_token,
                           user_data):

        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        new_data = {
                'username': 'new_username',
                'email': 'new_email@m.com',
                'password': 'wrong_password'
        }

        res = api_client.patch(self.endpoint, data=new_data, format='json')
        assert res.status_code == 400

        assert self.User.objects.count() == 1

        user = self.User.objects.get()
        assert user.username == user_data['username']
        assert user.email == user_data['email']

    @pytest.mark.django_db
    def test_unautharized(self, api_client: 'APIClient', basic_user, user_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token wrong_token')
        new_data = {
                'username': 'new_username',
                'email': 'new_email@m.com',
                'password': user_data.get('password')
        }

        res = api_client.patch(self.endpoint, data=new_data, format='json')
        assert res.status_code == 401

        assert self.User.objects.count() == 1

        user = self.User.objects.get()
        assert user.username == user_data['username']
        assert user.email == user_data['email']


class TestUpdatePassword:
    endpoint = '/api/auth/update-password/'
    User = get_user_model()

    @pytest.mark.django_db
    def test_success(self, api_client: 'APIClient',
                     auth_token,
                     basic_user, user_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        new_data = {
            'old_password': user_data.get('password'),
            'new_password': 'zxcvbnqwerty'
        }

        res = api_client.post(self.endpoint, data=new_data)
        assert res.status_code == 200
        assert self.User.objects.get().check_password(
            new_data['new_password']) is True

    @pytest.mark.django_db
    def test_wrong_old_password(self, api_client: 'APIClient',
                                auth_token,
                                basic_user, user_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        new_data = {
            'old_password': 'wrong_password',
            'new_password': 'zxcvbnqwerty'
        }

        res = api_client.post(self.endpoint, data=new_data)
        assert res.status_code == 400
        assert self.User.objects.get().check_password(
            new_data['new_password']) is False

    @pytest.mark.django_db
    def test_weak_password(self, api_client: 'APIClient',
                           auth_token,
                           basic_user, user_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        new_data = {
            'old_password': 'wrong_password',
            'new_password': '123qwe'
        }

        res = api_client.post(self.endpoint, data=new_data)
        assert res.status_code == 400
        assert self.User.objects.get().check_password(
            new_data['new_password']) is False
