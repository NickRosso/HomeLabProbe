# HomeLab Probe API

This is a small FastAPI project I built for experimenting with network probing inside my homelab. It started as a way to play with FastAPI, but it turned into a handy little tool for checking HTTP endpoints, scanning subnets, and more to come.

It’s lightweight, easy to run in Docker, and simple to extend.

---

## Features

### System Info (`GET /`)
Returns some deets of the server’s environment, including:

- Python, FastAPI, and Uvicorn versions  
- Hostname  
- Uptime  
- CPU load  
- Memory and disk usage  
- Current UTC time and epoch time  


---

### HTTP Probe (`GET /probe/url`)
Sends repeated GET requests to a URL you provide. You can control:

- Number of requests  
- SSL verification  
- Delay between requests  
- Backoff multiplier when a request fails  

Each request is logged with status code and content length in the final response. Maybe one day this can be changed to a websocket so it returns results as they come back.

---

### Subnet Probe (`GET /probe/subnet`)
Takes a Class C subnet (e.g., `192.168.1.0/28`) and runs an ICMP ping sweep across all hosts.

The subnet validation and ping logic lives in `utils.py`.

---
## Pre-reqs
Docker installed... duh


## Running Locally
The docker compose file will run the unit tests automatically.

```bash
docker compose build; docker compose up


