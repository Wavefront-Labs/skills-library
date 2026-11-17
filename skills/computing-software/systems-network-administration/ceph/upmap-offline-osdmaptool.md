---
id: computing-software.systems-network-administration.ceph.upmap-offline-osdmaptool
name: upmap-offline-osdmaptool
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, upmap, osdmaptool, offline-optimizer, osdmap]
level: sme
status: docs-checked
description: "Compute pg-upmap entries offline with osdmaptool against a copy of the OSDMap, per pool, and review them before applying."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/upmap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The offline optimiser is built into `osdmaptool`. Take a copy of the live map, then compute entries:

```
ceph osd getmap -o om
osdmaptool om --upmap out.txt [--upmap-pool <pool>] \
    [--upmap-max <max-optimizations>] \
    [--upmap-deviation <max-deviation>] \
    [--upmap-active]
```

Options:

- `--upmap-pool` can be given several times. The docs recommend optimising each pool, or sets of similarly utilised pools, separately. RBD image pools count as similar; an RGW index pool and an RGW data pool do not.
- `--upmap-max` is the maximum number of upmap entries to identify. The default is 10, as with the ceph-mgr balancer module; the page suggests a larger number for offline work. It stops early if nothing more can be improved.
- `--upmap-deviation` is the maximum PG deviation to accept; it defaults to 5. An OSD whose PG count is within that of the computed target is considered perfect.
- `--upmap-active` simulates the active balancer in upmap mode: it keeps cycling until the OSDs are balanced and reports rounds and time per round.

The proposed changes are written to `out.txt` as normal Ceph CLI commands. Read it, then apply:

```
source out.txt
```

The steps can be repeated until the PGs of each set of pools are distributed as well as possible. The page also notes `--debug-osd 10` and `--debug-crush 10` for tool detail.

## Checked

2026-11-03. Confirmed against: the Ceph Using pg-upmap page (docs.ceph.com/en/latest/rados/operations/upmap/): Offline Optimization.

Removed: the claims that out.txt holds pg-upmap-items commands specifically, that the balancer may revert entries, and the health-first advice.

Method: documentation only; no commands were run.
