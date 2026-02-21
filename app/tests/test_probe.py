from app.main import app
from fastapi.testclient import TestClient
import time

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



