from faker import Faker
from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.invitations.models import Invitation


class InvitationAPITest(TestCase):
    """ Test Invitation apis """

    def setUp(self):
        fake = Faker()

        self.client = APIClient()
        self.fake_user = User.objects.create(
            email=fake.ascii_safe_email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.user_name(),
            password=fake.password())
        self.client.force_login(self.fake_user)

    def test_create_invitation(self):
        data = {'email': 'test123@gmail.com'}
        resp = self.client.post('/api/invitations/', data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.get().email, 'test123@gmail.com')

    def test_list_invitation(self):
        data = {'email': 'test123@gmail.com'}
        self.client.post('/api/invitations/', data, format='json')

        resp = self.client.get('/api/invitations/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_patch_invitation(self):
        data = {'email': 'test123@gmail.com'}
        self.client.post('/api/invitations/', data, format='json')

        data = {'email': 'patch_test123@gmail.com', 'used': True}
        id = str(Invitation.objects.get().id)
        resp = self.client.patch(
            '/api/invitations/{id}/'.format(id=id), data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['email'], data['email'])
        self.assertEqual(resp.data['used'], data['used'])

    def test_delete_invitation(self):
        data = {'email': 'test123@gmail.com'}
        self.client.post('/api/invitations/', data, format='json')

        id = str(Invitation.objects.get().id)
        resp = self.client.delete('/api/invitations/{id}/'.format(id=id))

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invitation.objects.count(), 0)
