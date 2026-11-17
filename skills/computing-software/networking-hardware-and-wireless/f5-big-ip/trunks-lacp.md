---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.trunks-lacp
name: trunks-lacp
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, trunks, lacp, link-aggregation]
level: practitioner
status: draft
description: "Build a BIG-IP trunk with LACP, set distribution hash and active/passive mode, and verify member state."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trunks and LACP link aggregation

Trunks aggregate physical interfaces into one logical link, with or without LACP.
```
tmsh create net trunk uplink interfaces add { 1.1 1.2 } lacp enabled lacp-mode active lacp-timeout short distribution-hash src-dst-ipport
tmsh show net trunk uplink
tmsh show net lacp
```
- Use the trunk name wherever an interface is accepted: `tmsh create net vlan external interfaces add { uplink { tagged } } tag 100`.
- `lacp-timeout short` sends LACPDUs every second (long: every 30 s). Match the switch setting or detection will be slow.
- `distribution-hash` options include `src-dst-mac`, `src-dst-ipport` and `dst-mac`; choose one the switch peer can balance on. The default favours MAC pairs, which can leave one link hot for few-host traffic.
- Member interfaces must all be the same speed and duplex. Trunk bandwidth is the sum, but a single flow still uses one member.
- `qinq` and `link-select-policy` settings exist for specific designs; leave default unless needed.
- Gotcha: trunk name and MAC are tied to the first member; on a vCMP guest the host owns the physical trunk.

Verify: `tmsh show net trunk` lists each member as `up` and the aggregate status `up`; `show net lacp` shows partner system ID and "collecting/distributing". If a member shows `uninit` the switch side is not in the same channel group.
