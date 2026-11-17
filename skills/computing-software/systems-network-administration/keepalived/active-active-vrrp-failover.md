---
id: computing-software.systems-network-administration.keepalived.active-active-vrrp-failover
name: active-active-vrrp-failover
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, active-active, failover, case-study, sync-groups, vrrpv2]
level: advanced
status: docs-checked
description: "Active-active router pair from the failover case study: four VRRP instances per director, mirrored MASTER/BACKUP roles, sync groups VG1 and VG2, AH authentication."
sources:
  - https://keepalived.readthedocs.io/en/latest/case_study_failover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active-active VRRP failover

Two directors each run four VRRP instances (VRRPv2); two MASTER, two BACKUP, mirrored on the peer.

| Instance | Director 1 | iface | VRID | prio | VIPs |
|---|---|---|---|---|---|
| VI_1 | MASTER | eth0 | 51 | 150 | 192.168.200.10, .11 |
| VI_2 | MASTER | eth1 | 52 | 150 | 192.168.100.10 |
| VI_3 | BACKUP | eth0 | 53 | 100 | 192.168.200.12, .13 |
| VI_4 | BACKUP | eth1 | 54 | 100 | 192.168.100.11 |

Director 2 swaps roles: VI_3 and VI_4 MASTER at 150, VI_1 and VI_2 BACKUP at 100. Groups: `VG1` = VI_1 + VI_2, `VG2` = VI_3 + VI_4. All use `advert_int 1` and AH authentication with a distinct password each. Config path is /etc/keepalived/keepalived.conf.

The page notes this is a general high-availability router design, not LVS specific. Check ownership with ip address list on each node.

Verify: with both nodes up, each holds only its MASTER instances' VIPs; stop one and the other holds all four.

## Checked

2026-11-04. Confirmed against the Case Study: Failover page: four instances per director, VI_1 to VI_4 interfaces, VRIDs 51 to 54, priorities 150 and 100, VIP addresses, sync groups VG1 and VG2, AH authentication, advert_int 1, and the note that the sample is not LVS specific. Nothing removed.

Method: documentation only; no commands were run.
