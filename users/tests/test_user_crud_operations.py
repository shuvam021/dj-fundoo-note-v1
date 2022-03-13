import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.tests import create_user, PAYLOAD, list_user_endpoint


# Create your tests here.
class TestUserApiView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            username='@test_user',
            first_name='test',
            last_name='user',
            email='test_user@project.dev',
            password='test_password',
        )

    def test_user_list_api_view(self):
        """
        Test UserApiView's get() method is working or not

        :return:
        """
        res = self.client.get(list_user_endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['data']), 1)

    def test_user_create_through_api_view_with_success_response(self):
        """
        Test UserApiView's post() is working or not

        :return:
        """
        # Create a new user
        post_response = self.client.post(list_user_endpoint, PAYLOAD, format='json')
        self.assertEqual(post_response.data['data'].get('username'), "@test_user2")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # test updated data
        get_response = self.client.get(list_user_endpoint)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data['data']), 2)
        self.assertEqual(get_response.data['data'][1].get('username'), "@test_user2")

    def test_user_create_with_empty_payload(self):
        """
        Test UserApiView's post()'s response if empty payload is given

        :return:
        """
        res = self.client.post(list_user_endpoint, {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_without_password(self):
        """
        Test UserApiView's post()'s response if password is missing in given payload

        :return:
        """
        PAYLOAD.pop('password')
        res = self.client.post(list_user_endpoint, PAYLOAD, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_without_email_field(self):
        """
        Test UserApiView's post()'s response if email is missing in given payload

        :return:
        """
        PAYLOAD.pop('email')
        res = self.client.post(list_user_endpoint, PAYLOAD, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_details_urls_with_invalid_pk(self):
        """
        Test UserDetailsApiView's get(), put(), delete() response for an invalid user id

        :return:
        """
        user_details_endpoint = reverse('users:user_details', kwargs={'pk': random.randint(1000, 100000)})

        # Test for get()
        get_response = self.client.get(user_details_endpoint)
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_response.data['data'], None)

        # Test for put()
        put_response = self.client.put(user_details_endpoint)
        self.assertEqual(put_response.status_code, 404)
        self.assertEqual(get_response.data['data'], None)

        # Test for delete()
        delete_response = self.client.delete(user_details_endpoint)
        self.assertEqual(delete_response.status_code, 404)
        self.assertEqual(get_response.data['data'], None)

    def test_user_retrieve_method_with_success_response(self):
        """
        Test UserDetailsApiView's get()'s response
        (check if model contains only one user i.e. created by constructors)

        :return:
        """
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 1)

        endpoint = reverse('users:user_details', kwargs={'pk': self.user.id})
        get_response = self.client.get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.data['data']['id'], self.user.id)

    def test_user_update_method_with_success_response(self):
        """
        Test UserDetailsApiView's put()'s response

        :return:
        """
        payload = {"username": '@test_user_01', "first_name": 'test',
                   "last_name": 'user', "email": 'test_user@project.dev', "password": 'test_password'}

        endpoint = reverse('users:user_details', kwargs={'pk': self.user.id})
        get_response = self.client.get(endpoint)
        put_response = self.client.put(endpoint, payload, format='json')

        # test for status code
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_201_CREATED)

        # test if data updated or not
        self.assertNotEqual(get_response.data['data'], put_response.data['data'])
        self.assertEqual(put_response.data['data']['username'], payload.get("username"))

    def test_user_delete_method_with_success_response(self):
        """
        Test UserDetailsApiView's delete()'s response

        :return:
        """
        endpoint = reverse('users:user_details', kwargs={'pk': self.user.id})

        # API call
        delete_response = self.client.delete(endpoint)
        get_response = self.client.get(endpoint)

        # status check
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

        # check get response's data return any value or not
        self.assertEqual(get_response.data['data'], None)

        # check get response's data return any value or not
        self.assertEqual(len(get_user_model().objects.all()), 0)

    def test_hashed_password_stored_in_db(self):
        """
        Test password stored in db is properly hashed

        :return:
        """
        payload = {
            "username": "@test_user2",
            "first_name": "test",
            "last_name": "user_2",
            "email": 'test_user_two@project.dev',
            "password": 'test_password'
        }
        post_response = self.client.post(list_user_endpoint, payload, format='json')
        pk = post_response.data['data']['id']
        user_details_endpoint = reverse('users:user_details', kwargs={'pk': pk})
        user = get_user_model().objects.get(pk=pk)

        # password through post method check
        self.assertNotEqual(user.password, payload['password'])
        self.assertTrue('pbkdf2_sha256$' in user.password)

        # password through put method check
        payload['username'] = '@test_user03'
        self.client.put(user_details_endpoint, payload, format='json')
        get_response = self.client.get(user_details_endpoint)
        # making sure data is updated
        self.assertNotEqual(get_response.data['data']['username'], post_response.data['data']['username'])
        self.assertEqual(get_response.data['data']['username'], payload['username'])

        # password check
        user = get_user_model().objects.get(pk=int(get_response.data['data']['id']))
        self.assertTrue('pbkdf2_sha256$' in user.password)
