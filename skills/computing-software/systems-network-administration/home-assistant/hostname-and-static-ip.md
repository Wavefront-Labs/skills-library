---
id: computing-software.systems-network-administration.home-assistant.hostname-and-static-ip
name: hostname-and-static-ip
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [hostname, static-ip, dhcp-reservation]
level: practitioner
status: docs-checked
description: "Change the Home Assistant OS hostname and set a static IPv4 address in Settings > System > Network, or use a DHCP reservation on the router."
sources:
  - https://www.home-assistant.io/docs/configuration/network/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give Home Assistant a stable name and address on the LAN.

These settings are available only on Home Assistant Operating System and need administrator rights. On Home Assistant Container, the host operating system manages the network.

Change the hostname (default `homeassistant`, reachable as `homeassistant.local`):

1. Go to Settings > System > Network.
2. In Hostname, enter the new name and select Save.
3. Reboot the system.
4. Open it with the new name, for example `kitchen.local`. Keep the same `http://` or `https://` and port.

Use unique hostnames if you run more than one instance.

Set a static IP address. The router normally assigns the address, which can change after a router restart. Alternatively reserve the address in the router (a DHCP reservation).

1. Pick an unused address outside the router's automatic range, and note the router (gateway) address.
2. Go to Settings > System > Network.
3. Under Configure network interfaces, select the tab, for example `eth0`.
4. Expand IPv4 and select Static (for IPv6 use the IPv6 section, which uses Subnet prefix instead of Netmask).
5. Enter IP address, Netmask (for example `255.255.255.0`), Gateway address, and a DNS server, or choose Custom and enter the router address.
6. Save.

## Checked

2026-11-04. Confirmed against the Network configuration page. Nothing removed.

Method: documentation only; no commands were run.
