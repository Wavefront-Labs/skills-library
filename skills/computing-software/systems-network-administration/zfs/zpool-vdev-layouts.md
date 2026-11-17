---
id: computing-software.systems-network-administration.zfs.zpool-vdev-layouts
name: zpool-vdev-layouts
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, vdev, mirror, raidz, draid, spare, log]
level: practitioner
status: docs-checked
description: "Write vdev specifications for zpool create: stripes, mirrors, raidz, draid, hot spares and log devices, and the mixing checks that need -f."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-create.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/7/zpoolconcepts.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vdev layouts in zpool create

A pool is built from top-level vdevs. Redundancy exists only inside each vdev.

## Examples

```
zpool create tank sda1 sdb2                 # plain disks: no redundancy
zpool create tank mirror sda sdb mirror sdc sdd   # two mirrors, striped
zpool create tank raidz sda sdb sdc         # single raidz vdev
zpool create tank mirror sda sdb spare sdc  # mirror plus hot spare
zpool create tank sda sdb log mirror sde sdf   # mirrored log devices
```

- Each `mirror` keyword starts a new mirrored vdev; several mirrors stripe together.
- `spare` adds hot spares; `log` adds separate intent log devices.
- Files can be vdevs but the man page calls that not recommended, mainly for experiments.

## dRAID

`draid` specs carry parity, data, children and spares in one token: `draid1:4d:6c:1s` is one parity, four data, six devices, one spare. Failure groups and domains use the keywords `fgroup` and `fdomain` followed by the devices, e.g. `draid1:5s fgroup ... fgroup ...`.

## Checks (override with -f)

- Mixing redundant and non-redundant vdevs, or disks with files, is an error.
- Differently sized devices in one raidz or mirror group are an error.
- A device with an old UFS filesystem can be overridden.

Devices that are mounted or set as the dump device cannot be used. Decide the layout up front: top-level raidz and draid vdevs cannot later be removed from the pool.

## Checked

2026-11-03. Pages read: zpool-create(8), zpoolconcepts(7), zpool-remove(8).

Confirmed: every example layout, mirror and spare and log keywords, files being strongly discouraged, draid1:4d:6c:1s, fgroup and fdomain, the -f checks, mounted and dump devices, and the raidz and draid removal restriction.

Method: documentation only; no commands were run.
