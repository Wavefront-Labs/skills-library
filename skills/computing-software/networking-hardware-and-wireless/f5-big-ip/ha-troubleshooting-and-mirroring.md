---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.ha-troubleshooting-and-mirroring
name: ha-troubleshooting-and-mirroring
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, connection-mirroring, network-failover, sync-troubleshooting]
level: practitioner
status: draft
description: "Diagnose BIG-IP failover and sync problems: unicast and multicast failover, connection mirroring, split brain and stale device states."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-device-service-clustering-administration.html
  - https://clouddocs.f5.com/training/community/f5cert/html/class4/module3/module3.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HA troubleshooting: network failover, mirroring and sync failures

```
tmsh show cm device-group
tmsh show cm sync-status
tmsh list cm device all-properties | grep -E "name|unicast|mirror|configsync"
tmsh modify ltm virtual vs_web mirror enabled
tmsh show sys failover
tail -f /var/log/ltm | grep -i -E "failover|sod|devmgmtd"
```
- Typical error "Disconnected" or "Peer unreachable": the peer's configsync or failover IP fails the `4353`/`1026` lockdown, or the self IPs are on different VLANs/subnets.
- Failover uses a unicast or multicast heartbeat; add both a dedicated HA VLAN and mgmt-address failover for redundancy (`failover-unicast-address`) so a data-plane fault does not look like a unit failure.
- Split brain (both Active): the HA link is down but data VLANs are up. Fix the heartbeat path; the two units flip repeatedly.
- Connection mirroring (`mirror enabled` on the virtual, `mirror-ip` on the device) copies connection state to the standby; long-lived TCP survives failover but doubles processing; it needs a dedicated, fast link (`mirror-secondary-ip` for the second path).
- Persistence mirroring is separate; set on the persistence profile.
- Gotcha: changing a device's IP on a configsync address without updating the other device group member breaks sync; remove then add the device after fixing.

Verify: `tmsh show cm sync-status` returns "In Sync"; `tmsh show ltm persistence persist-records` and `tmsh show sys connection` on the standby show mirrored entries.
