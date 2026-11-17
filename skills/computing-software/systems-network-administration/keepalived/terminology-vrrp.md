---
id: computing-software.systems-network-administration.keepalived.terminology-vrrp
name: terminology-vrrp
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, terminology, vrrp, master, backup, advertisement, ip-address-owner]
level: intro
status: docs-checked
description: "Keepalived VRRP vocabulary: IP address owner, MASTER and BACKUP states, real and virtual load balancer, synchronized instance, advertisement."
sources:
  - https://keepalived.readthedocs.io/en/latest/terminology.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRRP terminology

- **VRRP:** protocol for director failover and virtualisation.
- **IP address owner:** the instance holding the addresses as real interface addresses and answering packets to them (ICMP, TCP).
- **MASTER state:** the instance forwards packets sent to its addresses.
- **BACKUP state:** the instance can forward if the MASTER fails.
- **Real load balancer:** an LVS director running one or more VRRP instances.
- **Virtual load balancer:** a set of real load balancers.
- **Synchronized instance:** an instance another instance is synchronized with, allowing it to be monitored.
- **Advertisement:** a simple VRRPv2 packet sent by the MASTER to the other instances.

## Checked

2026-11-04: definitions confirmed against the VRRP Component section of the Terminology page. Removed the generic Verify line.
Method: documentation only; no commands were run.
