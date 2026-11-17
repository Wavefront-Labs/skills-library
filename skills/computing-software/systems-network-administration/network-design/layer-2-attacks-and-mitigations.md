---
id: computing-software.systems-network-administration.network-design.layer-2-attacks-and-mitigations
name: layer-2-attacks-and-mitigations
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-attacks, mac-flooding, arp-spoofing, on-path-attack, rogue-dhcp, vlan-hopping, stp-attack, dhcp-starvation, port-security, dhcp-snooping, dynamic-arp-inspection, bpduguard, layer-2-security]
level: practitioner
status: draft
description: "Map each LAN attack (MAC flooding, ARP spoofing, rogue/starvation DHCP, VLAN hopping, STP root takeover) to its symptom and the switch control that stops it, with a rollout order."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg.html
  - https://www.comptia.org/certifications/network
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer 2 attacks and mitigations

| Attack | How it works | Symptom | Control |
|---|---|---|---|
| MAC flooding (macof) | thousands of fake source MACs fill the CAM table; switch floods all frames like a hub | CAM table full, unicast flooding, attacker sniffs others' traffic | port security max MACs; MAC limit per port |
| ARP spoofing / on-path | attacker sends ARP replies claiming the gateway IP | duplicate-IP warnings, traffic via attacker MAC | DHCP snooping + Dynamic ARP Inspection (DAI) |
| Rogue DHCP | attacker's server answers DISCOVERs with itself as gateway/DNS | wrong gateway/DNS on clients | DHCP snooping (trusted ports only on uplinks/servers) |
| DHCP starvation | many DISCOVERs with fake MACs exhaust the pool | pool exhausted, legit clients fail | DHCP snooping rate limit + port security |
| VLAN hopping: switch spoofing | host negotiates a trunk via DTP | host sees all VLANs | `switchport mode access` + `nonegotiate` |
| VLAN hopping: double tagging | outer tag = native VLAN stripped, inner tag delivered | one-way injection into another VLAN | unused native VLAN, or tag native VLAN |
| STP manipulation | rogue switch sends superior BPDUs to become root | traffic through attacker, topology changes | BPDU guard on edge, root guard on distribution |
| IP spoofing | forged source IPs | asymmetric/odd sources | IP Source Guard, uRPF at L3 |
| CDP/LLDP reconnaissance or floods | read/flood discovery frames | info disclosure, CPU | disable on user ports |

## Rollout order (least risk first)
1. PortFast + BPDU guard on all access ports; root guard on distribution downlinks.
2. Access ports hard-set (`mode access`, `nonegotiate`), unused ports shut in a parking VLAN.
3. DHCP snooping: enable per VLAN, mark uplinks/DHCP server ports **trusted** first, then
   enable; check `show ip dhcp snooping binding` fills.
4. DAI on the same VLANs after the binding table is populated; static ARP ACLs for static-IP
   hosts; trust uplinks.
5. Port security (max 2-3 MACs for phone + PC, `violation restrict` to start).
6. IP Source Guard where bindings are reliable.
7. 802.1X/MAB for identity (makes most of the above less exploitable).

## Gotchas
- DAI drops ARP from static-IP devices without bindings: printers, servers, cameras. Add ARP
  ACLs or DHCP reservations first.
- Wireless clients are protected by the WLC/AP equivalents (client isolation, ARP proxy).
- Port security breaks docking stations/VMs with many MACs: raise max on known ports.

## Verify
- [ ] Lab test with an attacker laptop (macof, a rogue DHCP server, arpspoof) shows each attack blocked and logged.
- [ ] Logs from snooping/DAI/BPDU guard reach the SIEM.
