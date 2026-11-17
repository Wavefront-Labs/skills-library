---
id: computing-software.messaging-and-integration.strimzi.recover-deleted-cluster
name: recover-deleted-cluster
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [cluster-recovery, persistent-volumes, pvc-recreate]
level: sme
status: docs-checked
description: "Recover a deleted Kafka cluster from persistent volumes."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recovering a deleted cluster

**Goal:** bring a cluster back from retained volumes.

Recreate the original PVCs bound to the retained PVs, then redeploy. Critical: PVs must mount into the **correct PVC** or data may be corrupted; specify `volumeName` in the PVC matching the PV name.

```bash
kubectl get pv
```

Recreate `KafkaTopic` and `KafkaUser` resources if those operators are deployed. Recreate topics with the **same configurations**, or the Topic Operator will try to update them in Kafka. Warning: if the User Operator is enabled and users are not recreated, users are deleted from Kafka immediately after recovery.

PVCs are retained by default when a Kafka cluster is deleted, which is what makes this possible.

**Checklist**

1. Match PV and PVC names exactly.
2. Recreate users and topics unchanged.
3. Check the PV-to-PVC mapping before deploying the Kafka resource.

## Checked

2026-11-03. Confirmed in Recovering a deleted Kafka cluster: recreate PVCs with volumeName matching the PV, same KafkaTopic configurations, the User Operator deletion warning, and that PVCs are retained by default on deletion. Removed the pause-reconciliation step because the recovery procedure does not state it.

Method: documentation only; no commands were run.
