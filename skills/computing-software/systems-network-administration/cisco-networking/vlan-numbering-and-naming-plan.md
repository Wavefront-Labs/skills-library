---
id: computing-software.systems-network-administration.cisco-networking.vlan-numbering-and-naming-plan
name: vlan-numbering-and-naming-plan
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, vlan, vlan-numbering-plan, vlan-naming, ip-addressing-plan, network-documentation, campus-design, cisco-ios]
level: practitioner
status: draft
description: "Design a VLAN numbering and naming plan that encodes site, function and subnet, avoids reserved and internal ranges, and stays consistent across sites."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_vlans.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN numbering and naming plan

## Principles
- One VLAN = one subnet = one function. Never stretch a VLAN across sites unless a design demands it.
- Encode function in the ID so an engineer recognises it on any switch.
- Keep IDs the same at every site for the same function; the subnet changes, the VLAN does not.
- Avoid 1, 1002-1005, the platform internal range (check `show vlan internal usage`), and
  3968-4095 if Nexus is in play.

## A workable scheme
| Block | Function | Example |
|---|---|---|
| 10-99 | user data by floor/zone | 10 DATA-FL1, 11 DATA-FL2 |
| 100-149 | voice | 100 VOICE |
| 150-199 | wireless client (if switched) | 150 WLAN-CORP, 160 WLAN-GUEST |
| 200-299 | infrastructure: AP mgmt, printers, cameras, IoT | 200 AP-MGMT, 210 PRINT, 220 CCTV |
| 900-949 | network management / OOB | 900 NET-MGMT |
| 999 | parking/black hole for unused ports | 999 UNUSED |
| 998 | native VLAN on trunks (carries nothing) | 998 NATIVE-UNUSED |

Tie to addressing where you can: VLAN 20 at site 12 = 10.12.20.0/24. The third octet = VLAN ID
makes troubleshooting fast (works while IDs < 256).

## Naming
- Upper case, no spaces, max 32 characters: `<FUNCTION>[-<ZONE>]`, e.g. `DATA-FL2`, `CCTV`, `AP-MGMT`.
- Names are local; VTP or automation must push them. Keep the source of truth in IPAM/NetBox
  and template it, not by hand.

## Gotchas
- Re-numbering live VLANs is a big outage project; get the plan right before rollout.
- Do not reuse a retired ID for a different function within a year; old ACLs and docs linger.
- The guest VLAN should never be routed internally; name makes it obvious (`GUEST`), ACLs enforce it.

## Verify
- [ ] Every site's `show vlan brief` matches the plan (automate with a compliance check).
- [ ] No access port in VLAN 1; unused ports in the parking VLAN and shut.
