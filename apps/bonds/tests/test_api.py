import datetime
from decimal import Decimal

from apps.bonds.enums import InterestFrequencyChoices
from apps.users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


url_bonds = "/en/api/bonds/"


class BondAPITests(APITestCase):
    url = url_bonds

    def setUp(self):
        self.client1 = APIClient()
        user1 = User.objects.create_user(username="test1", password="test1")
        token1, created = Token.objects.get_or_create(user=user1)
        self.client1.credentials(HTTP_AUTHORIZATION="Token " + token1.key)

        self.client2 = APIClient()
        user2 = User.objects.create_user(username="test2", password="test2")
        token2, created = Token.objects.get_or_create(user=user2)
        self.client2.credentials(HTTP_AUTHORIZATION="Token " + token2.key)

        self.default_payload = {
            "issuer": "Test Issuer",
            "isin": "CZ0003569816",
            "face_value": 256,
            "interest_rate": 5.5,
            "date_added": "2024-02-01",
            "maturity_date": "2030-02-01",
            "interest_frequency": InterestFrequencyChoices.ANNUAL,
        }

    def test_api_auth_bonds(self):
        self.client1.credentials()

        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client1.post(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client1.delete(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client1.put(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client1.patch(self.url)
        self.assertEqual(response.status_code, 403)

    def test_api_post_bond(self):
        expected_response = {
            "id": 1,
            "issuer": "Test Issuer",
            "isin": "CZ0003569816",
            "face_value": "256.0000",
            "interest_rate": "5.5000",
            "date_added": "2024-02-01",
            "maturity_date": "2030-02-01",
            "interest_frequency": InterestFrequencyChoices.ANNUAL.value,
            "user": 1,
        }

        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected_response)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        payload2 = self.default_payload
        payload2["isin"] = "CZ0003563959"
        response = self.client1.post(self.url, data=payload2, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_api_put_bond(self):
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["issuer"], self.default_payload["issuer"])

        payload2 = self.default_payload
        new_issuer = "Name modified with put call"
        payload2["issuer"] = new_issuer
        response = self.client1.put(self.url + "1/", data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["issuer"], new_issuer)

        payload3 = {
            "issuer": "Should fail due to missing other fields!",
        }
        response = self.client1.put(self.url + "1/", data=payload3, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_patch_bond(self):
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)

        payload2 = self.default_payload
        payload2["isin"] = "CZ0003563959"
        response = self.client1.post(self.url, data=payload2, format="json")
        self.assertEqual(response.status_code, 201)

        new_face_value = "666.0000"
        payload3 = {
            "face_value": new_face_value,
        }
        response = self.client1.patch(self.url + "2/", data=payload3, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[1]["face_value"], new_face_value)

        new_interest_frequency = InterestFrequencyChoices.SEMI_ANNUAL
        payload4 = {
            "interest_frequency": new_interest_frequency,
        }
        response = self.client1.patch(self.url + "1/", data=payload4, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["interest_frequency"], new_interest_frequency.value)

    def test_api_delete_bond(self):
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client1.delete(self.url + "2/")
        self.assertEqual(response.status_code, 404)

        payload2 = self.default_payload
        payload2["isin"] = "CZ0003563959"
        response = self.client1.post(self.url, data=payload2, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client1.delete(self.url + "2/")
        self.assertEqual(response.status_code, 204)
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client1.post(self.url, data=payload2, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client1.delete(self.url + "1/")
        self.assertEqual(response.status_code, 204)
        response = self.client1.delete(self.url + "3/")
        self.assertEqual(response.status_code, 204)

    def test_multiple_users_bonds(self):
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client2.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_change_user_bond(self):
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)

        new_user = 2
        payload2 = {
            "user": new_user,
        }

        response = self.client2.patch(self.url + "1/", data=payload2, format="json")
        self.assertEqual(response.data["detail"], "No Bond matches the given query.")
        self.assertEqual(response.status_code, 404)

        response = self.client1.patch(self.url + "1/", data=payload2, format="json")
        self.assertEqual(response.data["user"], 1)
        self.assertEqual(response.status_code, 200)

    def test_unique_isin(self):
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_correct_isin(self):
        payload = self.default_payload
        payload["isin"] = "CZ00"
        response = self.client1.post(self.url, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 400)


class PortfolioAnalysisTests(APITestCase):
    url_portfolio_analysis = "/en/api/portfolio-analysis/"

    def setUp(self):
        self.client1 = APIClient()
        user1 = User.objects.create_user(username="test1", password="test1")
        token1, created = Token.objects.get_or_create(user=user1)
        self.client1.credentials(HTTP_AUTHORIZATION="Token " + token1.key)

        self.default_payload = {
            "issuer": "Test Issuer",
            "isin": "CZ0003569816",
            "face_value": 500,
            "interest_rate": 10,
            "date_added": "2025-02-01",
            "maturity_date": "2027-02-01",
            "interest_frequency": InterestFrequencyChoices.ANNUAL,
        }

    def test_api_auth_portfolio_analysis(self):
        self.client1.credentials()

        response = self.client1.get(self.url_portfolio_analysis)
        self.assertEqual(response.status_code, 403)

    def test_api_portfolio_analysis(self):
        response = self.client1.post(url_bonds, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)

        payload2 = self.default_payload
        payload2["isin"] = "CZ0003539090"
        payload2["face_value"] = 1000
        payload2["interest_rate"] = 2.5
        response = self.client1.post(url_bonds, data=payload2, format="json")
        self.assertEqual(response.status_code, 201)

        expected_response = {
            "average_interest_rate": 6.25,
            "nearest_maturity": datetime.date(2027, 2, 1),
            "total_portfolio_value": Decimal("1500"),
            "total_future_portfolio_value": Decimal("1650"),
        }

        response = self.client1.get(self.url_portfolio_analysis)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, expected_response)

    def test_api_portfolio_analysis_zeros(self):
        payload = self.default_payload
        payload["face_value"] = 0
        payload["interest_rate"] = 0

        response = self.client1.post(url_bonds, data=self.default_payload, format="json")
        self.assertEqual(response.status_code, 201)

        expected_response = {
            "average_interest_rate": 0,
            "nearest_maturity": datetime.date(2027, 2, 1),
            "total_portfolio_value": 0,
            "total_future_portfolio_value": 0,
        }

        response = self.client1.get(self.url_portfolio_analysis)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, expected_response)
