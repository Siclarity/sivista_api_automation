import pytest
import json
from src.helpers.payload_manager import Payload
#from src.helpers.utils import common_header
from src.constants.basePage import Baseclass
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)



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
