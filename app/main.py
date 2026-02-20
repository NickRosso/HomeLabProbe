from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def index():
    return{"Hello": "World"}

@app.get("/probe/url")
def probe_url(
    count: int,
    url: str,
    ssl: bool = False
):
    """
    This endpoint probes the provided web app given with GET requests."
    Args:
        :param count: number of requests to made
        :type count: int
        :param url: https or http url of the URL
        :type url: str
        :param ssl: Selects to make requests with insecure flag. True uses SSL, False does not.
        :type ssl: bool
    Returns:
        A list dictionary of requests detailing request information and results.
    """
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

    return responses
    