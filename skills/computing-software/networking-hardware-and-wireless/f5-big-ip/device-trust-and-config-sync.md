---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.device-trust-and-config-sync
name: device-trust-and-config-sync
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, device-trust, device-group, config-sync]
level: practitioner
status: draft
description: "Establish BIG-IP device trust, build a sync-failover device group and run config sync with the correct direction."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-device-service-clustering-administration.html
  - https://clouddocs.f5.com/training/community/f5cert/html/class4/module3/module3.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device trust, device groups and config sync

```
tmsh modify cm device bigip1.example.com configsync-ip 10.10.10.1 unicast-address { { ip 10.10.10.1 port 1026 } } mirror-ip 10.10.10.1
tmsh add cm trust-domain /Common/Root ca-devices add { 10.1.1.2 } name bigip2 username admin password 'xxx'
tmsh create cm device-group dg_failover devices add { bigip1 bigip2 } type sync-failover auto-sync enabled network-failover enabled
tmsh run cm config-sync to-group dg_failover
tmsh show cm sync-status
```
- Before trust: unique hostnames, NTP in sync, and self IPs that allow `tcp:4353`, `tcp:22`/`443`, `udp:1026`. Trust is established once, from one unit, against the peer's management or self IP.
- Direction matters: `to-group` pushes the local config over the peers; `from-group` pulls. Syncing the wrong direction wipes the good config. Check which unit shows "Changes Pending" in `show cm sync-status`.
- `auto-sync enabled` pushes changes right away; many teams use manual sync and `incremental-config-sync-size-max` (confirm), to review before pushing.
- Not synced: self IPs of the non-floating kind, management IP, licence, host names, VLAN interface bindings (only objects, not hardware), and the local `root` password.
- Gotcha: `tmsh modify sys global-settings hostname` after trust requires reset of device trust (`tmsh modify cm device old-name name new-name`).

Verify: `tmsh show cm sync-status` shows "In Sync" with Last Sync time; `tmsh list cm device-group dg_failover devices`.
