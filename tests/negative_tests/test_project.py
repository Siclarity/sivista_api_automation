import json
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

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 208 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

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

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

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

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

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

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 200 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message


    def test_create_project_with_single_alpha_string_char(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_single_alpha_string_char"
        payload = payload.get_payload_create_project()

        payload["projectName"] = "s"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "Please ensure the project name is between 2 and 100 characters long."
        actual_message = response.json().get("message")

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_exact_hundred_char(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_exact_hundred_char"
        payload = payload.get_payload_create_project()

        # Generate a project name with more than 100 characters (only A-Z)
        project_name = ''.join(random.choices(string.ascii_letters, k=100))  # Ensures more than 100 chars
        logger.info(f"Project name is : {project_name}")

        payload["projectName"] = project_name
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project has been successfully created."
        actual_message = response.json().get("message")

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 200 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message


    def test_create_project_with_more_than_hundred_char(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_more_than_hundred_char"
        payload = payload.get_payload_create_project()

        # Generate a project name with more than 100 characters (only A-Z)
        project_name = ''.join(random.choices(string.ascii_letters, k=105))  # Ensures more than 100 chars
        logger.info(f"Project name is : {project_name}")

        payload["projectName"] = project_name
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "Please ensure the project name is between 2 and 100 characters long."
        actual_message = response.json().get("message")

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_only_special_chars(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_only_special_char"
        payload = payload.get_payload_create_project()

        # Generate a string with exactly 10 special characters
        project_name = ''.join(random.choices(string.punctuation, k=10))

        logger.info(f"Project name is : {project_name}")
        payload["projectName"] = project_name
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project name cannot consist only of special characters. Please include letters or numbers in the name."
        actual_message = response.json().get("message")

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message


    def test_create_project_with_netlist_file_name_as_blank(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_netlist_file_name_as_blank"
        payload = payload.get_payload_create_project()

        payload["netlistMetadata"]["fileName"] = ""
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")

        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_netlist_file_name_as_spice_extension(self, test_login, session_csv_filename):
        payload = Payload()# Initialize your Baseclass (adjust if needed)
        fake = Faker()
        headers = self.common_header()
        test_name = "test_create_project_with_netlist_file_name_as_spice_extension"
        payload = payload.get_payload_create_project()

        # Generate a unique project name using Faker
        unique_project_name = fake.unique.name().replace(" ", "_")
        payload["projectName"] = unique_project_name

        payload["netlistMetadata"]["fileName"] = "netlist.spice"
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The project has been successfully created."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 200 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_netlist_file_name_as_tech_extension(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_netlist_file_name_as_spice_extension"
        payload = payload.get_payload_create_project()

        payload["netlistMetadata"]["fileName"] = "monCFET.tech"
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_netlist_file_type_other_than_global_or_user(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_netlist_file_type_other_than_global_or_user"
        payload = payload.get_payload_create_project()

        payload["netlistMetadata"]["netlistType"] = "employee"
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The Netlist file type is not valid. Please provide a file with the correct format."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_selecting_cell_name_as_blank(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_selecting_cell_name_as_blank"
        payload = payload.get_payload_create_project()

        payload["netlistMetadata"]["cellSelections"][1]["cell_name"] = ""

        logger.info(f"payload : {payload}")

        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "Cell mismatch detected. Please verify that the cell details are correct and consistent."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_in_cell_selections_array_is_selected_false_for_all_cells(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_in_cell_selections_array_is_selected_false_for_all_cells"
        payload = payload.get_payload_create_project()

        for cell in payload["netlistMetadata"]["cellSelections"]:
            cell["is_selected"] = False

        # logging.info(payload["netlistMetadata"]["cellSelections"])
        # logger.info(f"payload  : {payload}")

        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "No cells are selected."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_tech_file_name_as_spice_extension(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_name_as_spice_extension"
        payload = payload.get_payload_create_project()

        payload["techMetadata"]["fileName"] = "monCFET.spice"
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_tech_file_name_as_blank(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_name_as_blank"
        payload = payload.get_payload_create_project()

        payload["techMetadata"]["fileName"] = ""
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_tech_file_name_as_alphanumeric_char(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_name_as_alphanumeric_char"
        payload = payload.get_payload_create_project()

        payload["techMetadata"]["fileName"] = "sp4545"
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_tech_file_type_other_than_global_or_user(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_type_other_than_global_or_user"
        payload = payload.get_payload_create_project()

        payload["techMetadata"]["techType"] = "employee"
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The Tech file type is not valid. Please provide a file with the correct format."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_netlist_file_contents_key_as_empty(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_type_other_than_global_or_user"
        payload = payload.get_payload_create_project()

        payload["netlistFileContents"] = ""
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The netlist file is empty. Please upload a file with the required content."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_netlist_file_contents_key_as_blank(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_netlist_file_contents_key_as_blank"
        payload = payload.get_payload_create_project()

        payload["netlistFileContents"] = "  "
        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "Netlist file content must be in encoded format."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_tech_file_contents_key_as_empty(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_contents_key_as_empty"
        payload = payload.get_payload_create_project()

        payload["techFileContents"] = []

        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The tech file is empty. Please upload a file with the required content."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_with_tech_file_contents_key_as_null(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_with_tech_file_contents_key_as_null"
        payload = payload.get_payload_create_project()

        payload["techFileContents"] = None

        # logger.info(f"Payload : ,{payload}")
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The tech file is empty. Please upload a file with the required content."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_hyper_with_netlist_file_key_as_empty(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_hyper_with_netlist_file_key_as_empty"
        payload = payload.get_payload_create_hyperexpressivity()

        payload["netlistMetadata"]["fileName"] = ""
        logger.info(f"Payload : ,{payload}")

        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message


    def test_create_project_hyper_with_netlist_file_key_as_null(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_hyper_with_netlist_file_key_as_null"
        payload = payload.get_payload_create_hyperexpressivity()

        payload["netlistMetadata"]["fileName"] = None
        logger.info(f"Payload : ,{payload}")

        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The netlist file name is missing or invalid. Please provide a valid string value for 'netlistFileName'."
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message

    def test_create_project_hyper_with_netlist_file_extension_as_csv(self, test_login, session_csv_filename):
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = self.common_header()
        test_name = "test_create_project_hyper_with_netlist_file_key_as_empty"
        payload = payload.get_payload_create_hyperexpressivity()

        payload["netlistMetadata"]["fileName"] = "Lauren_Pugh_monCFET.csv"
        logger.info(f"Payload : ,{payload}")

        headers["Authorization"] = f"Bearer {test_login}"
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        expected_message = "The file extension is incorrect. Please select a .spice file for the netlist and a .tech file for the PDK. "
        actual_message = response.json().get("message")
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")
        logger.info(f"actual_message: {actual_message}")
        logger.info(f"expected_message : {expected_message}")

        status = "PASS" if response.status_code == 400 and actual_message == expected_message else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assertions to verify login failure
        assert expected_message == actual_message





