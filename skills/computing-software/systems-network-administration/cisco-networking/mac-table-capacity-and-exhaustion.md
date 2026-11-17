---
id: computing-software.systems-network-administration.cisco-networking.mac-table-capacity-and-exhaustion
name: mac-table-capacity-and-exhaustion
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, switching, cisco-ios, ios-xe, mac-table-capacity, cam-table, mac-flooding, sdm-template, mac-limit, unknown-unicast-flooding]
level: practitioner
status: draft
description: "Size and monitor switch MAC/CAM table capacity, recognise exhaustion (flooding, failed learning), and protect it with port security, limits and SDM choices."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/configuring_sdm_templates.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_mac_address_table.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MAC table capacity and exhaustion

## Know the limit
```
show sdm prefer                      ! Cat 9000: "MAC Addresses" row = table size for the template
show mac address-table count         ! dynamic/static/total per VLAN and space available
```
Capacities differ widely (tens of thousands on Cat 9300/9500, single-digit thousands on old
access switches); read the number from `show sdm prefer`, do not assume.

## What exhaustion looks like
- Table full: new MACs are not learned, so frames to them are **flooded** as unknown unicast in the VLAN.
  Every host sees traffic for others; links fill; captures show foreign unicast.
- Causes: MAC flooding attack (macof), a loop churning MACs, huge flat VLANs, VM sprawl, hash
  collisions on platforms with hashed tables (learning fails before 100%).

## Protect it
```
interface Gi1/0/10
 switchport port-security
 switchport port-security maximum 3
mac address-table notification threshold limit 80 interval 120
```
- Shrink broadcast domains (smaller VLANs; routed access).
- Lower aging time cautiously (`mac address-table aging-time 120`) only if hosts churn; too low = more flooding.
- Pick an SDM template with more MAC space on L2 aggregation boxes (`sdm prefer ...` then reload).

## Verify
- [ ] Peak MAC count < 70-80% of `show sdm prefer` capacity.
- [ ] Threshold notification configured and reaching syslog/SNMP.
- [ ] Access ports have port-security maximums so one port cannot fill the table.
