---
id: computing-software.cybersecurity-defensive.network-defence.dhcp-snooping-and-dynamic-arp-inspection
name: dhcp-snooping-and-dynamic-arp-inspection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-access-control, dhcp-snooping, dynamic-arp-inspection, dai, ip-source-guard, rogue-dhcp, arp-spoofing, layer-2-security]
level: practitioner
status: draft
description: "Stop rogue DHCP servers and ARP spoofing with DHCP snooping, Dynamic ARP Inspection and IP Source Guard, including trusted ports and rate limits."
sources: ["Cisco Catalyst Security Configuration Guide (DHCP snooping, DAI, IP Source Guard)", "NSA Network Infrastructure Security Guide", "CompTIA Security+ SY0-701 objective 2.4 (on-path attacks)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCP snooping and Dynamic ARP Inspection

**Goal:** a device on an access port cannot hand out DHCP leases or poison ARP caches to
intercept other users' traffic (on-path attacks).

## DHCP snooping
Builds a binding table (MAC, IP, VLAN, port) from legitimate DHCP exchanges and drops DHCP
server messages from untrusted ports.
```
ip dhcp snooping
ip dhcp snooping vlan 100,110
no ip dhcp snooping information option        ! if the DHCP server rejects option 82
interface GigabitEthernet1/0/48               ! uplink towards real DHCP server/relay
 ip dhcp snooping trust
interface range GigabitEthernet1/0/1 - 47
 ip dhcp snooping limit rate 15               ! packets per second, stops starvation
```

## Dynamic ARP Inspection (DAI)
Validates ARP packets against the snooping binding table; drops ARP replies claiming an IP
that the sender does not own.
```
ip arp inspection vlan 100,110
ip arp inspection validate src-mac dst-mac ip
interface GigabitEthernet1/0/48
 ip arp inspection trust
```
Static IP devices (servers, printers) need ARP ACLs or static bindings (`ip source binding ...`)
or they lose connectivity.

## IP Source Guard
`ip verify source` on access ports filters IP traffic whose source does not match the binding:
stops IP spoofing from access ports.

## Rollout
1. Enable snooping and let the binding table populate for a full lease period.
2. Add static bindings/ARP ACLs for static devices.
3. Enable DAI per VLAN in a pilot; monitor `show ip arp inspection statistics` and logs.
4. Then IP Source Guard.

## Gotchas
- Forgetting to trust the uplink/relay port breaks DHCP for the whole VLAN.
- Switch reload loses the binding table unless stored (`ip dhcp snooping database flash:snoop.db`).
- Wireless and virtual environments need equivalent features on the WLC / vSwitch.

## Verify
- [ ] `show ip dhcp snooping binding` populated; rogue DHCP server on a test port gets no clients.
- [ ] ARP spoofing test in a lab VLAN is dropped and logged.
