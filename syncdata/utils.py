import requests
from salesvault import settings


def get_response(url):
    BASE_URL = "https://api.hubapi.com"
    url = f"{BASE_URL}{url}"
    headers = {"Authorization": f"Bearer {settings.API_KEY}"}
    response = requests.get(url, headers=headers)
    return response
