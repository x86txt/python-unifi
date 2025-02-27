# unifi/policy.py
import json


def extract_domains(m365_data: list) -> list:
    """
    Extract a deduplicated list of domain names (stripping any leading "*.")
    from endpoints where serviceArea or serviceAreaDisplayName is either
    "Skype" or "Microsoft Teams".
    """
    desired_areas = {"Skype", "Microsoft Teams"}
    domains = set()
    for item in m365_data:
        area = item.get("serviceArea")
        display_area = item.get("serviceAreaDisplayName")
        if area in desired_areas or display_area in desired_areas:
            for d in item.get("urls", []):
                if d.startswith("*."):
                    d = d[2:]
                domains.add(d)
    return list(domains)


async def create_policy_route(controller, conf, domains: list, console) -> None:
    """
    Create a policy-based route that directs traffic destined for the provided domains.
    Outputs a colored status update using the provided rich Console.
    """
    base_url = conf.url
    if controller.connectivity.is_unifi_os:
        base_url += "/proxy/network"
    route_url = base_url + "/v2/api/site/default/trafficroutes"

    domains_payload = [{"domain": d, "ports": [], "port_ranges": []} for d in domains]
    payload = {
        "enabled": True,
        "description": "Policy based route for Microsoft domains",
        "domains": domains_payload,
        "regions": [],
        "matching_target": "DOMAIN",
        "network_id": conf.POLICY_NETWORK_ID,
        "next_hop": "",
        "kill_switch_enabled": False,
        "target_devices": [{"type": "ALL_CLIENTS"}],
        "ip_addresses": [],
        "ip_ranges": [],
    }

    response, data = await controller.connectivity._request(
        "post", route_url, json=payload
    )
    if response.status in (200, 201):
        console.print(
            "[bright_green]Policy based route created successfully.[/bright_green]"
        )
    else:
        console.print(
            f"[light_red]Failed to create policy based route: status {response.status}[/light_red]"
        )
