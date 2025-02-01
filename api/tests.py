from django.test import TestCase
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserRegistrationSerializerTests(TestCase):

    def test_validate_email_unique(self):
        User.objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        data = {
            'name': 'Another User',
            'email': 'test@example.com',
            'password': 'testpass456'
        }
        serializer = UserRegisterSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("این ایمیل قبلا ثبت نام شده است", str(context.exception))
