from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm

User = get_user_model()


class CustomUserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
           email='test@example.com',
           name='Test User',
           password='testpassword123' 
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
           email='admin@example.com',
           name='Admin User',
           password='adminpassword123' 
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.name, 'Admin User')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                name='Test User',
                password='testpassword123'
            )
    
    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                name='Admin User',
                password='adminpassword123',
                is_staff=False
            )
    
    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                name='Admin User',
                password='adminpassword123',
                is_superuser=False 
            )


class CustomUserFormTests(TestCase):

    def test_user_creation_form(self):
        form_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_invalid(self):
        form_data = {
            'email': 'invalid-email',
            'name': '',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class CustomUserSignalTest(TestCase):
    def test_is_staff_updated_on_save(self):
        user = User(
                email='admin@example.com',
                name='Admin User',
                password='adminpassword123',
                is_superuser=True
            )
        self.assertFalse(user.is_staff)
        user.save()
        user.refresh_from_db()
        self.assertTrue(user.is_staff)