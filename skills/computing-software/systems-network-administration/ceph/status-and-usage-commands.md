---
id: computing-software.systems-network-administration.ceph.status-and-usage-commands
name: status-and-usage-commands
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, monitoring, status, ceph-df, osd-df, ceph-w]
level: intro
status: docs-checked
description: "Everyday Ceph status commands: ceph -s, ceph -w, ceph df, ceph osd tree/stat, mon and mds status."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Overall state:

```
ceph status
ceph -s
ceph -w
```

`-w` watches the cluster log live.

Usage:

```
ceph df
ceph df detail
```

OSDs:

```
ceph osd stat
ceph osd dump
ceph osd tree
```

Monitors and quorum:

```
ceph mon stat
ceph mon dump
ceph quorum_status
```

Metadata servers:

```
ceph mds stat
ceph fs dump
```

When the `ceph` command cannot find your config or keyring, pass them explicitly:

```
ceph -c /path/to/conf -k /path/to/keyring health
```

Reading `ceph status`: `usage` is actual raw storage used, with the lesser `xxx GiB / xxx GiB` figure being available capacity. The `objects` line counts client data once, before replication or erasure coding, and includes data only snapshots still reference, so `usage` is larger. In `ceph df`, `STORED` counts data once while `USED` includes replication, allocation granularity and erasure-coding overhead, minus compression savings; for three replicas, 1 MiB stored shows about 3 MiB used. `(DATA)` is RBD, CephFS file and RGW object data and `(OMAP)` is key-value metadata. `ceph quorum_status` returns JSON in which `quorum_names` lists the monitors in quorum. Interactive mode accepts `status` directly. `ceph tell osd.0 messenger dump` shows connections and sockets, but it locks connection data for tens of milliseconds.

## Checked

2026-11-09. Confirmed against: the Ceph Monitoring a Cluster page (docs.ceph.com/en/latest/rados/operations/monitoring/): status, watching a cluster, usage, OSD, monitor and MDS status, and the messenger dump note.

Removed: the `ceph osd pool stats` and `rados df` line (not on the page).

Method: documentation only; no commands were run.

