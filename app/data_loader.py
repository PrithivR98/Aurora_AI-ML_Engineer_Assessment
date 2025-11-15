# app/data_loader.py

import httpx

BASE_URL = "https://november7-730026606190.europe-west1.run.app"
MESSAGES_ENDPOINT = "/messages"

async def fetch_messages():
    """
    Fetch all messages from the remote API.
    """
    url = BASE_URL + MESSAGES_ENDPOINT

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    # API returns: {"total": ..., "items": [ ... ]}
    if isinstance(data, dict) and "items" in data:
        return data["items"]

    raise RuntimeError(f"Unexpected /messages response: {data}")
