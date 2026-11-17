---
id: computing-software.networking-hardware-and-wireless.opnsense.dhcp-relay
name: dhcp-relay
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [dhcrelay, dhcp-relay, agent-information]
level: practitioner
status: docs-checked
description: "Configure DHCP relay on OPNsense: reusable destinations, relay entries per interface, agent information and the port 67 binding caveat."
sources: ["https://docs.opnsense.org/manual/dhcrelay.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DHCP relay (dhcrelay)

DHCP relaying forwards requests arriving on one interface to a DHCP server in another network, for DHCPv4 and DHCPv6. Configure it under Services > DHCRelay. The relay binds port 67 like the other DHCP servers, so to run several services side by side use strict interface binding if available.

Two object types:

Destinations are reusable targets. Fields: Name (descriptive) and Server, a comma-separated list of IPs to forward to. A destination can be IPv4 or IPv6 exclusively, not mixed.

Relays tie an interface to a destination. Fields: Enable; Interface (only interfaces with an Ethernet address can be chosen, and only one interface per destination per address family is allowed); Destination (pick from the defined pool); Agent Information, which appends the circuit ID (interface number) and agent ID to the DHCP request so the central server can tell where it came from.

A typical layout: define one destination for the central server, then add one relay for each client-facing VLAN interface pointing to it. The DHCP overview notes DHCRelay is lightweight and suited to centralized servers serving many segments.

## Checked

2026-11-03. Read the DHCRelay and DHCP manual pages (dhcrelay.html, dhcp.html) on docs.opnsense.org and confirmed the claims above against them. Removed: advice about firewall rules, routing and disabling local DHCP services that the pages do not state.
Method: documentation only; no commands were run.
