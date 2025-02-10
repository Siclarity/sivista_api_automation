import pytest
import json
from src.helpers.payload_manager import Payload
#from src.helpers.utils import common_header
from src.constants.basePage import Baseclass
import logging
# conftest.py
import os
import pandas as pd
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)




# Setup logging
logger = logging.getLogger(__name__)

# Define the base directory to store results
RESULTS_DIR = "Results_csv"
os.makedirs(RESULTS_DIR, exist_ok=True)


# Function to generate a CSV filename based on the current timestamp
def generate_csv_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(RESULTS_DIR, f"{timestamp}API_Automation_Results.csv")


# Function to log the test results in the CSV
def log_test_result(test_name, endpoint_url, status, csv_filename):
    df = pd.DataFrame([{
        "Test_Case_Name": test_name,
        "Endpoint_URL": endpoint_url,
        "Result": status
    }])
    # Append the new result to the CSV file
    df.to_csv(csv_filename, mode='a', header=False, index=False)


# Fixture to create a new CSV file for each session based on timestamp
@pytest.fixture(scope="session", autouse=True)
def session_csv_filename():
    """
    Fixture that will run once per session and generate a unique CSV filename
    based on the timestamp.
    """
    # Generate the CSV filename based on the timestamp
    csv_filename = generate_csv_filename()

    # Create the CSV file with headers if it doesn't exist
    if not os.path.exists(csv_filename):
        df = pd.DataFrame(columns=["Test_Case_Name", "Endpoint_URL", "Result"])
        df.to_csv(csv_filename, index=False)

    yield csv_filename

    # Optionally log that session is complete or clean up (if needed)
    logger.info(f"Test results saved to: {csv_filename}")


# Fixture to log test results for each test case
def pytest_runtest_makereport(item, call):
    """
    Capture the test result after each test run and log it to the CSV file.
    """
    if call.when == "call":  # Only log after the test call (not before or during setup/teardown)
        test_name = item.nodeid
        status = "PASS" if call.excinfo is None else "FAIL"

        # Capture the URL from the test if it's available
        url = item.funcargs.get('url', None)

        # Log the result in the CSV for this session
        if url:
            log_test_result(test_name, url, status, item.session._csv_filename)


@pytest.fixture(scope="session")
def test_login():
    base = Baseclass()
    payload = Payload()
    login_url = base.get_user_login()
    headers = base.common_header()

    """
    Pytest fixture to log in and retrieve the access token.
    """
    payload = payload.get_payload_auth()

    response = base.post_request(login_url, auth=None, headers=headers, payload=payload, in_json=False)
    print("Payload:", payload)
    print("Response:", response.json())

    access_token = response.json().get("token", {}).get("access")
    if not access_token:
        pytest.fail("Login failed. No access token retrieved.")
    print("Access Token:", access_token)
    return access_token
