---
id: computing-software.systems-network-administration.cisco-networking.ptp-precision-time-protocol
name: ptp-precision-time-protocol
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ptp, precision-time-protocol, ieee-1588, boundary-clock, transparent-clock, grandmaster, gptp]
level: practitioner
status: draft
description: "Deploy IEEE 1588 PTP on Cisco switches: grandmaster choice, boundary vs transparent clock mode, profiles (default, power, AES67), domain, and checking offset."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_precision_time_protocol__ptp_.html
  - https://standards.ieee.org/ieee/1588/6825/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Precision Time Protocol (PTP)

PTP (IEEE 1588) gives sub-microsecond sync where NTP's milliseconds are not enough: broadcast
audio/video (AES67, SMPTE 2110), power substations (IEC 61850), finance, 5G fronthaul.
Every hop must participate in PTP, or the timestamps absorb queueing delay and accuracy collapses.

## Roles
- **Grandmaster (GM):** GPS/GNSS-disciplined appliance; elected by Best Master Clock Algorithm
  (priority1, clockClass, accuracy, priority2, identity).
- **Boundary clock (BC):** switch syncs to upstream as a slave, acts as master downstream.
  Scales well, isolates domains.
- **Transparent clock (TC):** switch adds residence time to a correction field. Simple, no
  BMCA participation.
- Ordinary clock: end device.

## Catalyst 9300 example (boundary clock, default profile)
```
ptp mode boundary delay-req
ptp priority1 128
ptp domain 0
interface TenGigabitEthernet1/0/1     ! towards GM
 ptp enable
```
Profiles change transport and messages: `ptp profile dot1as` (gPTP/AVB), power profile
(L2, peer-delay), AES67/SMPTE 2059 domains and rates. Every device in a domain must use the
same profile, domain number and delay mechanism (E2E delay-req vs P2P peer-delay).

## Design rules
- Two GMs with different priority1 for redundancy; set switch priority1 high (255) so no
  switch ever wins BMCA by accident.
- Put PTP event messages (UDP 319/320, or EtherType 0x88F7) in a priority queue; DSCP EF/CS7
  as per profile.
- Asymmetric links (different fibre lengths each way) cause constant offset; compensate or avoid.

## Verify
```
show ptp clock
show ptp parent                 ! grandmaster identity, clock class
show ptp port                   ! port state MASTER/SLAVE/PASSIVE
```
Offset from master should settle in the tens of nanoseconds on hardware-timestamped gear.
- [ ] Single expected GM across the domain; offsets stable; failover to backup GM tested.
