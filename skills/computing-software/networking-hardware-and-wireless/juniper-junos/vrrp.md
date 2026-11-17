---
id: computing-software.networking-hardware-and-wireless.juniper-junos.vrrp
name: vrrp
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, vrrp, virtual-ip, vrrp-priority, gateway-redundancy]
level: practitioner
status: draft
description: "Configure Junos VRRP groups with priorities, preempt, accept-data and tracking."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRRP gateway redundancy
Goal: provide a redundant default gateway.

```
set interfaces irb unit 100 family inet address 192.0.2.2/24 vrrp-group 100 virtual-address 192.0.2.1
set interfaces irb unit 100 family inet address 192.0.2.2/24 vrrp-group 100 priority 200
set interfaces irb unit 100 family inet address 192.0.2.2/24 vrrp-group 100 preempt
set interfaces irb unit 100 family inet address 192.0.2.2/24 vrrp-group 100 accept-data
set interfaces irb unit 100 family inet address 192.0.2.2/24 vrrp-group 100 track interface xe-0/0/47 priority-cost 120
```

```
user@host> show vrrp summary
user@host> show vrrp detail
```

- Priority 255 means the virtual IP is the interface IP (owner).
- `accept-data` lets the master answer ping to the VIP (otherwise it will not).
- Fast failover: `advertise-interval` can use ms with `vrrp` fast timers (confirm on platform); BFD is often better.

Gotcha: two routers with the same priority tie-break by highest IP. Without `preempt` a recovered primary stays backup. VRRP over EVPN anycast gateways is not the same: use virtual-gateway.

## Verify
- `show vrrp summary` shows one `master` and one `backup` per group; ping the VIP.
