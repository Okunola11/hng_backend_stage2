from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta, datetime
from organisation.models import Organisation

import pytest
from django.urls import reverse

User = get_user_model()

# || UNIT TEST || UNIT TEST || UNIT TEST || #


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            firstName='Test',
            lastName='User',
            password='password123',
            # phone='1234567890'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = refresh.access_token

    def test_token_generation(self):
        access_token = self.access_token

        # Ensure token contains correct user details
        # I set email as the unique primary key for the token in settings.py
        self.assertEqual(access_token['user_id'], str(self.user.email))
        
        # Token expiration
        access_token_exp = datetime.utcfromtimestamp(access_token['exp'])
       
        expected_expiration_time = datetime.utcnow() + timedelta(minutes=5)

        # Check if the access token expires within the configured time
        assert abs((access_token_exp - expected_expiration_time).total_seconds()) < 5, "Token expiration time is not as expected"
        

    def test_organisation_access(self):
        access_token = self.access_token
        org = Organisation.objects.create(
            orgId='org1',
            name="Test Organisation",
            description="A test organisation"
        )
        org.members.add(self.user)

        # Ensure the user can see their own organisation
        response = self.client.get(f'/api/organisations/{org.orgId}/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)

        # Createing another user
        other_user = User.objects.create_user(
            email='otheruser@example.com',
            firstName='Other',
            lastName='User',
            password='password456',
        )

        # Ensure the other user can't see the organisation
        other_refresh = RefreshToken.for_user(other_user)
        response = self.client.get(f'/api/organisations/{org.orgId}/', HTTP_AUTHORIZATION=f'Bearer {other_refresh.access_token}')
        self.assertEqual(response.status_code, 403)


# || END TO END TEST || END TO END TEST || END TO END TEST || #


@pytest.mark.django_db
class TestAuthEndpoints:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')

    def test_register_user_successfully(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        assert response.status_code == 201
        assert response.data['data']['user']['firstName'] == 'John'
        assert response.data['data']['user']['email'] == 'john.doe@example.com'
        assert 'accessToken' in response.data['data']

        # Verify default organisation
        user = User.objects.get(email='john.doe@example.com')
        access_token = response.data['data']['accessToken']
        org = self.client.get(f'/api/organisations/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        firstOrg = org.data['data']['organisations'][0]
        assert firstOrg['name'] == "John's Organisation"

    def test_login_user_successfully(self):
        user = User.objects.create_user(
            email='loginuser@example.com',
            firstName='Login',
            lastName='User',
            password='password123',
        )
        data = {
            'email': 'loginuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        assert response.status_code == 200
        assert response.data['data']['user']['email'] == 'loginuser@example.com'
        assert 'accessToken' in response.data['data']

    def test_register_missing_fields(self):
        data = {
            'firstName': 'Jane',
            'email': 'jane.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        assert response.status_code == 422
        assert any(error['field'] == 'lastName' for error in response.data['errors'])


    def test_register_duplicate_email(self):
        User.objects.create_user(
            email='duplicate@example.com',
            firstName='Duplicate',
            lastName='User',
            password='password123',
        )
        data = {
            'firstName': 'Duplicate',
            'lastName': 'User',
            'email': 'duplicate@example.com',
            'password': 'password456',
            'phone': '0987654321'
        }
        response = self.client.post(self.register_url, data, format='json')
        assert response.status_code == 422
        assert any(error['field'] == 'email' for error in response.data['errors'])

