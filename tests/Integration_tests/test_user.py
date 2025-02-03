import json
import os
import random
import string
import time
import logging

import pytest
import requests
from faker import Faker

from src.helpers.payload_manager import Payload
from src.constants.basePage import Baseclass

logger = logging.getLogger(__name__)
faker = Faker()  # Initialize Faker instance


class TestUser(Baseclass):

    def test_about_api(self, test_login):
        url = self.about_API()
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        assert response.json() is not None
        assert response.status_code == 200

    @pytest.fixture(scope="function")
    def random_username(self):
        """Generates a random username with 'Demo' prefix using Faker."""
        return "Demo" + faker.unique.user_name()[:5]

    @pytest.fixture(scope="class")
    def create_User(self, test_login):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        payload = payload.get_payload_create_user()
        payload["username"] = faker.unique.user_name()[:5]
        url = self.create_user()
        logger.info(f"Creating user with username: {payload}")
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        UserID = response.json().get("data", {}).get("UserID")
        logger.info(f"user id created with id{UserID}")
        logger.info("create user API executed successfully")

        return UserID, response


    def test_create_user(self, test_login, create_User):
        UserID, response = create_User
        assert UserID is not None
        assert response.status_code == 200
        assert response.json() is not None

    def test_modify_user_details(self, test_login, create_User):
        fake = Faker()
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        payload = payload.get_payload_modify_user()
        UserID, _, = create_User
        url = self.modify_user_details(UserID)
        random_name = fake.first_name()  # Generates a short first name

        payload["name"] = random_name
        actual_name = random_name.upper()

        response = self.patch_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        assert response.status_code == 201
        assert response.json() is not None
        expected_name = response.json().get("data", {}).get("name")
        assert actual_name == expected_name

    def test_profile_user_list(self, test_login):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        payload = payload.get_payload_profile_list()
        url = self.user_profile_list()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        assert response.status_code == 200
        assert response.json() is not None
        logger.info("user profile list API executed successfully")



    def test_disable_user(self, test_login, create_User):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        payload = payload.get_payload_modify_user()
        UserID, _, = create_User
        payload["isActive"] = False
        url = self.modify_user_details(UserID)
        response = self.patch_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        assert response.status_code == 201
        assert response.json() is not None
        logger.info("modified user details API executed successfully")

    @pytest.fixture(scope="class")
    def test_user_login(self):
        payload = Payload()
        login_url = self.get_user_login()
        headers = self.common_header()
        payload = payload.get_payload_dummy_user()

        response = self.post_request(login_url, auth=None, headers=headers, payload=payload, in_json=False)
        print("Payload:", payload)
        print("Response:", response.json())

        access_token = response.json().get("token", {}).get("access")
        refresh_token = response.json().get("token", {}).get("refresh")
        logger.info(f"refresh token{refresh_token}")
        if not access_token:
            pytest.fail("Login failed. No access token retrieved.")
        print("Access Token:", access_token)
        return access_token, refresh_token

    def test_refresh_token(self, test_user_login):
        payload = Payload()
        headers = self.common_header()
        payload = payload.get_payload_dummy_user()
        access_token, refresh_token = test_user_login
        payload["refresh"] = refresh_token
        url = self.refresh_token()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        print(response)
        assert response.json() is not None
        assert response.status_code == 200

    def generate_secure_password(self):
        """Generates a secure password (8-16 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special character)."""
        length = random.randint(8, 16)

        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice("@$!%*?&")

        all_chars = string.ascii_letters + string.digits + "@$!%*?&"
        remaining_chars = ''.join(random.choices(all_chars, k=length - 4))

        password = list(uppercase + lowercase + digit + special + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    def load_json(self, file_path):
        """Loads JSON data from a file."""
        with open(file_path, "r") as file:
            return json.load(file)

    def save_json(self, file_path, data):
        """Saves JSON data to a file."""
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def test_update_password(self, test_user_login):
        access_token, _ = test_user_login
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {access_token}"

        # Load JSON files before making the request
        dummy_user = self.load_json("src/resources/dummy_user.json")
        password_data = self.load_json("src/resources/user_password_update.json")

        # Send API request with current password
        url = self.password_update()
        response = self.post_request(url, auth=None, headers=headers, payload=password_data, in_json=False)
        print(response.json())
        #logger.info(f"response{response.json()}")

        # Assertions
        assert response.status_code == 200, "Password update failed!"
        assert response.json() is not None, "Response is empty!"

        #  Only update JSON files AFTER successful password update
        old_password = password_data["password"]
        new_password = self.generate_secure_password()

        password_data["old_password"] = old_password  # Move current password to old_password
        password_data["password"] = new_password  # Set a new password

        dummy_user["Password"] = old_password  # Update dummy user with the previous password

        # Save updated data
        self.save_json("src/resources/user_password_update.json", password_data)
        self.save_json("src/resources/dummy_user.json", dummy_user)

        logger.info(
            f" Password updated successfully!\nOld Password: {password_data['old_password']}\nNew Password: {password_data['password']}")
