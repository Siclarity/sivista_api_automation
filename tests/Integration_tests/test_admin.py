import os
import time
import logging
import pytest
import requests

from src.helpers.payload_manager import Payload
from src.constants.basePage import Baseclass

logger = logging.getLogger(__name__)


class TestAdmin(Baseclass):
    # file_path = "C:/Users/MeghakMahadi/PycharmProjects/API_Automation/src/resources/mw.tech"
    #
    # netlist_file_path = "C:/Users/MeghakMahadi/PycharmProjects/API_Automation/src/resources/mw.spice"

    #
    @pytest.fixture(scope="class")
    def get_file(self, test_login):
        file = open(self.file_path, 'rb')
        yield file  # The file is yielded for use in tests
        file.close()

    def test_upload_tech_file(self, test_login, get_file):
        headers = self.common_header1(test_login)

        # Use the file provided by the fixture
        files = {"upload": get_file}
        url = self.get_file_upload()

        # Example upload request
        response = requests.post(url, headers=headers, files=files)
        assert response.json() is not None
        # Assertions to validate the response
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        logger.info(f"tech file uploaded successfully")

    @pytest.fixture(scope="class")
    def test_get_uploaded_tech_file(self, test_login, get_file):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_file_list()
        payload = Payload()
        payload = payload.get_payload_get_techfile()

        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        assert response.json() is not None
        assert response.status_code == 200
        response_data = response.json()
        # Assuming response contains a list of files under "data"
        files = response_data.get("data", {}).get("Items", [])

        # Get the file name of the uploaded file
        uploaded_file_name = os.path.basename(get_file.name)

        # Find the file with the name that matches the one we uploaded
        uploaded_file = next((file for file in files if file.get("FileName") == uploaded_file_name), None)

        assert uploaded_file is not None, f"Uploaded file with name {uploaded_file_name} not found in the response"

        # Extract the fileId of the uploaded file
        file_id = uploaded_file.get("FileId")

        assert file_id is not None, "fileId not found for the uploaded file"
        logger.info(f"File ID of the uploaded tech file: {file_id}")

        return file_id  # Optionally return it if you need to use it

    def test_modify_tech_File(self, test_login, get_file, test_get_uploaded_tech_file):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        tech_file = os.path.basename(get_file.name)
        FileId = test_get_uploaded_tech_file
        logger.info(f"file name is{tech_file}")
        payload = payload.get_payload_modify_techfile()
        payload["FileName"] = tech_file
        payload["FileId"] = FileId
        logger.info(f"payload for modify_netlist is{payload}")
        url = self.get_modify_file()
        response = self.put_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        print(response.json())
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"tech file modified successfully")

    def test_delete_tech_file(self, test_login, get_file, test_get_uploaded_tech_file):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        tech_file = os.path.basename(get_file.name)
        FileId = test_get_uploaded_tech_file
        logger.info(f"file name is{tech_file}")
        payload = payload.get_payload_delete_techfile()
        payload["FileName"] = tech_file
        payload["FileId"] = FileId
        logger.info(f"payload for deletetechdata is{payload}")
        url = self.delete_tech_file()
        response = self.delete_file(url, auth=None, headers=headers, payload=payload, in_json=False)
        print(response.json())
        assert response.json()is not None
        assert response.status_code==200
        logger.info(f"tech file deleted succesfully")

    #######################for netlist file##################################

    @pytest.fixture(scope="class")
    def get_netlist_file(self, test_login):
        file = open(self.netlist_file_path, 'rb')
        yield file  # The file is yielded for use in tests
        file.close()

    def test_upload_netlist_file(self, test_login, get_netlist_file):
        headers = self.common_header1(test_login)

        # Use the file provided by the fixture
        files = {"upload": get_netlist_file}
        url = self.get_netlist_upload()

        # Example upload request
        response = requests.post(url, headers=headers, files=files)
        assert response.json() is not None
        # Assertions to validate the response
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        logger.info(f"netlist file uploaded succesfully")

    @pytest.fixture(scope="class")
    def test_get_uploaded_netlist_file(self, test_login, get_netlist_file):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_file_list()
        payload = Payload()
        payload = payload.get_payload_get_netlistfile()

        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        # assert response.json() is not None
        # assert response.status_code ==200
        response_data = response.json()
        # Assuming response contains a list of files under "data"
        files = response_data.get("data", {}).get("Items", [])

        # Get the file name of the uploaded file
        uploaded_file_name = os.path.basename(get_netlist_file.name)

        # Find the file with the name that matches the one we uploaded
        uploaded_file = next((file for file in files if file.get("FileName") == uploaded_file_name), None)

        assert uploaded_file is not None, f"Uploaded file with name {uploaded_file_name} not found in the response"

        # Extract the fileId of the uploaded file
        file_id = uploaded_file.get("FileId")

        assert file_id is not None, "fileId not found for the uploaded file"
        logger.info(f"File ID of the uploaded tech file: {file_id}")

        return file_id  # Optionally return it if you need to use it

    def test_modify_netlist_File(self, test_login, get_netlist_file, test_get_uploaded_netlist_file):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        tech_file = os.path.basename(get_netlist_file.name)
        FileId = test_get_uploaded_netlist_file
        logger.info(f"file name is{tech_file}")
        payload = payload.get_payload_modify_netlist()
        payload["FileName"] = tech_file
        payload["FileId"] = FileId
        logger.info(f"payload for modify_netlist is{payload}")
        url = self.get_modify_file()
        response = self.put_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        print(response.json())
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"netlist file updated successfully")

    def test_delete_netlist_file(self, test_login, get_netlist_file, test_get_uploaded_netlist_file):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        payload = Payload()
        tech_file = os.path.basename(get_netlist_file.name)
        FileId = test_get_uploaded_netlist_file
        logger.info(f"file name is{tech_file}")
        payload = payload.get_payload_delete_netlistfile()
        payload["FileName"] = tech_file
        payload["FileId"] = FileId
        logger.info(f"payload for deletenetlist is{payload}")
        url = self.delete_tech_file()
        response = self.delete_file(url, auth=None, headers=headers, payload=payload, in_json=False)
        print(response.json())
        assert response.status_code == 200
        assert response.json() is not None
        logger.info(f"netlist file deleted successfully")
