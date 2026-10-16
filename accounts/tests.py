from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_user_registration_successful(self):
        """
        Test that a user can register successfully with valid data
        """
        url = reverse('register')
        
        registration_data = {
            "first_name": "Festus",
            "username": "festus",
            "email": "adelekanf7@gmail.com",
            "password": "pointbridge12",
            "password2": "pointbridge12",
        }
        
        response = self.client.post(url, registration_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)