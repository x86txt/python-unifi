# unifi/endpoints.py
import aiohttp
from unifi import config


async def fetch_m365_data(session: aiohttp.ClientSession) -> list:
    """
    Fetch Microsoft 365 JSON data from the endpoints URL.
    """
    async with session.get(config.MICROSOFT_ENDPOINT_URL) as resp:
        resp.raise_for_status()
        return await resp.json()
