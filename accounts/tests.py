from django.test import TestCase

# Create test cases for the models
from .models import User
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="employer@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            role="employer",
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.user2 = User.objects.create_user(
            email="user@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            role="employee",
        )
        self.user2.set_password("testpassword")
        self.user2.save()
        
    def test_user_str(self):
        self.assertEqual(str(self.user), "Test User")
        self.assertEqual(str(self.user2), "Test User")
    def test_user_creation(self):
        user = User.objects.create_user(
            email="test@xyz.com",           
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            role="employer",
        )
        user.set_password("testpassword")
        user.save()
        
        self.assertEqual(user.email, "test@xyz.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.role, "employer")
        self.assertTrue(user.check_password("testpassword"))
        
    def test_user_email_unique(self):
        User.objects.create_user(
            email="test1@xyz.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            role="employer",
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="test1@xyz.com",
                password="testpassword",
                first_name="Test",  
                last_name="User",
                phone_number="1234567890",
                role="employer",
            )
    
    
