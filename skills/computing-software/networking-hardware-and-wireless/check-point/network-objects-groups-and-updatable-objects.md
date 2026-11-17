---
id: computing-software.networking-hardware-and-wireless.check-point.network-objects-groups-and-updatable-objects
name: network-objects-groups-and-updatable-objects
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, network-objects, object-groups, updatable-objects]
level: practitioner
status: draft
description: "Create hosts, networks, groups and dynamic/updatable objects (Office 365, AWS) in the Check Point management database."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/latest/APIs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network objects, groups and updatable objects

```
mgmt_cli -r true add host name "web1" ip-address "10.1.20.11" color "blue"
mgmt_cli -r true add network name "net_dmz" subnet "10.1.20.0" mask-length 24
mgmt_cli -r true add group name "grp_web" members.1 "web1" members.2 "net_dmz"
mgmt_cli -r true add address-range name "range_vpn" ip-address-first "10.9.0.10" ip-address-last "10.9.0.200"
mgmt_cli -r true show updatable-objects-repository-content details-level standard
mgmt_cli -r true publish
```
- Use groups in rules, not individual hosts, so policy stays readable. A group can nest groups. Where-used (right-click > Where Used) shows references before deleting.
- Updatable objects (e.g. Microsoft Office 365, Amazon Web Services regions) download from Check Point's repository and refresh without a policy install. They require the gateway to reach the update service (check the "Updates" in Manage & Settings > Updates).
- Dynamic Object: a placeholder resolved on each gateway with `dynamic_objects -n LocalMail -a 10.1.1.5` (address) or `-r` for ranges; the gateway needs this per-gateway definition or the rule never matches.
```
dynamic_objects -l                      # list on the gateway
dynamic_objects -n LocalMail -r 10.1.1.1 10.1.1.20 -a
```
- Domain objects (FQDN) do not use DNS caching in the old way: use a "Domain" object with a leading dot (`.example.com`) for subdomains; enable "Resolve" in Global Properties if needed (confirm).
- Gotcha: a host object with `ipv4` and `ipv6` both requires the gateway to have IPv6 enabled.

Verify: after install, `fw tab -t dynobj_tab -s` shows dynamic objects loaded (confirm); a log entry for traffic matching a rule using the group confirms membership.
