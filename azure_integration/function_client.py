import os
import requests


def send_alert_to_function(payload: dict) -> dict:
    url = os.getenv("AZURE_FUNCTION_URL")
    if not url:
        raise RuntimeError("Defina AZURE_FUNCTION_URL com a URL completa da Function (incluindo ?code=...).")

    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
