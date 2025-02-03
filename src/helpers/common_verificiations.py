def verify_status_code(response_data, expected_data):
    assert response_data.status_code == int \
        (expected_data), f"Expected http status {expected_data}, but got {response_data.status_code}"


def verify_key(response_data, key):
    assert key != 0, "key is not empty" + key
    assert key > 0, "key should be greater than zero" + key
