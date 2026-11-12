from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_user_with_email_and_default_role(self):
        user = get_user_model().objects.create_user(
            email="student@example.com",
            password="strong-pass-123",
            first_name="Ada",
            last_name="Lovelace",
        )

        self.assertEqual(user.email, "student@example.com")
        self.assertTrue(user.check_password("strong-pass-123"))
        self.assertEqual(user.role, "student")


class AuthEndpointTests(APITestCase):
    def test_login_returns_tokens_for_existing_user(self):
        user = get_user_model().objects.create_user(
            email="teacher@example.com",
            password="teacher-pass-123",
            first_name="Grace",
            last_name="Hopper",
            role="instructor",
        )

        response = self.client.post(
            reverse("auth_login"),
            {"email": user.email, "password": "teacher-pass-123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
