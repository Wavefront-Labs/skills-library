---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.default-and-static-routes
name: default-and-static-routes
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, static-routes, default-gateway, management-route]
level: practitioner
status: draft
description: "Add data-plane default and static routes, set the separate management route, and check the route table."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Default gateway and static routes

The management interface and data plane use separate routing tables.
```
tmsh create sys management-route default gateway 192.168.1.1
tmsh create net route default_gw network default gw 10.1.10.1
tmsh create net route to_dc network 172.16.0.0/16 gw 10.1.20.254
tmsh create net route blackhole network 192.0.2.0/24 blackhole
tmsh list net route
tmsh show net route
```
- `network default` means 0.0.0.0/0. Use a pool of gateways instead of a single IP with `pool <poolname>` for a resilient default route (router health monitored by the pool monitor).
- The gateway must be reachable via an existing self IP subnet, else create fails with "gateway is not on a directly connected network".
- Management traffic (SSH, GUI, SNMP, NTP, DNS by default) uses `sys management-route`; data-plane services (e.g. LDAP auth) can be forced via a self IP with `tmsh modify sys db tmm.sourceip ...` style settings only with F5 support guidance. Do not rely on the data-plane default gateway for management.
- Auto last hop (`tmsh modify ltm global-settings general auto-last-hop enabled`, default on) returns replies to the MAC the request arrived on, ignoring the route table; disable per VLAN/VS only when asymmetric return is intended.

Verify: `ip route`-like check is `tmsh show net route` (data plane) and `ip route show` in bash (mgmt, confirm). `tcpdump -nni 0.0 host <client>` proves where replies exit.
