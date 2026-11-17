---
id: computing-software.networking-hardware-and-wireless.opnsense.ipv6-interface-modes
name: ipv6-interface-modes
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ipv6-modes, track-interface, slaac, 6rd, link-local]
level: advanced
status: docs-checked
description: "Choose the right OPNsense IPv6 interface mode: None, Static, DHCPv6, SLAAC, 6to4, 6rd, Identity Association, Track Interface and Link Local."
sources: ["https://docs.opnsense.org/manual/ipv6.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPv6 interface configuration modes

Pick the mode that matches your ISP; ask the ISP or the forum if unsure.

- None: IPv6 off for the interface (WAN or LAN). Use it when DHCPv6 (the default) breaks connectivity.
- Static IPv6 (WAN or LAN): assign a /64 to WAN and other /64s to LANs; bigger networks can be delegated to downstream routers. A gateway address from the ISP must be created and set.
- DHCPv6 (WAN only): default for a preset WAN; acquires a prefix and optionally an address. A single global address comes via DHCPv6 and/or SLAAC, and routing uses the ISP's link-local next hop. "Request prefix only" may be needed if the ISP refuses a prefix. The interface does not assign itself a /64 from the prefix.
- SLAAC (WAN only): stateless autoconfiguration for connectivity only.
- 6to4 Tunnel (WAN only): RFC 3056 IPv6 over IPv4 to a fixed router; rarely used now.
- 6rd Tunnel (WAN only): generalised 6to4 with a configurable prefix; the DHCP-delivered configuration is not parsed.
- Identity Association (LAN only): assigns a /64 from a WAN DHCPv6 interface but does not auto-configure radvd or dnsmasq; set up DHCPv6 and RAs yourself.
- Track Interface, legacy (LAN only): assigns a /64 from the WAN and by default configures RAs and DHCPv6 including delegation if room remains. "Manual configuration" gives static-like control. Two settings matter: Assign prefix ID (sla-id) on the LAN picks the network number, and Prefix delegation size (sla-len) on the WAN sets the prefix size for attached networks (default /64).
- Link Local (WAN or LAN): link-local address only, no RA processing, no SLAAC or automatic routes. Advanced uses: distributing a larger prefix received by static or BGP routes (set LAN to link-local and use KEA for DHCPv6-PD) and NDP proxying.

## Checked

2026-11-03. Confirmed against the OPNsense IPv6 setup manual page, section Interface configuration modes: every mode, its WAN/LAN scope, sla-id and sla-len, and the Link Local uses. Nothing removed.

Method: documentation only; no commands were run.
