---
id: computing-software.networking-hardware-and-wireless.opnsense.dhcp-server-options
name: dhcp-server-options
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [dhcp, dnsmasq, kea, isc-dhcp, dhcrelay]
level: practitioner
status: docs-checked
description: "Choose between Dnsmasq, KEA, DHCRelay and legacy ISC for DHCPv4/v6 on OPNsense, and where to place static reservations."
sources: ["https://docs.opnsense.org/manual/dhcp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing a DHCP service

OPNsense offers four DHCP options. Dnsmasq (default) is a lightweight DNS, router advertisement and DHCP server with a small cache, static assignments, multiple networks, custom options and DHCPv6 with prefix-delegation-based allocation; it is recommended for small and medium setups, under about 1000 unique clients, and is the default for DHCPv4, DHCPv6 and RA. KEA is ISC's modular successor, handling DHCPv4 and DHCPv6, suited to larger or HA setups (over 1000 clients) or when you need API-driven configuration. It has no DNS or RA features and no dynamic lease registration into Unbound. DHCRelay forwards requests from one interface to a server on another network and supports multiple upstreams; it binds port 67 like the others, so use strict interface binding if available to run them side by side. ISC DHCP is end-of-life with no security patches; migrate to KEA or Dnsmasq. For Router Advertisements on IPv6 use radvd or Dnsmasq.

Reservations are supported by ISC, KEA and Dnsmasq, inside or outside the pool. Rules differ: with Dnsmasq define reservations inside the dynamic pool, where the address is fully held back from dynamic clients. With ISC and KEA define them outside the pool; inside the pool the server may hand the address to another client whenever the reserved client is offline.

## Checked

2026-11-03. Read the DHCP manual page (dhcp.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
