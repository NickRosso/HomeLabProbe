from fastapi import FastAPI, Query, HTTPException
from fastapi import __version__ as fastapi_version
import uvicorn
import requests
import time
import platform
import socket
import psutil
import datetime
import ipaddress

app = FastAPI()
start_time = datetime.datetime.now(datetime.UTC)

@app.get("/",
    summary="Welcome to the Homelab Probe API. This is a playground for messing with Fast API"
    " and trying different methodologies. This endpoint provides interesting system and server information."
)
def index():
    return{
        "app": {
            "name": "HomeLab Probe API",
            "version": "1.0.0",
        },
        "server": {
            "python_version": platform.python_version(),
            "fastapi_version": fastapi_version,
            "uvicorn_version": uvicorn.__version__,
            "hostname": socket.gethostname(),
            "uptime_seconds": (datetime.datetime.now(datetime.UTC) - start_time).seconds,
            "current_time_utc": datetime.datetime.now(datetime.UTC).isoformat(),
            "epoch_time": int(time.time())
        }, 
        "system": { 
            "cpu_count": psutil.cpu_count(),
            "cpu_load": psutil.getloadavg(),
            "memory": psutil.virtual_memory()._asdict(),
            "disk_usage": psutil.disk_usage("/")._asdict(), 
            }
        }

@app.get("/probe/url",
    summary="This endpoint probes the provided web app given with GET requests.",
    response_description="A dictionary of requests detailing request information and results. The key is the" \
    " request counter and the value is the response information."
)
def probe_url(
    count: int = Query(..., description="Number of Requests to Send."),
    url: str = Query(..., description="Full URL including http:// or https://"),
    ssl: bool = Query(False, description="Verify SSL Certificate"),
    delay: int = Query(15, description="Time in seconds between requests"),
    back_off: int = Query(5, description="Increases time between requests each time there is a error")
):

    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Error please provide the full URL of the web app to test. i.e. https://localhost")

    
    responses = {}
    print(f"Making {count} GET request(s)")
    for counter in range(0, count):
        response = requests.get(url, verify=ssl)
        responses[counter] = {
            "Type": "GET", 
            "URL": url,
            "status": response.status_code, 
            "content_length": len(response.content)
        }
        if not response.ok:
            delay *= back_off # Increase delay by back_off
            
        time.sleep(delay)

    return responses
    
@app.get("/probe/subnet",
    summary="This checks and does a ICMP ping on all hosts in a Class C subnet.",
    response_description="Returns all of the IPs that responded"
)
def probe_subnet(
    subnet: str = Query(..., description="Subnet such as 192.168.1.0/28. Must be a Class C Subnet.")
):
    try: 
        network = ipaddress.ip_network(subnet, strict=True) 
    except ValueError: 
        raise HTTPException(status_code=400, detail="Invalid subnet format. Use CIDR notation like 192.168.1.0/28.")
    print(network)