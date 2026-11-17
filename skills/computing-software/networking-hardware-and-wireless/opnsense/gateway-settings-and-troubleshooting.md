---
id: computing-software.networking-hardware-and-wireless.opnsense.gateway-settings-and-troubleshooting
name: gateway-settings-and-troubleshooting
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [gateway-monitoring, dpinger, failover-states, far-gateway]
level: practitioner
status: docs-checked
description: "OPNsense gateway form fields (monitor IP, far gateway, failover and failback states) plus a checklist for missing or offline gateways."
sources: ["https://docs.opnsense.org/manual/gateways.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateway settings and troubleshooting

Gateway form fields: Disabled; Name; Description; Interface; Address Family; IP address (empty or dynamic when auto-generated); Upstream Gateway (default candidate); Far Gateway (allows the gateway outside the interface subnet); Disable Gateway Monitoring (treated as online); Disable Host Route (no dedicated host route for the monitor); Monitor IP (alternative address to probe; it must be reachable through this interface); Mark Gateway as Down (never a default candidate); Priority (lower is more important).

Failover States kills states tied to a gateway that goes down, forcing clients to reconnect over another online gateway. Failback States kills states on the lower-priority gateway when a higher-priority one returns, typical for metered LTE links that should be used only when nothing else is online. Both require default gateway switching to be enabled or the gateway to be a member of a gateway group.

Missing dynamic gateway: most dynamic interface types record their gateway in /tmp/[interface]_router or /tmp/[interface]_routerv6. If it is not listed, the interface type or remote server is probably not providing one. For some VPN types, tick Dynamic gateway policy in the interface settings so traffic can be sent without an intermediate gateway.

Gateway marked offline: first check the monitor address is reachable on the right interface with Interfaces > Diagnostics > Ping. If the monitor is outside the interface subnet, confirm a static route in System > Routes > Status sends it to the correct upstream. A dpinger process should be running (System > Diagnostics > Services). If it is, use Interfaces > Diagnostics > Packet Capture to see ICMP packets heading to the monitor address.

## Checked

2026-11-03. Confirmed against the OPNsense Gateways manual page, sections Settings and Troubleshooting: every field, failover and failback states, the /tmp router files, Dynamic gateway policy, the offline checks. Nothing removed.

Method: documentation only; no commands were run.
