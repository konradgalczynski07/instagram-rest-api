from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_sample_user(email='test@test.com',
                       username='test',
                       password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, username, password)


class ModelTest(TestCase):

    def test_create_user_with_email_and_username(self):
        """Test creating a new user with an email and username successfully"""
        email = 'test@test.com'
        username = 'test'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_username_is_lowercase(self):
        """Test the username for a new user is in lowercase"""
        username = 'TEST'
        user = create_sample_user(username=username)

        self.assertEqual(user.username, username.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            create_sample_user(email=None)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TEST.COM'
        user = create_sample_user(email=email)

        self.assertEqual(user.email, email.lower())

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@test.com',
            'admin',
            'testpass'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @patch('uuid.uuid4')
    def test_profile_pic_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
