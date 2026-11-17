---
id: computing-software.systems-network-administration.keepalived.mixing-healthcheck-failover-case-study
name: mixing-healthcheck-failover-case-study
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, case-study, vrrp, healthcheck, lvs, vip, sync-groups, high-availability]
level: advanced
status: docs-checked
description: "Combining VRRP and healthchecks: use VRRP VIPs as LVS VIPs so both directors are active, director 1 serving HTTP on 192.168.200.10 and director 2 SSL on 192.168.200.12."
sources:
  - https://keepalived.readthedocs.io/en/latest/case_study_mixing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mixing healthcheck and failover

Idea: use VRRP VIPs as the LVS virtual server addresses, so the director is highly available while it also checks the real-server pool.

Topology: two symmetric directors, both active.
- Director 1: HTTP on 192.168.200.10:80 (wrr, NAT, delay_loop 30, persistence 50, sorry_server 192.168.100.100:80).
- Director 2: SSL on 192.168.200.12:443 (rr, NAT, delay_loop 20, persistence 360, TCP_CHECK).
- Real servers 192.168.100.2 and .3.

VRRP: VI_1 (eth0, VRID 51, prio 150) and VI_2 (eth1, VRID 52) in sync group VG1; VI_3 (53) and VI_4 (54) at priority 100 in VG2; all with `authentication` PASS and advert_int 1. Director 2 mirrors them; the page does not list its full values.

The page documents no commands.

Verify: each VIP is held by exactly one director and its virtual server exists in the IPVS table of the holder.

## Checked

2026-11-04. Confirmed against the Case Study: Mixing Healthcheck and Failover page: VRRP instances, VRIDs, priorities, PASS authentication, sync groups, the two virtual servers and their settings, and the symmetric second director. Nothing removed.

Method: documentation only; no commands were run.
