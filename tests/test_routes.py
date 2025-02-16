import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import json
from pathlib import Path

client = TestClient(app)

# Create a test data directory
TEST_DATA_DIR = Path("test_data")
TEST_DATA_DIR.mkdir(exist_ok=True)

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    os.environ["DATA_DIR"] = str(TEST_DATA_DIR)
    
    yield
    
    # Teardown
    for file in TEST_DATA_DIR.glob("*"):
        file.unlink()
    TEST_DATA_DIR.rmdir()

def test_run_endpoint_weekday_count():
    # Create test data
    dates_file = TEST_DATA_DIR / "dates.txt"
    dates_file.write_text("2024-02-14\n2024-02-21\n2024-02-28\n")  # All Wednesdays
    
    response = client.post("/run", params={
        "task": "Count Wednesdays in /data/dates.txt and write to /data/dates-wednesdays.txt"
    })
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify result
    result_file = TEST_DATA_DIR / "dates-wednesdays.txt"
    assert result_file.read_text().strip() == "3"

def test_run_endpoint_invalid_path():
    response = client.post("/run", params={
        "task": "Read file from /etc/passwd"
    })
    
    assert response.status_code == 400
    assert "Invalid file path" in response.json()["detail"]

def test_read_endpoint():
    # Create test file
    test_file = TEST_DATA_DIR / "test.txt"
    test_file.write_text("Hello, World!")
    
    response = client.get("/read", params={"path": "/data/test.txt"})
    
    assert response.status_code == 200
    assert response.text == "Hello, World!"

def test_read_endpoint_file_not_found():
    response = client.get("/read", params={"path": "/data/nonexistent.txt"})
    
    assert response.status_code == 404