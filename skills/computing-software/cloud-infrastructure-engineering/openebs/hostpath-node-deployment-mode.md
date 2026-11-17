---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-node-deployment-mode
name: hostpath-node-deployment-mode
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, node-deployment, daemonset, provisioner, helm, pvc-churn]
level: advanced
status: docs-checked
description: "Switch the Local PV Hostpath provisioner to Node-Deployment Mode (a DaemonSet doing in-process filesystem work, no helper pods) for high PVC churn and latency-sensitive workloads."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/advanced-operations/node-deployment-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the Local PV provisioner runs as a Deployment and uses helper operations to create and delete volume directories. **Node-Deployment Mode** runs it as a DaemonSet, one instance per node, and each instance performs the filesystem work (directory creation, quota setup, deletion) in-process on its own node, with no helper pod scheduled. Each instance handles only PVCs scheduled to its node and skips requests for other nodes as non-fatal. Leader election is disabled automatically because each instance is node-scoped.

The docs recommend it for **high PVC churn or latency-sensitive workloads**. It is opt-in and additive: existing PVs keep working and no migration is needed, and new PVCs are provisioned by the DaemonSet pods from then on.

Enable it through Helm:

```
helm upgrade openebs openebs/openebs \
  --namespace openebs \
  --set localpv-provisioner.nodeDeployment.enabled=true
```

If you enable it as part of a Helm upgrade, use `--reset-then-reuse-values` so the release resets to the new chart defaults, re-applies your existing values and then applies the new `--set` overrides.

Verify with `kubectl get po -n openebs`: you should see one `localpv-provisioner-node-*` pod per node, each Running. The page links to the XFS quota guide as a related feature, since quota setup is one of the operations the node instance performs directly.

## Checked

2026-11-04. Confirmed against the Node-Deployment Mode page: DaemonSet behaviour, per-node handling and disabled leader election, the recommendation, the opt-in and no-migration notes, the Helm value, `--reset-then-reuse-values`, and the verification pods. Nothing removed.

Method: documentation only; no commands were run.
