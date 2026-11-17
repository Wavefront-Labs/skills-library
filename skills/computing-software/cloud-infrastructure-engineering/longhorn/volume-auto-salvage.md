---
id: computing-software.cloud-infrastructure-engineering.longhorn.volume-auto-salvage
name: volume-auto-salvage
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [salvage, recovery, faulty-replicas, workload-pod, detached]
level: practitioner
status: docs-checked
description: "Longhorn automatic salvage when all replicas fault, and the setting that auto-deletes workload pods when a volume detaches unexpectedly."
sources:
  - https://longhorn.io/docs/1.13.0/high-availability/recover-volume/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand how Longhorn recovers a volume whose replicas all went faulty.

Auto salvage: when all of a volume's replicas become faulty, often from a network issue, Longhorn salvages the volume automatically. It identifies the usable replicas and uses them for the volume. This can trigger Automatic Workload Pod Deletion.

Setting: Automatically Delete Workload Pod when The Volume Is Detached Unexpectedly. Disable it in the Longhorn UI to stop Longhorn deleting workload pods after an unexpected detach.

Pods without a controller are never deleted by Longhorn. Delete and restart them manually to recover.

Practical sequence:
1. Check the volume in the UI; a volume with all replicas faulty is salvaged without action.
2. For a pod with a controller (Deployment, StatefulSet, DaemonSet), Longhorn deletes it after the salvage so the controller restarts it and Kubernetes remounts the volume.
3. If the pod has no controller, delete it yourself and recreate it.
4. If you do not want pods deleted automatically, turn the setting off and restart pods yourself.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/high-availability/recover-volume/ : automatic workload pod deletion triggers, setting name, controller-less pods. Reworded step 2 to match the page and removed a statement about what the page omits.

Method: documentation only; no commands were run.
