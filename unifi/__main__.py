import asyncio
import aiohttp
from aiounifi.models.configuration import Configuration
from aiounifi.controller import Controller
from unifi.endpoints import fetch_m365_data
from unifi.firewall import create_firewall_groups
from unifi.policy import extract_domains, create_policy_route
from unifi import config

# Import rich classes for fancy output.
from rich.console import Console


async def main():
    console = Console()
    async with aiohttp.ClientSession() as session:
        # ----- UniFi Controller Setup using aiounifi Configuration -----
        conf = Configuration(
            session=session,
            host=config.UNIFI_HOST,
            username=config.DUMMY_USERNAME,
            password=config.DUMMY_PASSWORD,
            port=config.UNIFI_PORT,
            site=config.UNIFI_SITE,
            ssl_context=False,  # For self-signed certs; use a proper SSLContext in production.
        )
        # Add extra attributes for policy.
        conf.POLICY_NETWORK_ID = config.POLICY_NETWORK_ID
        conf.POLICY_DESCRIPTION = config.POLICY_DESCRIPTION

        controller = Controller(conf)
        controller.connectivity.headers = {
            "X-API-KEY": config.API_KEY,
            "Accept": "application/json",
        }
        await controller.connectivity.check_unifi_os()

        # ----- Fetch Microsoft 365 JSON Data -----
        m365_data = await fetch_m365_data(session)

        # ----- Create Firewall Groups for IPv4 Subnets -----
        await create_firewall_groups(controller, conf, m365_data, console)

        # ----- Extract Domains and Create Policy Based Route -----
        domains_list = extract_domains(m365_data)
        console.print(f"[grey]Filtered domains:[/grey] {domains_list}")
        await create_policy_route(controller, conf, domains_list, console)


asyncio.run(main())
