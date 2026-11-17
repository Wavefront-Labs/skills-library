---
id: computing-software.systems-network-administration.cisco-networking.trace-host-to-switch-port
name: trace-host-to-switch-port
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, find-host-port, mac-trace, mac-address-table, mac-learning, show-ip-arp, cdp-neighbors, traceroute-mac, ip-device-tracking, device-tracking]
level: practitioner
status: draft
description: "Find which switch port an IP address or MAC is plugged into: ARP on the gateway, walk the MAC table hop by hop via CDP/LLDP, traceroute mac and device-tracking shortcuts."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/116191-trouble-l2-traceroute-00.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_switch_integrated_security_features.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trace a host to its switch port

## 1. IP to MAC on the gateway
```
show ip arp 10.20.30.45
! Internet  10.20.30.45  3  0050.56aa.bb01  ARPA  Vlan30
```
No entry? `ping 10.20.30.45` from the gateway first. IPv6: `show ipv6 neighbors`.

## 2. Walk the MAC table
On the gateway switch:
```
show mac address-table address 0050.56aa.bb01
! 30  0050.56aa.bb01  DYNAMIC  Te1/1/1
show cdp neighbors Te1/1/1 detail | i Device|IP address|Port
```
SSH to that neighbour and repeat until the port is an **access** port (no CDP/LLDP
neighbour, or a phone neighbour) instead of an uplink or Port-channel.

## 3. Shortcuts
- **Layer 2 traceroute** (needs CDP on all switches in the path, same VLAN):
  `traceroute mac 0050.56aa.bb01 0011.2233.4455 vlan 30` or by IP
  `traceroute mac ip 10.20.30.45 10.20.30.1`.
- **Device tracking (SISF)** on IOS XE access switches, if enabled by DHCP snooping/IPDT:
  `show device-tracking database address 10.20.30.45` gives the port directly.
- **NMS**: LibreNMS/NetBox/NetDisco "find MAC" indexes ARP and MAC tables from all devices.

## Gotchas
- Behind an IP phone, the PC MAC is in the data VLAN and the phone MAC in the voice VLAN on the
  same port. That is the access port you want.
- A MAC seen on a Port-channel: look at the neighbour on any member, not the Po.
- Virtual machines: the port leads to the hypervisor uplink; continue in vCenter/Proxmox.
- Wireless clients appear on the AP's port or on the WLC (central switching); use the WLC
  client table instead.
- Randomised MACs (phones, laptops on Wi-Fi) change per SSID; trace soon after the event.

## Verify
- [ ] The final port shows no switch neighbour and the MAC is the only (or phone + PC) entry.
- [ ] `shutdown` test (if allowed) drops the host's ping, confirming the port.
- [ ] Record the port in the ticket or source of truth.
