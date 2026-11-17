---
id: computing-software.systems-network-administration.ceph.stretch-mode-force-recovery
name: stretch-mode-force-recovery
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, stretch-cluster, recovery, force, degraded]
level: sme
status: docs-checked
description: "Force a Ceph stretch cluster into recovery or healthy stretch state when automatic transitions are stuck."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/stretch-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In stretch mode the cluster goes through degraded, recovery and healthy states automatically after losing and regaining a site. If a transition stalls you can force it.

```
ceph osd force_recovery_stretch_mode --yes-i-really-mean-it
ceph osd force_healthy_stretch_mode --yes-i-really-mean-it
```

- `force_recovery_stretch_mode` moves the cluster into recovery stretch mode.
- `force_healthy_stretch_mode` returns it to normal stretch mode.

Treat both as last resort tools: they override the checks that confirm the returning site has caught up. Before running them, confirm that the returning OSDs are up and that recovery has actually completed (for example with `ceph -s`).

Other commands from the page: disable stretch mode with `ceph mon disable_stretch_mode [{crush_rule}] --yes-i-really-mean-it`, and swap the tiebreaker with `ceph mon set_new_tiebreaker mon.<new_mon_name>`.

Know the states. If a whole `datacenter` becomes inaccessible, the survivor enters degraded stretch mode: pools' `min_size` drops to 1, `size` is unchanged so PGs are reported undersized, and a stretch flag stops OSDs creating extra copies. When the zone returns, recovery stretch mode allows peering using only the zone that stayed up, and when PGs are no longer degraded, undersized or incomplete the cluster returns to normal, restoring `min_size` 2. `force_healthy_stretch_mode` fails if the cluster is not in recovery mode. A CRUSH rule using a device class can leave PGs inactive after a site loss, because the monitors compare the real bucket to a shadow bucket such as `zone1~ssd`; the page recommends rules without a device class.

## Checked

2026-11-09. Confirmed against: the Ceph Stretch Mode page (docs.ceph.com/en/latest/rados/operations/stretch-mode/): the force_recovery and force_healthy commands, disable_stretch_mode, set_new_tiebreaker, degraded and recovery states and the device-class CRUSH rule caveat.

Removed: the `ceph pg stat` check (not on the page).

Method: documentation only; no commands were run.

