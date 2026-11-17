---
id: computing-software.systems-network-administration.cisco-networking.vlan-1-and-unused-port-hygiene
name: vlan-1-and-unused-port-hygiene
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, vlan, access-port, vlan-1, unused-ports, parking-vlan, blackhole-vlan, switchport-hardening, interface-range, shutdown, native-vlan, layer-2-security]
level: practitioner
status: draft
description: "Get user and management traffic off VLAN 1 and lock down unused switch ports: parking VLAN, shutdown, access mode, description conventions and audit commands."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Security/Baseline_Security/securebasebook/sec_chap4.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN 1 and unused-port hygiene

Every port starts in VLAN 1 and VLAN 1 is the default native VLAN on every trunk. A port
plugged in anywhere in the building lands on the same broadcast domain as anything else left
in VLAN 1, including (on many networks) the switch management SVI.

## Target state
- VLAN 1: no hosts, no management IP, pruned from trunks where the platform allows.
- Management in its own VLAN (e.g. 99) or out-of-band interface/VRF.
- Unused ports: access mode, in a **parking VLAN** that routes nowhere, administratively shut.
- Trunk native VLAN: an unused VLAN distinct from the parking VLAN (or tag native).

## Configure
```
vlan 999
 name PARKING
vlan 998
 name NATIVE-UNUSED
!
interface range Gi1/0/25 - 48
 description UNUSED
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 shutdown
!
interface Vlan1
 no ip address
 shutdown
!
interface Po1
 switchport trunk native vlan 998
 switchport trunk allowed vlan remove 1
```
VLAN 1 itself cannot be deleted; control traffic (CDP, VTP, DTP, PAgP, STP for VLAN 1) still
uses it internally even when pruned from the allowed list.

## Audit
```
show interfaces status | i  1  |notconnect        ! ports in VLAN 1 or not connected
show vlan id 1                                        ! ports still in VLAN 1
show interfaces status unused                         ! (some platforms) never used ports
show interfaces trunk                                 ! native VLAN and allowed list
```
`show interfaces Gi1/0/30 | i Last input` shows `never` for ports that have never seen traffic;
`show interfaces | i line protocol|Last input` across the stack finds ports idle for weeks.

## Gotchas
- Enabling a port for a new user = change VLAN, `no shutdown`, update description; make this a
  documented ticket step so ports do not linger in the parking VLAN with `no shutdown`.
- 802.1X/NAC deployments replace the parking VLAN with auth-fail/guest VLANs; do not combine
  both on the same port without testing.
- Removing VLAN 1 from a trunk to a third-party switch or old Catalyst can break that device's
  management if it lives in VLAN 1.

## Verify
- [ ] `show vlan id 1` lists no access ports.
- [ ] `show ip interface brief | i Vlan1` shows administratively down.
- [ ] Spot check: plugging a laptop into an unused port gives no link or no DHCP lease.
