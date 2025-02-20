import random
import string
import time
import logging
import pytest

from src.helpers.payload_manager import Payload
from src.constants.basePage import Baseclass
from faker import Faker

from conftest import log_test_result

logger = logging.getLogger(__name__)


class TestSivista(Baseclass):

    def test_invalid_login(self, session_csv_filename):

        payload = Payload()
        login_url = self.get_user_login()
        headers = self.common_header()

        test_name = "test_invalid_login"

        payload = payload.get_payload_invalid_credentials()

        # Send POST request with invalid credentials
        response = self.post_request(login_url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "Invalid Credentials"
        actual_message = response.json().get("message")

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 401 and expected_message == actual_message else "FAIL"
        log_test_result(test_name, login_url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message
