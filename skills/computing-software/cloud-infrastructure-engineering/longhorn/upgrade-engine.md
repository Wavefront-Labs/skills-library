---
id: computing-software.cloud-infrastructure-engineering.longhorn.upgrade-engine
name: upgrade-engine
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [engine-upgrade, live-upgrade, offline-upgrade, engine-image, v1]
level: advanced
status: docs-checked
description: "Upgrade Longhorn V1 volume engines after a manager upgrade, with offline and live methods, the iSCSI frontend limit and temporary replica doubling."
sources:
  - https://longhorn.io/docs/1.13.0/deploy/upgrade/upgrade-engine/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move volumes to the engine image shipped with the new manager.

Applies to V1 Data Engine volumes. In v1.13.0 V2 volumes do not support live upgrade and must be detached before upgrading Longhorn. Back up volumes first and upgrade the manager before the engine.

Offline upgrade (use if live upgrade is unavailable or a volume is stuck degraded):
1. Detach the relevant workloads.
2. Batch-select volumes, click Upgrade Engine, and pick the engine image shipped with this release's manager.
3. Resume workloads. Volumes not owned by a Kubernetes workload must be attached from the Longhorn UI.

Live upgrade (supported from v1.12.x to v1.13.0):
- Not supported for the iSCSI frontend.
- Only on healthy volumes.
- Select the volume, Upgrade Engine in the dropdown, pick the engine image, OK. The UI normally lists only one image because it excludes the current one.
- During the upgrade the replica count temporarily doubles; afterwards it returns to the original count and the volume's Engine Image field updates.

For liveness and cleanup of old instance manager pods during live upgrade, see the Instance Manager Pods During Upgrade documentation.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/deploy/upgrade/upgrade-engine/ : offline and live upgrade steps, iSCSI limit, replica doubling. Removed an unsupported claim about when old instance manager pods are removed.

Method: documentation only; no commands were run.
