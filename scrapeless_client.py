import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def extract_page_text(url: str) -> str:
    api_token = os.getenv("SCRAPELESS_API_TOKEN")
    endpoint = "https://api.scrapeless.com/api/v1/unlocker/request"

    headers = {
        "x-api-token": api_token
    }

    payload = {
        "actor": "unlocker.webunlocker",
        "proxy": {"country": "ANY"},
        "input": {
            "url": url,
            "method": "GET",
            "redirect": True,
            "js_render": True,
            "js_instructions": [
                {"wait": 5000}  # wait 5 seconds for JS-rendered content
            ],
            "block": {
                "resources": ["image", "font", "script"],
                "urls": ["https://example.com"]
            }
        }
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Scrapeless failed: {response.status_code} — {response.text}")