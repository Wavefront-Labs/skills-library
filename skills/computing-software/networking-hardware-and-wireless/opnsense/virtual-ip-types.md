---
id: computing-software.networking-hardware-and-wireless.opnsense.virtual-ip-types
name: virtual-ip-types
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [virtual-ip, ip-alias, proxy-arp, carp]
level: practitioner
status: docs-checked
description: "OPNsense Virtual IP modes (IP Alias, CARP, Proxy ARP) and the settings form: VHID, peer, gateway, expansion, service binding."
sources: ["https://docs.opnsense.org/manual/firewall_vip.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Virtual IP types and settings

Virtual IPs (Interfaces > Virtual IPs) add extra addresses to an existing interface for NAT, service binding or high availability.

Modes:
- IP Alias: a normal extra address. It answers ping and generates ARP like a real interface address, can bind services and be used in NAT. The mask usually matches the interface or is a single address (/32 or /128). It can join a CARP group by setting the same VHID.
- CARP: an address for a high availability cluster, behaving as a normal address while the node is MASTER. Needs a VHID Group.
- Proxy ARP: adds no address; the system answers ARP requests via choparp so clients believe the address is local.

Key fields: Interface; Type (Network or Single address, relevant only for NAT, where Proxy ARP plus Expansion generates a separate address for every item in the netmask); Address with netmask; Deny service binding (services on the interface automatically include the VIP unless this is checked); Peer IPv4/IPv6 (24.7 and later, CARP destination for announcements, multicast by default, unicast possible where multicast is blocked such as some cloud providers); Gateway (IP Alias only, normally empty except for tunnel types like ppp, pppoe and tun that need one); Disable Expansion (stops a network entry such as 192.168.1.0/24 from expanding to 256 entries in NAT lists); Virtual IP Password (encrypts CARP packets, must match across nodes); VHID Group 1 to 255 (identical on all members); Advertising Frequency with base in seconds and skew, where higher skew means less preferred; Description.

Keep a separate VHID per interface for easier debugging, although the protocol only needs uniqueness within the interface's broadcast domain.

## Checked

2026-11-03. Read the Virtual IPs manual page (firewall_vip.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
