from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.tests import PAYLOAD, list_user_endpoint
from users.utils import gen_token


# Create your tests here.
class TestUserAuthenticationApiView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_check_user_verification_status(self):
        """
        Test case for if user is verified or not
        (when user is created, by default is_verified is assigned to False)
        :return:
        """
        # create new user
        post_response = self.client.post(list_user_endpoint, PAYLOAD)
        self.assertFalse(post_response.data['data']['is_verified'])

        pk = post_response.data['data']['id']
        token = gen_token({'id': pk})

        # run verify endpoint and check returned response
        verify_response = self.client.put(reverse('verify_user', kwargs={"token": token}))
        self.assertTrue(verify_response.data['data']['is_verified'])

        # double check with get method
        endpoint = reverse('users:user_details', kwargs={'pk': pk})
        get_response = self.client.get(endpoint)
        self.assertTrue(get_response.data['data']['is_verified'])

    def test_login_view(self):
        """
        Test case for login endpoint

        :return:
        """
        # create a new user
        post_response = self.client.post(list_user_endpoint, PAYLOAD)

        # check return status of login endpoint
        login_payload = {'email': PAYLOAD['email'], 'password': PAYLOAD['password']}
        get_response = self.client.post(reverse('login'), login_payload, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_202_ACCEPTED)

        # check return status contains auth token or not
        token = gen_token({'id': post_response.data['data']['id']})
        self.assertEqual(token, get_response.data['data']['token'])

        # check return status of login endpoint if password is not given
        login_payload = {'email': PAYLOAD['email']}
        get_response = self.client.post(reverse('login'), login_payload, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check return status of login endpoint if email id is not given
        login_payload = {'password': PAYLOAD['password']}
        get_response = self.client.post(reverse('login'), login_payload, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check return status of login endpoint if empty payload is not given
        get_response = self.client.post(reverse('login'), {}, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
