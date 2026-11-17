---
id: computing-software.systems-network-administration.ceph.cephfs-multiple-active-mds
name: cephfs-multiple-active-mds
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephfs, mds, max-mds, balancer, standby]
level: advanced
status: docs-checked
description: "Scale CephFS to several active MDS ranks with max_mds and tune dynamic subtree balancing."
sources:
  - https://docs.ceph.com/en/latest/cephfs/multimds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set the number of active ranks:

```
ceph fs set <fs_name> max_mds 2
```

Standby daemons fill the new ranks. Decrease with the same command, for example `ceph fs set <fs_name> max_mds 1`; the extra ranks are stopped.

Dynamic subtree partitioning:

```
ceph fs set <fs_name> balance_automate true
```

Restrict the balancer to chosen ranks with a bitmask:

```
ceph fs set <fs_name> bal_rank_mask 0x3
ceph fs set <fs_name> bal_rank_mask -1
ceph fs set <fs_name> bal_rank_mask 0x0
```

`0x3` uses ranks 0 and 1, `-1` uses all ranks, and `0x0` disables the balancer.

Use multiple active MDS ranks when metadata performance is bottlenecked on the single MDS that runs by default. For predictable placement the page also describes manually pinning directory trees to ranks.

Each file system defaults to one active MDS. Raising `max_mds` only creates ranks when spare daemons exist: with one daemon and `max_mds 2`, no second rank forms and a health warning appears because no standby can take over. New ranks pass through `creating` then `active`. Highly available setups still need standbys, so the practical maximum is one less than the number of MDS servers. A single application on a single client rarely benefits; many clients on many directories do. Pinning is manual and explicit: `setfattr -n ceph.dir.pin -v 2 path/to/dir` pins a tree to rank 2, and `setfattr -n ceph.dir.pin.distributed -v 1 /cephfs/home` enables distributed ephemeral pinning for home directories.

## Checked

2026-11-09. Confirmed against: the Ceph CephFS Multiple Active MDS page (docs.ceph.com/en/latest/cephfs/multimds/): max_mds, standby daemons, manual and ephemeral pinning, balance_automate and bal_rank_mask.

Removed: the CPU-saturation trigger wording and the `ceph fs status` / `ceph mds stat` check (not on the page).

Method: documentation only; no commands were run.

