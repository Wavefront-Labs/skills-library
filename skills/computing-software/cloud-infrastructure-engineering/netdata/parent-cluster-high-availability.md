---
id: computing-software.cloud-infrastructure-engineering.netdata.parent-cluster-high-availability
name: parent-cluster-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, parent-cluster, high-availability, failover]
level: advanced
status: docs-checked
description: "Build an active-active Netdata Parent cluster, then restore or add a Parent after maintenance without losing history or deleting copied data."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/clustering-and-high-availability-of-netdata-parents.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failover setup:
1. Configure Children to connect to all Parents (list them in `stream.conf`; the first available is used).
2. Configure Parents to sync with each other.

Every Parent receives all metrics of all Children. Children reconnect to another Parent automatically. At least one Parent must be online for Children to stay visible in Netdata Cloud.

Retention (in `[db]`, default 1GiB each): `dbengine tier 0 retention size`, `dbengine tier 1 retention size`, `dbengine tier 2 retention size`.

Parent back after maintenance:
- If Children lack enough history, temporarily block them until it syncs with other Parents: firewall port 19999 from Children IP ranges, or use different streaming keys for Children versus Parents and disable the Children key until sync ends.

Creating a new Parent:
1. `rsync` `/var/cache/netdata` from an existing Parent.
2. Do not start with default settings; it may delete the copied data to apply default size limits.
3. Set the retention settings to match, then start the service.

Balance Children by listing Parents in a different order in each `stream.conf`. Do not use a TCP load balancer; the FAQ recommends listing all Parents directly in the Children's `stream.conf`.

## Checked

2026-11-04. Confirmed against the Netdata Clustering and High Availability page and the metrics centralization FAQ: the two failover steps, all Parents receiving all metrics, automatic Child reconnection, Cloud visibility with one Parent online, the [db] retention size table with 1GiB defaults, both blocking options, the rsync of /var/cache/netdata and the warning about default settings, Parent ordering for balance, and the load balancer advice. Removed the claim that a cluster adds resilience, not capacity, which no page states.

Method: documentation only; no commands were run.
