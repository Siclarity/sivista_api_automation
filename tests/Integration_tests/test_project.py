import logging
import time
import logging
import pytest

from src.helpers.payload_manager import Payload
from src.constants.basePage import Baseclass
from faker import Faker

from conftest import log_test_result

logger = logging.getLogger(__name__)


class TestSivista(Baseclass):

    def test_project_status(self, test_login, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_project_status"
        headers["Authorization"] = f"Bearer {test_login}"

        payload = payload.get_payload_check_project_status()

        url = self.check_project_status()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)

        logger.info(f"response for run_layout{response.json()}")
        assert response.status_code == 200
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        logger.info(f"project status api executed succesfully")

    def test_project_list(self, test_login, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_project_list"
        url = self.project_list()
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"project list api executed succesfully")

    def test_validate_netlist(self, test_login, session_csv_filename):
        headers = self.common_header()
        headers['Authorization'] = f"Bearer {test_login}"
        test_name = "test_validate_netlist"
        url = self.validate_netlist()
        payload = Payload()
        payload = payload.get_payload_validate_netlist()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        logger.info(f"response for run_layout{response.json()}")
        assert response.status_code == 200
        assert response.json() is not None
        logger.info(f"netlist validate api executed successfully")

    def test_download_global_netlist(self, test_login, session_csv_filename):
        headers = self.common_header()
        headers['Authorization'] = f"Bearer {test_login}"
        test_name = "download_global_netlist"
        url = self.download_file()
        payload = Payload()
        payload = payload.download_global_netlist()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        expected_filename = "NETLIST_Files.zip"
        if response.headers.get("X-Filename") != expected_filename:
            status = "FAIL"
            logger.error(
                f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'.")

        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        #expected_filename = "NETLIST_Files.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        logger.info(f"netlist validate api executed successfully")

    def test_download_global_techfile(self, test_login, session_csv_filename):
        headers = self.common_header()
        headers['Authorization'] = f"Bearer {test_login}"
        test_name = "test_download_global_techfile"
        url = self.download_file()
        payload = Payload()
        payload = payload.download_global_netlist()
        payload[0]['FileName'] = "monCFET.tech"
        payload[0]['DirType'] = "techfile"
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        expected_filename = "TECHFILE_Files.zip"
        if response.headers.get("X-Filename") != expected_filename:
            status = "FAIL"
            logger.error(
                f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'.")

        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        # expected_filename = "NETLIST_Files.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        logger.info(f"global techfile api executed successfully")

    @pytest.mark.em
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

    def test_download_user_netlist(self, test_login, test_create_project_layout, session_csv_filename):
        headers = self.common_header()
        headers['Authorization'] = f"Bearer {test_login}"
        test_name = "download_global_netlist"
        url = self.download_file()
        _, project_name, _ = test_create_project_layout
        payload = Payload()
        payload = payload.download_global_netlist()
        payload[0]['FileType'] = "USER"
        payload[0]['FileName'] = f"{project_name}_monCFET.spice"
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        expected_filename = "NETLIST_Files.zip"
        if response.headers.get("X-Filename") != expected_filename:
            status = "FAIL"
            logger.error(
                f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'.")

        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        #expected_filename = "NETLIST_Files.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        logger.info(f"netlist validate api executed successfully")

    def test_download_user_techfile(self, test_login, test_create_project_layout, session_csv_filename):
        headers = self.common_header()
        headers['Authorization'] = f"Bearer {test_login}"
        test_name = "test_download_user_techfile"
        url = self.download_file()
        _, project_name, _ = test_create_project_layout
        payload = Payload()
        payload = payload.download_global_netlist()
        payload[0]['FileType'] = "USER"
        payload[0]['DirType'] = "techfile"
        payload[0]['FileName'] = f"{project_name}_monCFET.tech"
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        expected_filename = "TECHFILE_Files.zip"
        if response.headers.get("X-Filename") != expected_filename:
            status = "FAIL"
            logger.error(
                f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'.")

        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        #expected_filename = "NETLIST_Files.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        logger.info(f"download user techfile api executed successfully")

    def test_project_status_once_created(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_project_status_once_created"
        headers["Authorization"] = f"Bearer {test_login}"
        _, project_name, _ = test_create_project_layout

        payload = payload.get_payload_check_project_status()
        payload["projectName"] = project_name

        url = self.check_project_status()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 208 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        logger.info(f"response for run_layout{response.json()}")
        assert response.status_code == 208
        assert response.json() is not None
        logger.info(f"project status api after project creation executed successfully")

    @pytest.mark.em
    def test_create_project_and_verify(self, test_create_project_layout):
        project_id, unique_project_name, _, = test_create_project_layout
        assert project_id is not None, "Project ID should be valid."
        assert unique_project_name is not None

    @pytest.mark.em
    @pytest.fixture(scope="class")
    def test_run_layout_project(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_run_layout_project"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_layout
        payload = payload.get_payload_run_project()
        payload["projectId"] = project_id
        print("pppp", project_id)
        url = self.run_layout()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        logger.info(f"response for run_layout{response.json()}")
        time.sleep(30)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        jobId = response.json()['data']['jobId']
        logger.info(f"job id for stage1 {jobId}")
        return jobId

    @pytest.mark.em
    def test_verify_run_layout_project(self, test_run_layout_project):
        jobid = test_run_layout_project
        assert jobid is not None
        logger.info(f"stage1 project API executed succesfully with job id{jobid}")

    ##########################code commented for stage summary as code is not deployed on QA##############################################################


    # @pytest.mark.em
    # def test_stage1_run_summary(self, test_login, test_create_project_layout, session_csv_filename):
    #     payload = Payload()
    #     headers = self.common_header()
    #     test_name = "test_stage1_run_summary"
    #     headers["Authorization"] = f"Bearer {test_login}"
    #     project_id, _, _, = test_create_project_layout
    #     payload = payload.get_payload_stage_summary()
    #     payload["projectId"] = project_id
    #     logger.info(f"payload for stage1 summary is {payload}")
    #     url = self.stage_summary()
    #     response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
    #     logger.info(response.json())
    #     status = "PASS" if response.status_code == 200 else "FAIL"
    #     log_test_result(test_name, url, status, session_csv_filename)
    #     assert response.status_code == 200
    #     assert response.json() is not None
    #     # logger.info(f"response for run_layout{response.json()}")

    def test_get_stage1_job_details(self, test_login, test_run_layout_project, session_csv_filename):
        jobid = test_run_layout_project
        test_name = "test_get_stage1_job_details"
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_job_run(jobid)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(10)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"details fetch succesfully for {jobid}")


    @pytest.fixture(scope="class")
    def test_stage1_result(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_stage1_result"
        headers["Authorization"] = f"Bearer {test_login}"
        #project_id, unique_project_name, _, = test_create_project_layout
        project_id, _, _, = test_create_project_layout
        payload = payload.get_payload_stage1_result()
        payload["projectId"] = project_id
        print("payload for stage1", payload)
        print("project_id in stage1", project_id)
        logger.info(f"projectid for stage1{project_id}")
        url = self.stage1_result()
        print("url for stage1", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(15)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        response_data = response.json()
        print(f"response for stage1{response.json()}")
        logger.info(f"show_result api for stage1 executed successfully")

        filenames = [
            item["File"] for pex in response_data["data"]["PEX_Consolidated"] for item in pex["data"]
        ]

        # Get the 0th index filename
        extracted_filename = filenames[0] if filenames else None  # Handle case if list is empty

        print("Extracted 0th index filename from PEX_Consolidated:", extracted_filename)
        layout_data_list = [item["LayoutData"] for item in response_data["data"]["Items"]]
        logger.info(f"layoutdata list,{layout_data_list}")

        # Print all LayoutData entries
        for layout in layout_data_list:
            print(layout)

        return extracted_filename, response, layout_data_list

    def test_get_gds_images_stage1(self, test_login, test_stage1_result, session_csv_filename):
        _, _, layout_data_list = test_stage1_result
        payload = Payload()
        headers = self.common_header()
        test_name = "test_get_gds_images_stage1"
        headers["Authorization"] = f"Bearer {test_login}"
        payload = payload.get_payload_gds_images()
        payload["LayoutData"] = layout_data_list
        logger.info(f"payload for gds{payload}")
        url = self.get_gds_images()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"GDS images API for stage1 executed successfully")

    def test_stage1_result_verification(self, test_stage1_result):
        """
        Test case that verifies Stage 1 API response.
        Uses the fixture `test_stage1_result`.
        """
        extracted_filename, response, _, = test_stage1_result  # Unpack response and filename

        # Assertions for response verification
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.json()}"
        assert response.json() is not None, "Response JSON should not be None"
        assert extracted_filename is not None, "Extracted filename should not be None"

    def test_download_all_stage1(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_download_all_stage1"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_layout
        #logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_payload_stage1_download_All()
        payload["project_id"] = project_id

        print(f"payload for download{payload}")
        logger.info(f"projectid for stage1_download{project_id}")
        url = self.get_stage_download_all_layout()
        print("url for stage1_download", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        print(response.headers)
        assert response.status_code == 200
        #Dynamically construct the expected filename
        expected_filename = f"{unique_project_name}_Stage1.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )

        # Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )
        logger.info(f"downloadAPI for  stage1 executed successfully")

    def test_single_gds_download(self, test_login, test_create_project_layout, test_stage1_result,
                                 session_csv_filename):
        #assert self.extracted_filename is not None, "test_stage1_result must run before test_single_gds_download"
        payload = Payload()
        headers = self.common_header()
        test_name = "test_single_gds_download"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_layout
        url = self.single_gds_download()
        logger.info(f"url for single_download{url}")
        # logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_single_gds_payload()
        payload["projectId"] = project_id
        extracted_filename, _, _, = test_stage1_result
        payload["fileList"] = [extracted_filename]  # Use stored filename

        print("payload for singlegds", payload)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.headers is not None
        logger.info(f"stgae1 singlegdsheaders{response.headers}")
        expected_filename = f"{extracted_filename}.zip"
        print(f"headers filename is{expected_filename}")
        assert response.status_code == 200

        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        # Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )
        logger.info(f"download api for stage1 for single gds executed successfully")

    def test_getlist_netlist(self, test_login, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_getlist_netlist"
        url = self.get_netlist()
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response is not None
        assert response.status_code == 200
        logger.info(f"getlist for nrtlist API executed successfully")

    def test_getlist_techlist(self, test_login, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_getlist_techlist"
        url = self.get_techlist()
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response is not None
        assert response.status_code == 200
        logger.info(f"getlist for tech file API executed successfully")

    def test_get_data(self, test_login, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_get_data"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_netlist_data()
        payload = payload.get_payload_netlist_getdata()
        print(payload)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        print(response.json())
        assert response.status_code == 200
        assert response.json() is not None
        logger.info(f"get data for netlist executed successfully")

    def test_techdata(self, test_login, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        payload = payload.get_payload_techdata()
        test_name = "test_techdata"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_techdata()

        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        logger.info(f"get data for techfile executed successfully")

    def test_get_job_list(self, test_login, session_csv_filename):
        headers = self.common_header()
        payload = Payload()
        test_name = "test_get_job_list"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_job_list()
        payload = payload.get_run_list_payload()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        if response.status_code == 200:
            assert response.json().get("status") is True, "Expected status=True for running jobs"
            logger.info("✅ Job list retrieved successfully. Running jobs found.")

        elif response.status_code == 404:
            assert response.json().get("status") is False, "Expected status=False when no running jobs"
            assert response.json().get("message") == "There is not any running job present", "Unexpected error message"
            logger.info("⚠️ No running jobs found.")

        else:
            pytest.fail(f"Unexpected status code: {response.status_code()}, Response: {response.json()}")

    # def test_get_job_list(self, test_login):
    #     headers = self.common_header()
    #     payload = Payload()
    #     headers["Authorization"] = f"Bearer {test_login}"
    #     url = self.get_job_list()
    #     payload = payload.get_run_list_payload()
    #     response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
    #     assert response.json() is not None
    #     assert response.status_code == 405
    #     logger.info(f"job list API executed successfully")

    def test_get_stage1_ready_list(self, test_login, session_csv_filename):
        headers = self.common_header()
        test_name = "test_get_stage1_ready_list"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_stage1_ready()
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"stage1 ready API  executed successfully")

    def test_get_project_details_stage1(self, test_login, test_create_project_layout, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_get_project_details_stage1"
        project_id, _, _, = test_create_project_layout
        url = self.get_project_details(project_id)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(10)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"project details fpr stage1 executed successfully")

    #========================================================================================

    @pytest.fixture(scope="class")
    def create_project_hyperexpressivity(self, test_login, test_create_project_layout, test_stage1_result,
                                         session_csv_filename):
        headers = self.common_header()
        fake = Faker()
        test_name = "create_project_hyperexpressivity"
        headers["Authorization"] = f"Bearer {test_login}"
        stage1_projectid, _, _, = test_create_project_layout
        selected_layout, _, _, = test_stage1_result
        payload = Payload()
        payload = payload.get_payload_create_hyperexpressivity()
        stage2_project_name = fake.unique.name().replace(" ", "_")

        payload["projectName"] = stage2_project_name
        payload["stageOneProjectId"] = stage1_projectid
        payload["selectedLayouts"] = [selected_layout]
        url = self.create_project()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        stage2_project_id = response.json().get("data", {}).get("projectId")
        return stage2_project_id, stage2_project_name

    def test_verify_project_hyperexpressivity(self, create_project_hyperexpressivity):
        stage2_project_id, stage2_project_name = create_project_hyperexpressivity
        assert stage2_project_id is not None, "Project ID should be valid."
        assert stage2_project_name is not None
        logger.info(f"stage2 project created {stage2_project_id} successfully")

    #
    @pytest.fixture(scope="class")
    def test_run_project_hyperexpressvity(self, test_login, create_project_hyperexpressivity, test_stage1_result,
                                          test_create_project_layout, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_run_project_hyperexpressvity"
        stage2_project_id, _, = create_project_hyperexpressivity
        stage1_project, _, cell_name = test_create_project_layout
        selected_layout, _, _, = test_stage1_result
        payload = Payload()
        payload = payload.get_payload_create_hyperexpressivity()
        payload["stage1Project"] = stage1_project
        payload["projectId"] = stage2_project_id
        payload["selectedLayouts"] = [selected_layout]
        payload["cells"] = cell_name
        url = self.run_layout()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        print(response.json())
        time.sleep(40)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        jobId = response.json()['data']['jobId']
        logger.info(f"job id for stage2 {jobId}")
        logger.info(f"stage2 run API executed successfully ")
        return jobId

    #
    def test_get_stage2_job_details(self, test_login, test_run_project_hyperexpressvity, session_csv_filename):
        jobid = test_run_project_hyperexpressvity
        headers = self.common_header()
        test_name = "test_get_stage2_job_details"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_job_run(jobid)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(10)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    def test_verify_project_hyper_expressivity(self, test_run_project_hyperexpressvity):
        jobId = test_run_project_hyperexpressvity
        assert jobId is not None

    @pytest.fixture(scope="class")
    def test_stage2_show_result(self, test_login, create_project_hyperexpressivity, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_stage2_show_result"
        # project_id, unique_project_name, _, = test_create_project_layout
        project_id, _, = create_project_hyperexpressivity
        payload = payload.get_payload_stage2_result()
        payload["projectId"] = project_id
        print("payload for stage2", payload)
        print("project_id in stage2", project_id)
        logger.info(f"projectid for stage1{project_id}")
        url = self.stage1_result()
        print("url for stage1", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(30)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        response_data = response.json()
        print(f"response for stage1{response.json()}")
        filenames = [
            item["File"] for pex in response_data["data"]["PEX_Consolidated"] for item in pex["data"]
        ]
        extracted_filename = filenames[0] if filenames else None  # Handle case if list is empty

        print("Extracted 0th index filename from PEX_Consolidated:", extracted_filename)
        layout_data_list = [item["LayoutData"] for item in response_data["data"]["Items"]]
        logger.info(f"layoutdata list,{layout_data_list}")
        # Print all LayoutData entries
        for layout in layout_data_list:
            print(layout)
        return extracted_filename, response, layout_data_list

    def test_verify_stage2_result(self, test_stage2_show_result):
        _, response, layout_data_list = test_stage2_show_result
        assert response.json() is not None
        assert response.status_code == 200
        assert layout_data_list is not None

    def test_get_project_details_stage2(self, test_login, create_project_hyperexpressivity, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_get_project_details_stage2"
        project_id, _, = create_project_hyperexpressivity
        url = self.get_project_details(project_id)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(15)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    def test_get_gds_images_stage2(self, test_login, test_stage2_show_result, session_csv_filename):
        _, _, layout_data_list = test_stage2_show_result
        payload = Payload()
        headers = self.common_header()
        test_name = "test_get_gds_images_stage2"
        headers["Authorization"] = f"Bearer {test_login}"
        payload = payload.get_payload_gds_images()
        payload["LayoutData"] = layout_data_list
        logger.info(f"payload for gds{payload}")
        url = self.get_gds_images()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(30)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    def test_download_all_stage2(self, test_login, create_project_hyperexpressivity, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_download_all_stage2"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name = create_project_hyperexpressivity
        #logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_payload_stage2_download_All()
        payload["project_id"] = project_id

        print(f"payload for download{payload}")
        logger.info(f"projectid for stage1_download{project_id}")
        url = self.get_stage_download_all_layout()
        print("url for stage1_download", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        #print(response.headers)
        time.sleep(30)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        #Dynamically construct the expected filename
        expected_filename = f"{unique_project_name}_Stage2.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )

        # Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )

    def test_single_gds_download_stage2(self, test_login, create_project_hyperexpressivity, test_stage2_show_result,
                                        session_csv_filename):
        #assert self.extracted_filename is not None, "test_stage1_result must run before test_single_gds_download"
        payload = Payload()
        headers = self.common_header()
        test_name = "test_single_gds_download_stage2"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name = create_project_hyperexpressivity
        url = self.single_gds_download()
        # logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_single_gds_payload_stage2()
        payload["projectId"] = project_id
        extracted_filename, _, _, = test_stage2_show_result
        payload["fileList"] = [extracted_filename]  # Use stored filename

        print("payload for singlegds", payload)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.headers is not None

        logger.info(f"headers{response.headers}")

        expected_filename = f"{extracted_filename}.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        #Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )

    def test_edit_stage1_project(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()
        project_id, unique_project_name, _, = test_create_project_layout
        headers = self.common_header()
        test_name = "test_edit_stage1_project"
        headers["Authorization"] = f"Bearer {test_login}"
        payload = payload.get_payload_stage1_edit_project()
        url = self.edit_stage_project(project_id)
        response = self.patch_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        print(response.json())
        assert response.json() is not None
        assert response.status_code == 200

    def test_edit_stage2_project(self, test_login, create_project_hyperexpressivity, session_csv_filename):
        payload = Payload()
        project_id, unique_project_name = create_project_hyperexpressivity
        headers = self.common_header()
        test_name = "test_edit_stage2_project"
        headers["Authorization"] = f"Bearer {test_login}"
        payload = payload.get_payload_stage2_edit_project()
        url = self.edit_stage_project(project_id)
        response = self.patch_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    #
    def test_clear_result_stage1(self, test_login, test_create_project_layout, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_clear_result_stage1"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_layout
        payload = payload.clear_result_stage1()
        payload["projectId"] = project_id
        print("pppp", project_id)
        url = self.clear_stage_result()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        logger.info(f"response for run_layout{response.json()}")
        assert response.json() is not None
        assert response.status_code == 200

    def test_clear_result_stage2(self, test_login, create_project_hyperexpressivity, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_clear_result_stage2"
        project_id, unique_project_name = create_project_hyperexpressivity
        payload = payload.clear_result_stage2()
        payload["projectId"] = project_id
        print("pppp", project_id)
        url = self.clear_stage_result()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        logger.info(f"response for run_layout{response.json()}")
        assert response.json() is not None
        assert response.status_code == 200

    def test_delete_stage1_project(self, test_login, test_create_project_layout, session_csv_filename):
        project_id, unique_project_name, _, = test_create_project_layout
        headers = self.common_header()
        test_name = "test_delete_stage1_project"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.delete_project(project_id)
        response = self.delete_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None

        logger.info(f"delete API for stage1 executed successfully")

    def test_delete_stage2_project(self, test_login, create_project_hyperexpressivity, session_csv_filename):
        project_id, unique_project_name, = create_project_hyperexpressivity
        headers = self.common_header()
        test_name = "test_delete_stage2_project"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.delete_project(project_id)
        response = self.delete_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        logger.info(f"delete API for stage2 executed successfully")

        ########################################action3###############################

    @pytest.fixture(scope="class")
    def test_create_project_action3(self, test_login, session_csv_filename):
        """
        Fixture to create a project and return the project ID.
        The project ID is generated for every test that uses this fixture.
        """
        fake = Faker()
        base = Baseclass()
        payload = Payload()  # Initialize your Baseclass (adjust if needed)
        headers = base.common_header()
        test_name = "test_create_project_action3"

        # Load the base payload
        payload = payload.get_payload_create_action3()

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
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        # Assert the response
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.json()}"
        assert response.json() is not None
        logger.info(f"response.json()")
        project_id = response.json().get("data", {}).get("projectId")
        assert project_id is not None
        logger.info(f"project id for layout{project_id}")
        logger.info(f"cell name is{cell_name}")
        return project_id, unique_project_name, cell_name

    def test_create_project_and_verify_action3(self, test_create_project_action3):
        project_id, unique_project_name, _, = test_create_project_action3
        assert project_id is not None, "Project ID should be valid."
        assert unique_project_name is not None
        logger.info(f"project created API executed successfully with {project_id}")

    @pytest.fixture(scope="class")
    def test_run_layout_project_action3(self, test_login, test_create_project_action3, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_run_layout_project_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_action3
        payload = payload.get_payload_run_layout_Action3()
        payload["projectId"] = project_id
        print("pppp", project_id)
        url = self.run_layout()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        logger.info(f"response for run_layout{response.json()}")

        time.sleep(25)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        jobId = response.json()['data']['jobId']
        logger.info(f"job id for stage2 {jobId}")
        return jobId

    def test_verify_run_layout_project_action3(self, test_run_layout_project_action3):
        jobid = test_run_layout_project_action3
        assert jobid is not None
        logger.info(f"run api for action3 executed successfully")

    def test_get_stage1_job_details_action3(self, test_login, test_run_layout_project_action3, session_csv_filename):
        jobid = test_run_layout_project_action3
        headers = self.common_header()
        test_name = "test_get_stage1_job_details_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_job_run(jobid)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(5)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"stage project details executed successfully for action3")

    @pytest.fixture(scope="class")
    def test_stage1_result_action3(self, test_login, test_create_project_action3, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_stage1_result_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        # project_id, unique_project_name, _, = test_create_project_layout
        project_id, _, _, = test_create_project_action3
        payload = payload.get_payload_stage1_result()
        payload["projectId"] = project_id
        print("payload for stage1", payload)
        print("project_id in stage1", project_id)
        logger.info(f"projectid for stage1{project_id}")
        url = self.stage1_result()
        print("url for stage1", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(55)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        response_data = response.json()
        print(f"response for stage1{response.json()}")
        filenames = [
            item["File"] for pex in response_data["data"]["PEX_Consolidated"] for item in pex["data"]
        ]

        # Get the 0th index filename
        extracted_filename = filenames[0] if filenames else None  # Handle case if list is empty

        print("Extracted 0th index filename from PEX_Consolidated:", extracted_filename)
        layout_data_list = [item["LayoutData"] for item in response_data["data"]["Items"]]
        logger.info(f"layoutdata list,{layout_data_list}")

        # Print all LayoutData entries
        for layout in layout_data_list:
            print(layout)

        return extracted_filename, response, layout_data_list

    def test_get_gds_images_stage1_action3(self, test_login, test_stage1_result_action3, session_csv_filename):
        _, _, layout_data_list = test_stage1_result_action3
        payload = Payload()
        headers = self.common_header()
        test_name = "test_get_gds_images_stage1_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        payload = payload.get_payload_gds_images()
        payload["LayoutData"] = layout_data_list
        logger.info(f"payload for gds{payload}")
        url = self.get_gds_images()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(5)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"gds images for action3 API executed successfully")

    def test_stage1_result_verification_action3(self, test_stage1_result_action3):
        """
        Test case that verifies Stage 1 API response.
        Uses the fixture `test_stage1_result`.
        """
        extracted_filename, response, _, = test_stage1_result_action3  # Unpack response and filename

        # Assertions for response verification
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.json()}"
        assert response.json() is not None, "Response JSON should not be None"
        assert extracted_filename is not None, "Extracted filename should not be None"

    def test_download_all_stage1_action3(self, test_login, test_create_project_action3, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_download_all_stage1_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_action3
        #logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_payload_stage1_download_All()
        payload["project_id"] = project_id

        print(f"payload for download{payload}")
        logger.info(f"projectid for stage1_download{project_id}")
        url = self.get_stage_download_all_layout()
        print("url for stage1_download", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(20)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        #print(response.headers)

        assert response.status_code == 200
        #Dynamically construct the expected filename
        expected_filename = f"{unique_project_name}_Stage1.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )

        # Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )
        logger.info(f"download all API executed successfully")

    def test_single_gds_download_action3(self, test_login, test_create_project_action3, test_stage1_result_action3,
                                         session_csv_filename):
        #assert self.extracted_filename is not None, "test_stage1_result must run before test_single_gds_download"
        payload = Payload()
        headers = self.common_header()
        test_name = "test_single_gds_download_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_action3
        url = self.single_gds_download()
        logger.info(f"url for single_download{url}")
        # logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_single_gds_payload()
        payload["projectId"] = project_id
        extracted_filename, _, _, = test_stage1_result_action3
        payload["fileList"] = [extracted_filename]  # Use stored filename

        print("payload for singlegds", payload)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(15)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.headers is not None
        logger.info(f"stgae1 singlegdsheaders{response.headers}")
        expected_filename = f"{extracted_filename}.zip"
        print(f"headers filename is{expected_filename}")
        assert response.status_code == 200

        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        # Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )

    def test_get_project_details_action3(self, test_login, test_create_project_action3, session_csv_filename):
        headers = self.common_header()
        test_name = "test_get_project_details_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, _, _, = test_create_project_action3
        url = self.get_project_details(project_id)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200
        logger.info(f"project details for stage3 executed successfully")

    @pytest.fixture(scope="class")
    def test_run_project_hyperexpressvity_Action3(self, test_login, test_stage1_result_action3,
                                                  test_create_project_action3, session_csv_filename):
        headers = self.common_header()
        test_name = "test_run_project_hyperexpressvity_Action3"
        headers["Authorization"] = f"Bearer {test_login}"
        stage2_project_id, _, _, = test_create_project_action3
        stage1_project, _, cell_name = test_create_project_action3
        selected_layout, _, _, = test_stage1_result_action3
        payload = Payload()
        payload = payload.get_payload_create_hyperexpressivity()
        payload["stage1Project"] = stage1_project
        payload["projectId"] = stage2_project_id
        payload["selectedLayouts"] = [selected_layout]
        payload["cells"] = cell_name
        url = self.run_layout()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        #print(response.json())
        time.sleep(50)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        jobId = response.json()['data']['jobId']
        logger.info(f"job id for stage2 {jobId}")
        logger.info(f"RUN api for action3 stage2 executed successfully")
        return jobId

    def test_get_stage2_job_details_action3(self, test_login, test_run_project_hyperexpressvity_Action3,
                                            session_csv_filename):
        jobid = test_run_project_hyperexpressvity_Action3
        headers = self.common_header()
        test_name = "test_get_stage2_job_details_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.get_job_run(jobid)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(5)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    def test_verify_project_hyper_expressivity_action3(self, test_run_project_hyperexpressvity_Action3):
        jobId = test_run_project_hyperexpressvity_Action3
        assert jobId is not None

    @pytest.fixture(scope="class")
    def test_stage2_show_result_action3(self, test_login, test_create_project_action3, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_stage2_show_result_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        # project_id, unique_project_name, _, = test_create_project_layout
        project_id, _, _, = test_create_project_action3
        payload = payload.get_payload_stage2_result()
        payload["projectId"] = project_id
        print("payload for stage2", payload)
        print("project_id in stage2", project_id)
        logger.info(f"projectid for stage1{project_id}")
        url = self.stage1_result()
        print("url for stage1", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(55)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        response_data = response.json()
        print(f"response for stage1{response.json()}")
        filenames = [
            item["File"] for pex in response_data["data"]["PEX_Consolidated"] for item in pex["data"]
        ]
        extracted_filename = filenames[0] if filenames else None  # Handle case if list is empty

        print("Extracted 0th index filename from PEX_Consolidated:", extracted_filename)
        layout_data_list = [item["LayoutData"] for item in response_data["data"]["Items"]]
        logger.info(f"layoutdata list,{layout_data_list}")
        # Print all LayoutData entries
        for layout in layout_data_list:
            print(layout)
        return extracted_filename, response, layout_data_list

    def test_verify_stage2_result_Action3(self, test_stage2_show_result_action3):
        _, response, layout_data_list = test_stage2_show_result_action3
        assert response.json() is not None
        assert response.status_code == 200
        assert layout_data_list is not None

    def test_get_project_details_stage2_action3(self, test_login, test_create_project_action3, session_csv_filename):
        headers = self.common_header()
        headers["Authorization"] = f"Bearer {test_login}"
        test_name = "test_get_project_details_stage2_action3"
        project_id, _, _, = test_create_project_action3
        url = self.get_project_details(project_id)
        response = self.get_request(url, auth=None, headers=headers, in_json=False)
        time.sleep(5)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    def test_get_gds_images_stage2_action3(self, test_login, test_stage2_show_result_action3, session_csv_filename):
        _, _, layout_data_list = test_stage2_show_result_action3
        payload = Payload()
        headers = self.common_header()
        test_name = "test_get_gds_images_stage2_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        payload = payload.get_payload_gds_images()
        payload["LayoutData"] = layout_data_list
        logger.info(f"payload for gds{payload}")
        url = self.get_gds_images()
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(5)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.json() is not None
        assert response.status_code == 200

    def test_download_all_stage2_action3(self, test_login, test_create_project_action3, session_csv_filename):
        payload = Payload()
        headers = self.common_header()
        test_name = "test_download_all_stage2_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_action3
        #logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_payload_stage2_download_All()
        payload["project_id"] = project_id

        print(f"payload for download{payload}")
        logger.info(f"projectid for stage1_download{project_id}")
        url = self.get_stage_download_all_layout()
        print("url for stage1_download", url)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(10)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        logger.info(f"{response.headers}")
        assert response.status_code == 200
        #Dynamically construct the expected filename
        expected_filename = f"{unique_project_name}_Stage2.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )

        # Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )

    def test_single_gds_download_stage2_action3(self, test_login, test_create_project_action3,
                                                test_stage2_show_result_action3, session_csv_filename):
        #assert self.extracted_filename is not None, "test_stage1_result must run before test_single_gds_download"
        payload = Payload()
        headers = self.common_header()
        test_name = "test_single_gds_download_stage2_action3"
        headers["Authorization"] = f"Bearer {test_login}"
        project_id, unique_project_name, _, = test_create_project_action3
        url = self.single_gds_download()
        # logger.info(f"unique projectname is{unique_project_name}")
        payload = payload.get_single_gds_payload_stage2()
        payload["projectId"] = project_id
        extracted_filename, _, _, = test_stage2_show_result_action3
        payload["fileList"] = [extracted_filename]  # Use stored filename

        print("payload for singlegds", payload)
        response = self.post_request(url, auth=None, headers=headers, payload=payload, in_json=False)
        time.sleep(5)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.headers is not None

        logger.info(f"headers{response.headers}")

        expected_filename = f"{extracted_filename}.zip"
        print(f"headers filename is{expected_filename}")
        assert response.headers["X-Filename"] == expected_filename, (
            f"X-Filename header value is '{response.headers['X-Filename']}', expected '{expected_filename}'."

        )
        #Verify the 'Content-Disposition' header contains the correct filename
        content_disposition = response.headers.get('Content-Disposition', '')
        assert f'filename="{expected_filename}"' in content_disposition, (
            f"Content-Disposition header value is '{content_disposition}', expected 'filename={expected_filename}'."
        )

    def test_delete_action3_project(self, test_login, test_create_project_action3, session_csv_filename):
        project_id, unique_project_name, _, = test_create_project_action3
        headers = self.common_header()
        test_name = "test_delete_action3_project"
        headers["Authorization"] = f"Bearer {test_login}"
        url = self.delete_project(project_id)
        response = self.delete_request(url, auth=None, headers=headers, in_json=False)
        status = "PASS" if response.status_code == 200 else "FAIL"
        log_test_result(test_name, url, status, session_csv_filename)
        assert response.status_code == 200
        assert response.json() is not None
        logger.info(f"delete API for action3 executed successfully")
