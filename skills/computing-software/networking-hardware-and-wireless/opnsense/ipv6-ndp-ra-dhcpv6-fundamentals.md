---
id: computing-software.networking-hardware-and-wireless.opnsense.ipv6-ndp-ra-dhcpv6-fundamentals
name: ipv6-ndp-ra-dhcpv6-fundamentals
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ipv6, ndp, router-advertisement, dhcpv6, slaac]
level: advanced
status: docs-checked
description: "IPv6 building blocks as OPNsense uses them: NDP, RS/RA flags M and O, rtsold, DHCPv6 ports and prefix delegation, address categories."
sources: ["https://docs.opnsense.org/manual/ipv6.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPv6 fundamentals on OPNsense

Neighbour discovery (NDP) replaces ARP: Neighbor Solicitation is ICMPv6 type 135 and Advertisement type 136; view the table at Interfaces > Diagnostics > NDP Table. A dynamically configured host sends a Router Solicitation (type 133) and expects a Router Advertisement (type 134). On OPNsense the rtsold service sends the solicitations; the kernel also handles advertisements when accept_rtadv is enabled on the interface. A DHCPv6 client runs after the router solicitation process.

An RA normally comes from a link-local (FE80::/10) source which clients use as default gateway. Flags: M (Managed) means addresses come from DHCPv6; O (Other) means other info such as DNS comes from DHCPv6. Options: prefix information (type 3, flag A allows SLAAC), recursive DNS server (type 25), route information (type 24). Clients on the LAN need an RA daemon from OPNsense: radvd or dnsmasq.

DHCPv6 clients listen on UDP port 546 and servers on UDP 547. DHCPv6 does not handle routing and depends on RAs first. It can also delegate prefixes (PD): the ISP usually hands OPNsense a prefix larger than /64 (for example /48) for attached networks, and the DHCP client configures LAN addresses from it, which is the "tracking" setting on the LAN interface. Without a PD from the provider reliable routing is not possible; proxying NDP (RFC 4389), implemented by ndp-proxy-go, can be an option. The firewall itself expects a global unicast address on WAN, so the IA_NA option is used.

Address categories: GUA 2000::/3 global unicast, ULA FC00::/7 unique local, LL FE80::/10 link-local.

## Checked

2026-11-03. Confirmed against the OPNsense IPv6 setup manual page, section Technical background: ICMPv6 types 133 to 136, rtsold, accept_rtadv, RA flags and option types, UDP 546 and 547, prefix delegation, ndp-proxy-go, IA_NA, address categories. Removed: the WAN flow sequence, which the page shows only in a diagram.

Method: documentation only; no commands were run.
