---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.traffic-groups-and-floating-ips
name: traffic-groups-and-floating-ips
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, traffic-groups, floating-ip, ha-group]
level: practitioner
status: draft
description: "Place floating self IPs and virtual addresses in traffic groups, set ha-order and force failover from tmsh."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-device-service-clustering-administration.html
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Traffic groups, floating addresses and failover

```
tmsh create cm traffic-group tg_2 ha-order { bigip2 bigip1 } auto-failback-enabled true auto-failback-time 60
tmsh modify net self float-ext traffic-group tg_2
tmsh modify ltm virtual-address 10.1.10.100 traffic-group tg_2
tmsh show cm traffic-group
tmsh run sys failover standby traffic-group tg_2
tmsh run sys failover online
```
- A traffic group is the unit of failover: it carries floating self IPs, virtual addresses, SNAT addresses and NATs. `traffic-group-local-only` keeps an address on one unit (non-floating self IPs).
- Active/active uses two traffic groups, each with a different default device (`ha-order`), so each unit carries one while both pass traffic. Capacity planning: if one fails, the survivor must carry both.
- Failover triggers: loss of heartbeat (network failover via UDP 1026 on the unicast address, or hard-wired), an HA group score (`ha-group`/`ha-score`), VLAN failsafe, a failed `tmm`, or `fail-safe`.
- `auto-failback` moves the group back to its preferred device after the timer; leave it off unless the units are unequal.
- Gotcha: a floating virtual address in `traffic-group-1` but with a pool on a standby-only VLAN gets no responses; `tmsh show cm traffic-group` first.

Verify: `tmsh show cm failover-status` and `tmsh show sys failover`; on the new active unit, gratuitous ARP appears in `tcpdump -nni external arp`, and upstream switches update their MAC table.
