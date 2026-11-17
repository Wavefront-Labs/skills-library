---
id: computing-software.cloud-infrastructure-engineering.talos-linux.lvm-volume-groups-logical-volumes
name: lvm-volume-groups-logical-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [lvm, lvmvolumegroupconfig, lvmlogicalvolumeconfig, volume-group, logical-volume, wipe, csi]
level: advanced
status: docs-checked
description: "Provision LVM on Talos declaratively: volume groups from whole disks or raw volumes, logical volume types and sizing, inspecting pvs, vgs and lvs, and removal with talosctl wipe."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/lvm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos reconciles LVM from two documents: `LVMVolumeGroupConfig` selects whole disks or Talos volumes (CEL `volumeSelector`, with `volume` and, for disks, `disk` variables) and creates physical volumes and the group; `LVMLogicalVolumeConfig` creates logical volumes. Talos initializes every matched device as a physical volume, so selectors must match only intended devices; prefer serial, WWID or symlink over `/dev/sd*` (`talosctl get disks -o yaml`).

```yaml
# lvm.patch.yaml
apiVersion: v1alpha1
kind: LVMVolumeGroupConfig
name: vg-pool
provisioning:
  volumeSelector:
    match: disk.dev_path == "/dev/sdb" || disk.dev_path == "/dev/sdc"
---
apiVersion: v1alpha1
kind: LVMLogicalVolumeConfig
name: lv-data
type: linear
provisioning:
  volumeGroup: vg-pool
  maxSize: 80%
```

Apply with `talosctl --nodes <NODE> patch mc --patch lvm.patch.yaml`. Names are 1-63 characters of letters, digits, hyphens and underscores. Logical volume `type` is `linear`, `raid0`, `raid1` or `raid10`; `maxSize` is absolute (`50GiB`) or a percentage of the group; optional `minSize`, `mirrors` (default 1 for raid1 and raid10) and `stripes` (at least 2). Talos activates the volume (for example `/dev/vg-pool/lv-data`) but does not format or mount it.

To build on Talos partitions instead, create `RawVolumeConfig` documents and select labels with `volume.partition_label.startsWith("r-lvm")`.

Inspect with `talosctl get pvs`, `talosctl get vgs`, `talosctl get lvs`, and debug using `lvmphysicalvolumespecs`, `lvmvolumegroupspecs`, `lvmlogicalvolumespecs` and `lvmvalidationerrors`.

Remove: delete both documents first (otherwise Talos reconciles them again), then:

```bash
talosctl --nodes <NODE> wipe lv vg-pool/lv-data
talosctl --nodes <NODE> wipe vg vg-pool
talosctl --nodes <NODE> wipe pv /dev/sda1
```

Wiping a group removes all its logical volumes; PV labels persist until `wipe pv`.

## Checked

2026-11-04. Document fields, constraints, inspection resources and wipe commands confirmed on the LVM page.

Method: documentation only; no commands were run.
