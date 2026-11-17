---
id: computing-software.systems-network-administration.ceph.upmap-enable-compat-client
name: upmap-enable-compat-client
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, upmap, pg-upmap, require-min-compat-client, ceph-features]
level: practitioner
status: docs-checked
description: "Enable pg-upmap on an existing Ceph cluster by checking connected client versions and raising the minimum compatible client."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/upmap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The pg-upmap exception table in the OSDMap lets the cluster map specific PGs to specific OSDs. It needs every client to understand the structure, so the cluster must have no pre-Luminous clients.

New clusters enable the balancer module, which uses it. To use pg-upmap on an existing cluster, restrict it to compatible clients:

```
ceph osd set-require-min-compat-client luminous
```

The command fails if older clients or daemons are connected. See which versions are in use:

```
ceph features
```

If you want your own upmap entries or a different balancer, stop the module first so the two do not fight:

```
ceph balancer off
```

Order of work:

1. Run `ceph features` and upgrade or disconnect any old client.
2. Set the minimum client release.
3. Turn the balancer on again, or add manual entries.

## Checked

2026-11-03. Confirmed against: the Ceph Using pg-upmap page (docs.ceph.com/en/latest/rados/operations/upmap/): Online Optimization, Enabling.

Removed: the 'never lower' warning (it appears on the read-balancer page for reef, not on this page).

Method: documentation only; no commands were run.
