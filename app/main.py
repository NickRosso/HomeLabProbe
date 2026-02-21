from fastapi import FastAPI, Query
import requests
import time

app = FastAPI()

@app.get("/")
def index():
    return{"Hello": "Whoever is reading this"}

@app.get("/probe/url",
    summary="This endpoint probes the provided web app given with GET requests.",
    response_description="A dictionary of requests detailing request information and results. The key is the request counter and the value is the response information."
)
def probe_url(
    count: int = Query(..., description="Number of Requests to Send."),
    url: str = Query(..., description="Full URL including http:// or https://"),
    ssl: bool = Query(False, description="Verify SSL Certificate"),
    delay: int = Query(15, description="Time in seconds between requests"),
    back_off: int = Query(5, description="Increases time between requests each time there is a error")
):

    if not url.startswith(("http://", "https://")):
        return {"Error": "Please provide the full URL of the web app to test. i.e. https://localhost"}
    
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
    