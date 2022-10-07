import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def user_data():
    data = {
        'username': 'user',
        'email': 'email@m.com',
        'password': 'pass12345'
    }
    return data


@pytest.fixture
@pytest.mark.django_db
def basic_user(api_client, user_data):
    api_client.post('/api/auth/register/', data=user_data)
    return User.objects.get()


@pytest.fixture
@pytest.mark.django_db
def auth_token(api_client, basic_user, user_data):
    data = user_data.copy()
    del data['email']
    res = api_client.post('/api/auth/login/', data=data)
    return res.data.get('token')
