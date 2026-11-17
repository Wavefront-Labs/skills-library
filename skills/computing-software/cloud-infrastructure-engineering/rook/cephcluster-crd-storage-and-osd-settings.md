---
id: computing-software.cloud-infrastructure-engineering.rook.cephcluster-crd-storage-and-osd-settings
name: cephcluster-crd-storage-and-osd-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [storage, usealldevices, usea, fullratio, nearfullratio, backfillfullratio, flapping, osdmaxupdatesinparallel]
level: advanced
status: docs-checked
description: "OSD-related CephCluster settings: node selection, full ratios, flapping restart, parallel update limit, device class and CRUSH weight updates."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/ceph-cluster-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Under `spec.storage`:
- `useAllNodes`: whether every node is used for storage. If you list individual `nodes`, `useAllNodes` must be false.
- `nodes`: nodes whose storage is included, with optional per-node overrides.
- `config`: settings applied to all OSDs on the node unless overridden by devices.
- `allowDeviceClassUpdate`: default false, to avoid accidental data movement when a device class changes.
- `allowOsdCrushWeightUpdate`: default false; when true, a larger OSD PVC resizes the CRUSH weight and triggers rebalancing, which can briefly slow the cluster.
- `osdMaxUpdatesInParallel`: maximum OSDs down at once during an update, default 20. Updates always occur when the operator restarts and only ok-to-stop OSDs are taken down. Lower it to keep more OSDs online.

Spec-level OSD settings:
- `fullRatio` 0.95: Ceph blocks IO.
- `backfillFullRatio` 0.90: Ceph stops backfilling.
- `nearFullRatio` 0.85: health warning raised.
- `flappingRestartIntervalHours`: an OSD marked down more than 5 times in 600 seconds is flapping and its pod sleeps this long before restarting; 0 disables the sleep.
- `scheduleAlways`: schedule OSDs on explicitly listed nodes even if temporarily unschedulable; consider tolerations.
- `onlyApplyOSDPlacement`: apply only the OSD placement and ignore `all`.
- `removeOSDsIfOutAndSafeToRemove`: remove OSDs that are down and safe to destroy.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-cluster-crd) against this skill: 16 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 1 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
