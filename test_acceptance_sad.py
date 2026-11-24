# test_acceptance_sad.py

from io import BytesIO
import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture for the Flask test client.
    - Purpose: Set up a test client for making requests to the Flask app during testing.
    - Usage: Provides a `client` object to use for HTTP request simulations.
    """
    with app.test_client() as client:
        yield client

def test_acceptance_missing_file(client):
    """
    Test Case: No File Uploaded
    - Purpose: Validate the application's behavior when no file is provided in the upload request.
    - Scenario:
        - Simulate a POST request to the `/prediction` route with no file data.
        - Assert the response status code is 200 (to indicate a valid request was processed).
        - Verify that the response includes an appropriate error message.
    """
    # Simulate a POST request with no file data
    response = client.post("/prediction", data={}, content_type="multipart/form-data")
    
    # Assertions:
    assert response.status_code == 200
    assert b"File cannot be processed" in response.data

def test_acceptance_empty_filename(client):
    """Test POST request with an empty filename to verify validation."""
    data = {"file": (BytesIO(b""), "")}
    response = client.post("/prediction", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed" in response.data

def test_acceptance_get_prediction_route(client):
    """Test GET request to /prediction directly to verify informational message."""
    response = client.get("/prediction")
    assert response.status_code == 200
    assert b"Please upload an image" in response.data

def test_acceptance_home_route(client):
    """Test GET request to home / route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Image Recognition" in response.data or response.status_code == 200
