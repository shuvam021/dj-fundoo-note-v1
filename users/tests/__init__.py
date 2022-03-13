from django.contrib.auth import get_user_model
from django.urls import reverse

list_user_endpoint = reverse('users:user')
PAYLOAD = {
    "username": "@test_user2",
    "first_name": "test",
    "last_name": "user_2",
    "email": 'test_user_two@project.dev',
    "password": 'test_password'
}


def create_user(**params):
    return get_user_model().objects.create_user(**params)
