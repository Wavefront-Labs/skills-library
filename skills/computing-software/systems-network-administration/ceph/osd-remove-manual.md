---
id: computing-software.systems-network-administration.ceph.osd-remove-manual
name: osd-remove-manual
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, osd, remove, purge, crush-reweight, out]
level: advanced
status: docs-checked
description: "Remove an OSD manually: mark it out, let data migrate, stop it, then ceph osd purge."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/add-or-rm-osds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Removal order protects data.

1. Take the OSD out so data moves off it:

```
ceph osd out {osd-num}
```

To reverse this, run `ceph osd in {osd-num}`.

2. Wait for migration to finish; watch it with `ceph -w` until PGs are `active+clean`. An alternative that also moves data is `ceph osd crush reweight osd.{osd-num} 0`.
3. Stop the daemon on the host (for systemd installs, `systemctl stop ceph-osd@{osd-num}`).
4. Remove it from CRUSH, auth and the OSD map in one command:

```
ceph osd purge {id}
```

Notes:

- If the cluster is near `full_ratio`, do not remove OSDs: removal might push it to or past the ratio.
- If PGs stay stuck in `active+remapped` after marking out (seen on small clusters with few hosts), run `ceph osd in {osd-num}` and reweight to 0 instead of marking out again.
- On a cephadm-managed cluster the page says to use the orchestrator instead of this procedure.
- The page also removes any `[osd.N]` entry from `ceph.conf` and copies the file to the other hosts.

`ceph osd purge {id}` first checks the OSD is safe to destroy and stops if it is not. `--force` (or the older `--yes-i-really-mean-it`) skips that check and can cause permanent data loss. Purge deletes the ID, CRUSH position, CephX keys and config-key data, but not settings for `osd.{id}` in the central configuration database, so an OSD that later reuses the ID inherits them. Out versus reweight: marking an OSD `out` leaves its bucket's weight unchanged, while `ceph osd crush reweight osd.{osd-num} 0` subtracts the OSD's weight from the bucket, which the page says can be preferable when operating small clusters.

## Checked

2026-11-09. Confirmed against: the Ceph Adding/Removing OSDs page (docs.ceph.com/en/latest/rados/operations/add-or-rm-osds/): Removing OSDs (Manual), including out, observing migration, stopping, purge warning and the out versus reweight note.

Removed: the one-OSD-at-a-time advice, the generic never-stop warning and the specific cephadm command (not on this page).

Method: documentation only; no commands were run.

