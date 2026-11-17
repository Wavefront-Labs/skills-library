---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-disruption-control-flow
name: karpenter-disruption-control-flow
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [disruption-controller, termination-controller, finalizer, disrupted-taint, drain, eviction-api]
level: practitioner
status: docs-checked
description: "How the Karpenter Disruption and Termination controllers process a node: candidate selection, simulation, disrupted taint, replacement pre-spin, drain order."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter disruption and termination flow

Karpenter adds a finalizer to every node and NodeClaim it provisions, so deletion blocks until the Termination Controller has drained the node and removed the NodeClaim. Without it, `kubectl delete node` removes the node object but leaves the EC2 instance running. Disruption can come from the Disruption Controller, a manual `kubectl delete`, or an external system deleting the node object.

The Disruption Controller runs one automated method at a time, Drift first and then Consolidation:
1. Build a prioritised candidate list. Nodes with pods that cannot be evicted are skipped and retried later; with no candidates, move to the next method.
2. For each candidate, check the NodePool disruption budget and run a scheduling simulation to see if replacements are needed.
3. Add the `karpenter.sh/disrupted:NoSchedule` taint.
4. Pre-spin replacements and wait for them to be ready. If a replacement fails to initialise, the taint is removed and the process restarts from the first method.
5. Delete the node(s) and wait for graceful termination, then restart from the first method.

The Termination Controller (modelled on Kubernetes Graceful Node Shutdown):
1. Apply the `karpenter.sh/disrupted:NoSchedule` taint.
2. Evict pods via the Eviction API, so PDBs are honoured. Static pods, pods tolerating the disrupted taint and Succeeded/Failed pods are skipped.
3. Confirm VolumeAttachments for drainable pods are deleted.
4. Terminate the NodeClaim at the cloud provider.
5. Remove the finalizer so the node object is deleted.

If the NodeClaim disappears while waiting, the finalizer is removed.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 disruption.md page. Flow steps confirmed; added the "no candidates" step, manual and external deletion sources and the graceful-termination wait.
