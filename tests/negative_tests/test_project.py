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

    @pytest.fixture(scope="class")
    def test_create_project_layout(self, test_login, session_csv_filename):
        """
        Fixture to create a project and return the project ID.
        The project ID is generated for every test that uses this fixture.
        """
        fake = Faker()
        base = Baseclass()
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = base.common_header()

        # Load the base payload
        payload = payload.get_payload_create_project()
        test_name = "test_create_project_layout"

        # Generate a unique project name using Faker
        unique_project_name = fake.unique.name().replace(" ", "_")
        payload["projectName"] = unique_project_name
        cell_name = [
            cell["cell_name"]
            for cell in payload["netlistMetadata"]["cellSelections"]
            if cell["is_selected"] == True  # This ensures only selected cells are fetched
        ]

        headers["Authorization"] = f"Bearer {test_login}"
        url = base.create_project()

        # Send the API request
        response = base.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        # Assert the response
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.json()}"
        assert response.json() is not None
        logger.info(f"response.json()")
        project_id = response.json().get("data", {}).get("projectId")
        assert project_id is not None
        logger.info(f"project id for layout{project_id}")
        logger.info(f"cell name is{cell_name}")
        logger.info(f"stage1 project created succesfully")
        return project_id, unique_project_name, cell_name

    def test_create_project_existing_project_name(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_existing_project_name"
        _, unique_project_name, _, = test_create_project_layout
        payload = payload.get_payload_create_project()

        payload["projectName"] = unique_project_name
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project name already exists. Please choose a different name."
        actual_message = response.json().get("message")
        assert expected_message == actual_message
        status = "PASS" if response.status_code == 208 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)

    def test_create_project_with_blank_project_name(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_blank_project_name"
        payload = payload.get_payload_create_project()

        payload["projectName"] = ""
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project name cannot be left blank. Please enter a valid project name."
        actual_message = response.json().get("message")
        assert expected_message == actual_message
        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)


    def test_create_project_with_single_special_char(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_single_special_char"
        payload = payload.get_payload_create_project()

        payload["projectName"] = "#"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project name cannot consist only of special characters. Please include letters or numbers in the name."
        actual_message = response.json().get("message")
        assert expected_message == actual_message
        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)

    def test_create_project_with_one_char_and_one_special_char(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_one_char_and_one_special_char"
        payload = payload.get_payload_create_project()

        # Generate a project name with one special character and one alphanumeric character
        special_char = random.choice(string.punctuation)
        alphanumeric_char = random.choice(string.ascii_letters + string.digits)
        project_name = f"{special_char}{alphanumeric_char}"

        payload["projectName"] = project_name
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project has been successfully created."
        actual_message = response.json().get("message")
        assert expected_message == actual_message
        status = "PASS" if response.status_code == 200 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)









