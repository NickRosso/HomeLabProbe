from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()

    # --- root json keys ---
    assert "app" in data
    assert "server" in data
    assert "system" in data

    # --- app json keys ---
    app_info = data["app"]
    assert app_info["name"] == "HomeLab Probe API"
    assert app_info["version"] == "1.0.0"

    # --- server json keys ---
    server = data["server"]
    assert "python_version" in server
    assert "fastapi_version" in server
    assert "uvicorn_version" in server
    assert "hostname" in server
    assert "uptime_seconds" in server
    assert "current_time_utc" in server
    assert "epoch_time" in server


    # uptime should be non-negative
    assert server["uptime_seconds"] >= 0

    # --- System section ---
    system = data["system"]
    assert "cpu_count" in system
    assert "cpu_load" in system
    assert "memory" in system
    assert "disk_usage" in system

    # cpu_count should be an int
    assert isinstance(system["cpu_count"], int)

    # cpu_load should be a tuple/list of 3 values
    assert isinstance(system["cpu_load"], (list, tuple))
    assert len(system["cpu_load"]) == 3

    # memory and disk usage should be dicts
    assert isinstance(system["memory"], dict)
    assert isinstance(system["disk_usage"], dict)

def test_probe_url_required_query_parameters():
    response = client.get("/probe/url")
    data = response.json()
    assert response.status_code == 422
    assert isinstance(data["detail"], list) # if request does not contain required parameters 
    assert len(data["detail"])== 2 #currently there are two required query parameters

@patch("app.main.time.sleep")
@patch("app.main.requests.get")
def test_probe_url_request_count(mock_get, mock_sleep):
    #creating a mock object to mimick get request and time.sleep calls. 
    # In the test we count the number of times they were called to check the underlying logic
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 500
    mock_response.content = b"error"
    mock_get.return_value = mock_response

    response = client.get("/probe/url", params={
        "count": 2,
        "url": "http://localhost:8000",
        "delay": 2, 
        "back_off": 3,
        "ssl": True
    })

    assert response.status_code == 200
    assert mock_sleep.call_count == 2
    
    response = client.get("/probe/url", params={
        "count": 10,
        "url": "http://localhost:8000",
        "delay": 2, 
        "back_off": 3,
    })

    assert response.status_code == 200
    #call_count should be total of count between the 2 requests
    assert mock_sleep.call_count == 12


def test_probe_url_missing_protocol_error():
    response = client.get("/probe/url", params={
        "count": 2,
        "url": "localhost:8000",
        "delay": 2, 
        "back_off": 3,
        "ssl": True
    })
    assert response.json() == {"Error": "Please provide the full URL of the web app to test. i.e. https://localhost"}
