---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-online-resize-and-limits
name: rawfile-online-resize-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, resize, allowvolumeexpansion, csi-resizer, block-mode, expansion]
level: practitioner
status: docs-checked
description: "Expand a Local PV Rawfile volume online (ext4, xfs, btrfs): chart and StorageClass settings, block-mode behaviour, no shrinking, and fixes when capacity never updates."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/advanced-operations/rawfile-resize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rawfile supports **online expansion**: the backing file, loop device and filesystem all grow live, with no pod restart. Shrinking is not supported, and Kubernetes rejects reduce requests.

Requirements:

- resize enabled in the chart (default `capabilities.resize.enabled=true`);
- `allowVolumeExpansion: true` on the StorageClass;
- online growth on `ext4`, `xfs` or `btrfs`;
- enough free capacity in the volume's pool on its node. Expanding beyond pool free space fails with `Not enough disk space`.

Edit the PVC's `spec.resources.requests.storage` to the larger size, or patch it in place, then watch the capacity and events. Internally, the `csi-resizer` sidecar calls the controller, which forwards to the node owning the volume; the node grows the backing file, resizes the loop device and expands the filesystem. Verify inside the pod; the new size shows immediately.

**Block mode** volumes (`volumeMode: Block`) are expandable too. If no pod uses the volume, only the backing file grows and node-side expansion waits for the next attach. The application must notice the larger device.

If the PVC capacity never updates, check that `allowVolumeExpansion` is true, that `capabilities.resize.enabled=true`, and that the controller deployment is running, using `kubectl -n openebs logs deploy/<release>-controller`.

Other symptoms from the page's troubleshooting table:

- `Not enough disk space`: the pool on the volume's node lacks free capacity; free space or grow the underlying disk, and watch the `rawfile_pool_remaining_capacity_bytes` metric.
- `Resizing capabilities are disabled`: set `capabilities.resize.enabled=true` and upgrade the Helm release.
- Filesystem size unchanged but the PV shows the new size: node-side expansion is pending; make sure the node plugin is healthy, since kubelet triggers `NodeExpandVolume` on the mounted node.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for rawfile-resize) in full. Existing claims match the page; added its troubleshooting rows.
