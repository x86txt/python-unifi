import json


async def create_firewall_groups(controller, conf, m365_data: list, console) -> None:
    """
    Filter endpoints for IPv4 subnets (ignoring IPv6) for service areas
    "Skype" or "Microsoft Teams", then create a UniFi firewall group for each.
    For /32 subnets, remove the /32 so the IP is treated as a single host.
    Outputs a colored status update via the provided rich Console.
    """
    desired_areas = {"Skype", "Microsoft Teams"}
    filtered_subnets = set()
    for item in m365_data:
        area = item.get("serviceArea")
        display_area = item.get("serviceAreaDisplayName")
        if area in desired_areas or display_area in desired_areas:
            for ip in item.get("ips", []):
                # Only include IPv4 addresses (skip IPv6, which contain ":")
                if "/" in ip and ":" not in ip:
                    filtered_subnets.add(ip)
    filtered_subnets = list(filtered_subnets)
    console.log(
        f"[grey]Filtered IPv4 subnets (deduplicated): {filtered_subnets}[/grey]"
    )

    base_url = conf.url  # Uses the read-only property from aiounifi Configuration.
    if controller.connectivity.is_unifi_os:
        base_url += "/proxy/network"
    fw_endpoint = f"/api/s/{conf.site}/rest/firewallgroup"
    unifi_fw_url = base_url + fw_endpoint

    for subnet in filtered_subnets:
        if subnet.endswith("/32"):
            member = subnet.split("/")[0]
            name = f"MS365_{member}"
        else:
            member = subnet
            name = f"MS365_{subnet}"
        payload = {
            "name": name,
            "group_type": "address-group",
            "group_members": [member],
        }
        response, data = await controller.connectivity._request(
            "post", unifi_fw_url, json=payload
        )
        if response.status in (200, 201):
            console.print(
                f"[bright_green]Created firewall group: {name}[/bright_green]"
            )
        elif response.status == 400:
            try:
                msg = data.decode()
            except Exception:
                msg = str(data)
            if "api.err.FirewallGroupExisted" in msg:
                console.print(f"[yellow]Firewall group exists: {name}[/yellow]")
            else:
                console.print(f"[light_red]Error creating {name}: {msg}[/light_red]")
        else:
            console.print(
                f"[light_red]Error creating {name}: status {response.status}[/light_red]"
            )
