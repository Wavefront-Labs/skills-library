---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-manual-node-deletion
name: karpenter-manual-node-deletion
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [kubectl, nodeclaim, nodepool-deletion, cascade-deletion, finalizer, owner-reference]
level: practitioner
status: docs-checked
description: "Manually removing Karpenter nodes: kubectl delete node or nodeclaim, label-selector deletes by nodepool, and cascading deletion when a NodePool is removed."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manually deleting Karpenter nodes and NodePools

Each Karpenter node is owned by a NodeClaim, so deleting either one cascades to the other and runs the graceful termination flow (taint, drain, terminate instance).

```bash
# one nodeclaim or node
kubectl delete nodeclaim $NODECLAIM_NAME
kubectl delete node $NODE_NAME

# all nodeclaims
kubectl delete nodeclaims --all

# all nodes owned by any nodepool
kubectl delete nodes -l karpenter.sh/nodepool

# all nodeclaims of one nodepool
kubectl delete nodeclaims -l karpenter.sh/nodepool=$NODEPOOL_NAME
```

NodePool deletion: NodeClaims carry an owner reference to the NodePool that launched them, so deleting the NodePool gracefully terminates all of its nodes by cascading deletion.

Why the finalizer matters: on a node without Karpenter's finalizer, `kubectl delete node` only removes the API object. The kubelet does not watch for its own node object, so it keeps running, the EC2 instance continues running, and the pod objects are only garbage collected later. Karpenter's finalizer ensures the drain and instance termination happen first.

Manual deletion is a forceful path: `karpenter.sh/do-not-disrupt` pod annotations and NodePool budgets do not stop it, and blocking PDBs or do-not-disrupt pods can stall the drain unless `terminationGracePeriod` is set.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Dropped the unsupported billing claim.
