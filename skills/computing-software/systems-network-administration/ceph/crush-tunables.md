---
id: computing-software.systems-network-administration.ceph.crush-tunables
name: crush-tunables
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, crush, tunables, optimal, legacy, old-crush-tunables]
level: sme
status: docs-checked
description: "Change CRUSH tunables profiles in Ceph, understand the non-optimal tunables warning and silence it deliberately."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/crush-map/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tunables are CRUSH behaviour settings added over the years (bobtail, firefly, hammer, jewel profiles). Newer profiles need newer clients.

Switch profile:

```
ceph osd crush tunables optimal
ceph osd crush tunables legacy
```

Adjusting tunables shifts PGs between nodes, so be prepared for significant data movement (the page says possibly as much as 10% when moving to optimal); check for old kernel CephFS/RBD clients or pre-Bobtail librados clients first.

The "Non-optimal tunables" warning (`crush map has non-optimal tunables`, v0.74 and later) is raised when any tunable lacks the optimal value from the `default` profile; the health-checks page lists `OLD_CRUSH_TUNABLES` for very old settings. The preferred fix is `ceph osd crush tunables optimal`. If you cannot change tunables because ancient clients still connect, silence the warning on the monitors:

```
ceph tell mon.\* config set mon_warn_on_legacy_crush_tunables false
```

The page also lists which client versions support each tunables profile (TUNABLES2, TUNABLES3, V4, TUNABLES5); consult it before changing anything for kernel RBD or CephFS clients.

Before changing a profile, know what happens next. The OSD and monitor daemons immediately start rejecting new connections from clients that do not support the new feature, while already-connected clients are grandfathered in and may malfunction if they lack it. Reverting to legacy values later does not let you run old `ceph-osd` versions: peering still has to read old maps, so the page says not to run old OSD daemons once non-legacy values have been used. Profiles are `legacy`, `argonaut`, `bobtail`, `firefly`, `hammer`, `jewel`, `optimal` and `default`, and the page suggests throttling recovery and backfill parameters to limit the resulting backfill.

## Checked

2026-11-03. Confirmed against: the Ceph CRUSH Maps page (docs.ceph.com/en/latest/rados/operations/crush-map/): Tunables, Non-optimal tunables warning, Tuning CRUSH; the Health checks page (OLD_CRUSH_TUNABLES).

Removed: nothing; the OLD_CRUSH_TUNABLES wording was tightened.

Method: documentation only; no commands were run.
