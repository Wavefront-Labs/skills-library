---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodeclaim-lifecycle
name: karpenter-nodeclaim-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodeclaim, launch, registration, initialization, unregistered-taint, provisioning, insufficient-capacity]
level: practitioner
status: docs-checked
description: "NodeClaim lifecycle from pending pod to Initialized: compute, create, launch, register within 15 minutes, initialize, ICE handling, and example log messages to follow."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclaims.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodeClaim lifecycle

NodeClaims are immutable, cluster-scoped objects mapping one-to-one to a cloud instance and a Node. Karpenter creates them to satisfy pending pods (and for disruption pre-spin). Steps:

1. Watch pods; match their constraints to NodePool/NodeClass pairs. Log: `found provisionable pod(s)`.
2. Compute shape and size of NodeClaims. Log: `computed new nodeclaim(s) to fit pod(s)`.
3. Create the NodeClaim. Log: `created nodeclaim` with `requests` and the candidate `instance-types`.
4. Launch: translate to an EC2 call. On an unrecoverable error such as Insufficient Capacity, Karpenter deletes the NodeClaim, marks that instance type temporarily unavailable and creates another if needed. Log: `launched nodeclaim` (provider-id, instance-type, zone, capacity-type, allocatable).
5. Register: the instance joins as a node; Karpenter syncs labels, annotations, taints, owner refs and finalizer, then removes the `karpenter.sh/unregistered` taint. If this does not happen within 15 minutes the NodeClaim and instance are deleted and a replacement is created. Log: `registered nodeclaim`.
6. Initialize: wait for node Ready, startup taints removed and requested resources registered. Log: `initialized nodeclaim`.

Follow along:

```bash
export KARPENTER_NAMESPACE="kube-system"
kubectl logs -f -n "${KARPENTER_NAMESPACE}" -l app.kubernetes.io/name=karpenter
kubectl get nodeclaims
kubectl describe nodeclaim <name>
```

A NodeClaim `describe` shows whether launch, registration or initialization failed when a node is NotReady.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Removed the GPU device plugin aside, which is not on the NodeClaims page.
