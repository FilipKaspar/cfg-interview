from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from bonds.enums import InterestFrequencyChoices


class BondAPITests(APITestCase):
    url = "/api/bonds/"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.default_payload = {
            "issuer": "Test Issuer",
            "isin": "CZ0003569816",
            "face_value": 256,
            "bond_rate": 5.5,
            "date_bought": "2024-02-01",
            "maturity_date": "2030-02-01",
            "interest_frequency": InterestFrequencyChoices.ANNUAL,
        }

    def test_api_auth_bonds(self):
        self.client.credentials()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 403)

    def test_api_create_bond(self):
        expected_response = {
            "id": 1,
            "issuer": "Test Issuer",
            "isin": "CZ0003569816",
            "face_value": "256.0000",
            "bond_rate": "5.5000",
            "date_bought": "2024-02-01",
            "maturity_date": "2030-02-01",
            "interest_frequency": InterestFrequencyChoices.ANNUAL.value,
            "user": 1,
        }

        response = self.client.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected_response)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        payload2 = self.default_payload
        payload2["isin"] = "CZ0003563959"
        response = self.client.post(self.url, data=payload2, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_unique_isin(self):
        response = self.client.post(self.url, data=self.default_payload, format="json")
        print(response.data)
        self.assertEqual(response.status_code, 201)

        response = self.client.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_correct_isin(self):
        payload = self.default_payload
        payload["isin"] = "CZ00"
        response = self.client.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 400)
