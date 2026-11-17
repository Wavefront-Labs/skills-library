---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.dhcp-and-arp-for-host-attribution
name: dhcp-and-arp-for-host-attribution
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [dhcp-forensics, arp, host-attribution, mac-address, ip-to-host, dhcp-options, wireshark, dfir]
level: practitioner
status: draft
description: "Attribute IPs to physical hosts and users at a point in time using DHCP leases and options, ARP traffic and server logs, and detect ARP spoofing."
sources: ["https://datatracker.ietf.org/doc/html/rfc2131", "https://wiki.wireshark.org/DHCP", "https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-top"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCP and ARP for host attribution

**Goal:** answer "which machine had IP 10.1.4.77 at 14:32 UTC" so network alerts and logs
can be tied to a device, its hostname and ultimately a user.

## DHCP in captures
Filter `dhcp` (older Wireshark: `bootp`). Message types (`dhcp.option.dhcp`): 1 Discover,
2 Offer, 3 Request, 5 ACK, 6 NAK, 7 Release, 8 Inform.
Useful fields and columns:
- `dhcp.hw.mac_addr` client MAC (vendor OUI identifies manufacturer, randomised MACs set the
  locally-administered bit: second hex digit 2, 6, A or E)
- `dhcp.option.hostname` (option 12) client hostname
- `dhcp.option.requested_ip_address` (option 50), `dhcp.ip.your` (assigned IP in ACK)
- `dhcp.option.vendor_class_id` (option 60, e.g. `MSFT 5.0`, `android-dhcp-14`)
- `dhcp.option.client_id` (option 61), `dhcp.option.ip_address_lease_time` (option 51)
- option 81 (FQDN) for dynamic DNS registration
- Parameter request list (option 55) order is OS-specific: passive OS fingerprinting.

## ARP
- `arp.opcode == 1` request, `2` reply; `arp.src.hw_mac` and `arp.src.proto_ipv4` give MAC/IP
  pairs.
- Wireshark flags conflicts: `arp.duplicate-address-detected` or `arp.duplicate-address-frame`.
- **ARP spoofing** (MITM): one MAC claiming the gateway's IP, gratuitous ARP replies storms,
  a MAC mapping to many IPs. Compare with the gateway's real MAC from switch/router data.

## Server-side sources (often all you have)
- Windows DHCP server logs `%windir%\System32\dhcp\DhcpSrvLog-<Day>.log` (one per weekday,
  overwritten weekly: collect quickly) with event IDs 10 (new lease), 11 (renew), 12
  (release), 30 (DNS update); also the DHCP-Server operational event log.
- ISC/Kea DHCP: `dhcpd.leases`, syslog lines `DHCPACK on 10.1.4.77 to aa:bb:cc:...`.
- Switch CAM tables / 802.1X RADIUS logs map MAC to switch port and authenticated user;
  wireless controller logs map MAC to user and access point.

## Chain of attribution
IP + time -> DHCP lease -> MAC + hostname -> asset inventory / AD computer object -> logged-on
user at that time (4624 on the host, EDR, VPN logs). Mind NAT: behind a proxy or NAT, the
external IP maps to many hosts; you need the translation logs.

## Gotchas
- Static IPs never appear in DHCP; use ARP and switch tables.
- MAC randomisation on phones and Windows (per-network random MACs) weakens MAC-based
  attribution over time.
- Clock skew between DHCP server, sensor and SIEM: confirm offsets.

## Self-check
Your attribution statement cites lease start/end covering the event time, MAC, hostname and
the source used to link to a user.
