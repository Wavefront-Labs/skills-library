---
id: computing-software.cloud-infrastructure-engineering.openebs.uninstall-openebs-helm-and-rawfile
name: uninstall-openebs-helm-and-rawfile
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [uninstall, helm, rawfile, crds, finalizers, loop-device, cleanup]
level: practitioner
status: docs-checked
description: "Uninstall OpenEBS cleanly: delete volumes and pools first, helm uninstall, the separate Rawfile release and its deletion order, and the CRDs that stay behind."
sources:
  - https://openebs.io/docs/user-guides/uninstall
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The prerequisites for a graceful uninstall are that **volumes are cleaned up** and **pools are cleaned up**. Without that, finalizers and protection rules imposed by the engines can cause errors.

Then run `helm uninstall openebs -n <OPENEBS_NAMESPACE>`.

**Local PV Rawfile** is a separate Helm release and must be removed on its own. To avoid leaked loop device mounts, delete resources in this order:

1. all VolumeSnapshots;
2. all PersistentVolumeClaims;
3. all PersistentVolumes.

Then run `helm uninstall rawfile-localpv -n openebs`. You may also remove the data directory from each node yourself (default `/var/csi/rawfile`). If you uninstall first, loop devices and mounts can be left on the nodes and need manual cleanup.

**CRDs are not removed.** Helm uninstall leaves these behind: `diskpools.openebs.io`, `lvmnodes.local.openebs.io`, `lvmsnapshots.local.openebs.io`, `lvmvolumes.local.openebs.io`, the three `snapshot.storage.k8s.io` kinds (volumesnapshotclasses, volumesnapshotcontents, volumesnapshots), and the ZFS kinds `zfsbackups`, `zfsnodes`, `zfsrestores`, `zfssnapshots` and `zfsvolumes` under `zfs.openebs.io`. The page does not give a command for removing them.

## Checked

Method: 2026-11-08 read the raw markdown of the cited uninstallation page in full; prerequisites, Rawfile deletion order, default data directory and the CRD list match. Removed an unsupported advice clause about checking snapshot CRD use.
