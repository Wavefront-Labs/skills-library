---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-thin-provisioning-and-pool-autoextend
name: lvm-thin-provisioning-and-pool-autoextend
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, thin-provisioning, dm-thin-pool, lvchange, autoextend, lvm-conf, overprovisioning]
level: advanced
status: docs-checked
description: "Enable thinProvision on Local PV LVM, load dm_thin_pool, extend the thin pool, and turn on pool monitoring plus thin_pool_autoextend settings because the provisioner does not."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/advanced-operations/lvm-thin-provisioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LVM thin provisioning lets you over-provision: filesystems can be larger than the physical storage because virtual disks live inside a thin pool. In Local PV LVM it is controlled by the StorageClass parameter `thinProvision`, with values `"yes"` and `"no"`. The default is `"no"`, which gives thick volumes. A thin class also sets `volgroup` and, if you plan to resize, `allowVolumeExpansion: true`.

Before using it, the `dm_thin_pool` kernel module must be loaded on all nodes. Check with `lsmod | grep dm_thin_pool` and load with `modprobe dm_thin_pool`.

The driver creates the thin pool automatically with the first thin volume (the example pool is named like `lvmvg_thinpool`). Thin pools are logical volumes, so you extend them with the same commands as other logical volumes, but **you cannot reduce a thin pool**.

**The provisioner does not enable auto-extension**, because not every case wants it and some need a cap. So you must:

1. Turn on monitoring for every thin pool with `lvchange`, on all nodes. `lvs -o+seg_monitor` shows `not monitored` until you do; without this step, no automatic extension happens whatever `lvm.conf` says.
2. Edit `/etc/lvm/lvm.conf`. The defaults are `thin_pool_autoextend_threshold = 100` (never grows) and `thin_pool_autoextend_percent = 20`. Setting the threshold to 75 extends the pool when it is 75% full, by the percent value.

Recheck with `lvs -o+seg_monitor` to confirm the Monitor column reads `monitored`.

The page also says you must monitor the thin pool yourself and add capacity when it starts to fill, and that LVM configuration offers no way to cap how far auto-extension goes.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for lvm-thin-provisioning) in full. All claims match the page; only the closing monitoring note was added.
