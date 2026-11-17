---
id: computing-software.networking-hardware-and-wireless.opnsense.static-routes-and-routing-table
name: static-routes-and-routing-table
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [static-routes, routing-table, route-flags, traceroute]
level: intro
status: docs-checked
description: "Define static routes on OPNsense and read System > Routes > Status columns and flag letters."
sources: ["https://docs.opnsense.org/manual/routes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Static routes and the routing table

When a packet arrives for a network not directly attached, the firewall consults its routing table to pick a gateway (see System > Gateways). Static routes under System > Routes > Configuration teach it a path to a specific network, for instance how a client reaches a private network behind a second router. Fields: Disabled (temporary), Network Address (destination), Gateway, Description. The gateway must already exist in the gateway list.

Do not add static routes manually for services that maintain the routing table themselves; OpenVPN manages its own routes, for example. Use Interfaces > Diagnostics > Trace Route to check which path traffic actually takes.

Status page columns: Proto (IPv4 or IPv6), Destination, Gateway, Flags, Use (packets sent over the route), MTU, Netif and Netif (name), Expire (zero means never).

Key flag letters: U route usable, G destination is a gateway, H host entry (otherwise a net), S manually added (static), D created dynamically by redirect, M modified dynamically, R host or net unreachable (reject), B blackhole (discard packets during updates), b broadcast address, L valid link-address translation, C cloning (generates new routes on use), X external daemon resolves the name. Flags 1, 2 and 3 are protocol specific; c, d are protocol cloning and message confirmed.

The Logs tab collects routing related messages such as radvd and rtsold output, useful when debugging IPv6 route and router advertisement problems.

## Checked

2026-11-03. Read the Routes manual page (routes.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
