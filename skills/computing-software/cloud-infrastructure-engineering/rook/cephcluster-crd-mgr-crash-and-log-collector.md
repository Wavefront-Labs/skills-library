---
id: computing-software.cloud-infrastructure-engineering.rook.cephcluster-crd-mgr-crash-and-log-collector
name: cephcluster-crd-mgr-crash-and-log-collector
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [mgr, modules, pg-autoscaler, crashcollector, logcollector, daystoretain]
level: practitioner
status: docs-checked
description: "Set manager count and modules, the mgr_role=active label, crash collector retention and the log collector side-car in the CephCluster CR."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/ceph-cluster-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Manager settings:
- `mgr.count`: 1 to 2, default 2. With two managers, services must point at the active one. Rook labels mgr pods `mgr_role` as `active` or `standby`, so services (the dashboard, the prometheus collector) add `mgr_role=active` to their selector.
- `mgr.modules`: a list of Ceph manager modules to enable or disable:
```
mgr:
  modules:
  - name: <name of the module>
    enabled: true
```
The `dashboard` and `monitoring` modules are configured by other settings. Enabling `pg_autoscaler` makes Rook set `osd_pool_default_pg_autoscale_mode = on` for all new pools.

Crash collector:
- `crashCollector.disable`: true stops it on every node running a Ceph daemon.
- `crashCollector.daysToRetain`: how long crash entries stay in the cluster; by default they are kept indefinitely.

Log collector:
- `logCollector.enabled`: default true; runs as a side-car next to each Ceph daemon and turns on `log_to_file`, so logs go to files (rotated) as well as stdout. Segfault coredumps usually land in `/var/lib/systemd/coredump` on the host.
- `logCollector.periodicity`: rotation interval, default 24h, with suffix `h` or `d`. Rotating too often briefly interrupts the daemon and slightly hurts performance.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-cluster-crd) against this skill: 17 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 5 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
