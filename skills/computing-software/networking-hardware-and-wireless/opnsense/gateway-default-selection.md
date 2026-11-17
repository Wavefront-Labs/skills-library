---
id: computing-software.networking-hardware-and-wireless.opnsense.gateway-default-selection
name: gateway-default-selection
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [gateways, default-gateway, priority, upstream, gateway-switching]
level: practitioner
status: docs-checked
description: "How OPNsense chooses the default gateway: priority 1-255, upstream flag, monitoring, gateway switching and the overview page."
sources: ["https://docs.opnsense.org/manual/gateways.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateways and default gateway selection

Gateways (System > Gateways > Configuration) define routes to other networks. They are either defined manually or generated from dynamic interfaces such as DHCP, which then have no preset address and names like WAN_DHCP; generated ones can still be edited. Static routes to specific networks (System > Routes > Configuration) depend on the gateways listed here. Only one default route per IP protocol (IPv4, IPv6) can exist in the routing table.

Selection works identically for both families. Priority runs from 1 (most important) to 255 (least); automatically generated gateways get a low priority by default. The Upstream flag marks a gateway as a default candidate and several may carry it. The algorithm sorts upstream gateways first, then by priority; if none is flagged upstream, the first non-upstream is used. With monitoring enabled, current status matters too: an unreachable monitor address demotes the gateway.

By default the default gateway is only re-evaluated at startup or when an interface connects or disconnects. To switch when the current gateway stops responding, enable Gateway switching in System > Settings > General. For ordered fail-over of dynamic gateways (favour fibre over 4G), set priority and the upstream flag and check the grid order.

The overview lists gateways by importance; the one marked (active) is the calculated default, which may differ from actual routing if switching is off. Check the real default in System > Routes > Status. The system only considers gateways shown on this page, so when debugging dynamic gateways confirm the expected one is listed.

## Checked

2026-11-03. Confirmed against the OPNsense Gateways manual page: priority 1 to 255, upstream flag, sort order, monitoring, Gateway switching in System > Settings > General, the (active) marker and System > Routes > Status. Nothing removed.

Method: documentation only; no commands were run.
