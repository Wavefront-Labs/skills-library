---
id: computing-software.systems-network-administration.ceph.health-osd-full-ratios
name: health-osd-full-ratios
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, health, osd-full, nearfull, backfillfull, full-ratio]
level: practitioner
status: docs-checked
description: "Respond to OSD_NEARFULL, OSD_BACKFILLFULL and OSD_FULL, including temporary full-ratio changes and leftover rados bench objects."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/health-checks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three escalating checks:

- `OSD_NEARFULL`: an early warning that the cluster is approaching full.
- `OSD_BACKFILLFULL`: an OSD is, or would become after pending backfills, above the backfillfull threshold, so rebalancing may not finish.
- `OSD_FULL`: an OSD exceeded the full threshold and the cluster stops servicing writes.

Start with utilisation:

```
ceph df
ceph osd df
ceph osd dump | grep full_ratio
```

Short-term workaround to restore writes: raise the full threshold slightly.

```
ceph osd set-full-ratio <ratio>
```

Lasting fix: add OSDs in appropriate CRUSH failure domains, or delete data. A subtle cause is `rados bench` test objects left in a pool. Check with `rados ls` against each pool for names beginning `bench`, then delete them carefully.

The page calls raising the full threshold a short-term workaround to restore write availability.

Each check has its own wording. `OSD_NEARFULL` means an OSD exceeded the `nearfull` threshold and is an early warning. `OSD_BACKFILLFULL` means an OSD exceeded `backfillfull`, or would once currently mapped backfills finish, which blocks data from rebalancing onto it. `OSD_FULL` means an OSD exceeded `full` and the cluster refuses writes. For all three the page points to `ceph df` for per-pool use and to the OSD troubleshooting section on running out of drive space. Use `ceph osd dump | grep full_ratio` to read the current ratios before changing anything with `ceph osd set-full-ratio <ratio>`.

## Checked

2026-11-03. Confirmed against: the Ceph Health checks page (docs.ceph.com/en/latest/rados/operations/health-checks/): OSD_NEARFULL, OSD_BACKFILLFULL, OSD_FULL.

Removed: the instruction to lower the ratio again (the page only calls the raise short-term).

Method: documentation only; no commands were run.
