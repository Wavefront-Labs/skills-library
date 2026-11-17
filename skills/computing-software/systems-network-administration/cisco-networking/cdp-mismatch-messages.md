---
id: computing-software.systems-network-administration.cisco-networking.cdp-mismatch-messages
name: cdp-mismatch-messages
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cdp, cdp-mismatch-messages, native-vlan, duplex-mismatch, cdp-timers, syslog, troubleshooting]
level: practitioner
status: draft
description: "Act on CDP-4 NATIVE_VLAN_MISMATCH and DUPLEX_MISMATCH syslogs: confirm the mismatch, fix the right side, and tune CDP timers/holdtime and version 2."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/cdp/configuration/xe-16/cdp-xe-16-book/nm-cdp-discover.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/98155-tshoot-vlan.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CDP mismatch messages

CDPv2 carries native VLAN and duplex, so the switch can warn you about a misconfigured link
before users notice.

## The messages
```
%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on GigabitEthernet1/0/48 (1), with SW2 GigabitEthernet1/0/48 (99).
%CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on GigabitEthernet0/1 (not full duplex), with R1 GigabitEthernet0/0 (full duplex).
```
They repeat every CDP interval (60 s) until fixed.

## Native VLAN mismatch
Effect: untagged frames from one side land in the other side's native VLAN, leaking traffic between
VLANs and splitting STP (PVST+ blocks the port with `*PVID_Inc` inconsistency).
```
show interfaces Gi1/0/48 trunk | include Native
show spanning-tree inconsistentports
```
Fix to the agreed native VLAN on both ends (`switchport trunk native vlan 99`). Also check an
access port wired to a trunk port: the access VLAN shows as the "native" VLAN in the message.

## Duplex mismatch
Effect: late collisions and CRC/runts on the half-duplex side, terrible throughput under load.
```
show interfaces Gi0/1 | include duplex|collisions|CRC
```
Set both sides to auto (preferred) or both hard-coded. Hard-coding one side and leaving the other
on auto produces exactly this mismatch: the auto side falls back to half duplex.

## CDP timers and version
```
cdp timer 30          ! advertisement interval (default 60 s)
cdp holdtime 90       ! neighbour expiry (default 180 s), keep >= 3 x timer
cdp advertise-v2      ! default on; v1 lacks native VLAN/duplex TLVs
show cdp
show cdp neighbors Gi1/0/48 detail
```
Shorter timers help topology tools notice changes faster; they do not speed up failure detection
for anything that matters.

## Gotchas
- Messages are suppressed if CDP is disabled on the port; LLDP has no native VLAN warning on IOS.
- Intentional mismatches (e.g. to a non-Cisco device with a different native) can be silenced with
  `no cdp log mismatch native` on that interface; document why.
- After fixing native VLAN, STP may need a moment to clear PVID inconsistency.

## Verify
- [ ] Message stops after the next CDP interval.
- [ ] `show spanning-tree inconsistentports` is empty.
