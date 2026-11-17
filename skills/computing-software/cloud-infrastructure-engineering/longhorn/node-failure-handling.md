---
id: computing-software.cloud-infrastructure-engineering.longhorn.node-failure-handling
name: node-failure-handling
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [node-failure, pod-deletion-policy, statefulset, recovery, volumes]
level: advanced
status: docs-checked
description: "What happens to Longhorn volumes and pods when a node goes down, the Pod Deletion Policy When Node is Down setting and recovery timelines."
sources:
  - https://longhorn.io/docs/1.13.0/high-availability/node-failure/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict and shorten recovery from a failed node.

Timeline (approximate, per the page): about 1 minute until `kubectl get nodes` shows `NotReady`; about 5 minutes until pods on the node become `Unknown` or `NodeLost`.

Behaviour:
- StatefulSet pods are not force-deleted by Kubernetes because they have a stable identity.
- A Deployment with an RWO volume cannot attach the volume to two nodes, so the replacement pod stays `ContainerCreating` while the old pod holds the volume. The old pod is evicted but sits in `Terminating`, so without intervention the new pod stays stuck.

Fix: the Longhorn setting Pod Deletion Policy When Node is Down (UI Settings tab) force-deletes terminating StatefulSet or Deployment pods on the down node. Kubernetes then detaches the volume and starts replacements on another node.

Recovery of the node:
- Within about 5 to 6 minutes: Kubernetes restarts the pods and remounts volumes without re-attaching. Longhorn detaches and re-attaches volumes to restore the engines because the device no longer exists on the node.
- After about 5 to 6 minutes: pods are already evicted and `Terminating`. On recovery Kubernetes restarts them, detaches volumes, waits for old VolumeAttachment cleanup, then re-attaches and re-mounts. This typically takes 1 to 7 minutes.

No manual steps are needed in either case; Longhorn recovers automatically with Kubernetes.

Check node state with `kubectl get nodes`.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/high-availability/node-failure/

No claim needed changing.

Method: documentation only; no commands were run.
