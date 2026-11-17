---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodeclaim-status-and-conditions
name: karpenter-nodeclaim-status-and-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodeclaim, conditions, launched, registered, initialized, consolidatable, drifted, providerid]
level: practitioner
status: docs-checked
description: "Reading NodeClaim status: nodeName, providerID, imageID, capacity versus allocatable, and the condition types Launched through ConsistentStateFound."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclaims.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodeClaim status and conditions

`kubectl get nodeclaim` prints NAME, TYPE, ZONE, NODE, READY and AGE. `kubectl describe nodeclaim <name>` shows spec, status and events (for example `Launched`, `Registered`, `Initialized`, `Ready`, or `DisruptionBlocked`).

Status fields:
- `status.nodeName`: linked Node (set after registration).
- `status.providerID`: for example `aws:///us-west-2b/i-01234567adb205c7e`.
- `status.imageID`: the AMI.
- `status.capacity`: estimated full capacity including system reservations; includes extended resources like `vpc.amazonaws.com/pod-eni`.
- `status.allocatable`: capacity after reservations, what pods can use (typically lower).

Conditions (each with status, reason, message, lastTransitionTime):

| Type | Meaning |
|---|---|
| Launched | cloud instance created |
| Registered | joined cluster; labels, taints, owner refs synced |
| Initialized | node ready, startup taints gone, resources registered |
| Ready | True only when Launched, Registered and Initialized are True |
| Consolidatable | candidate for consolidation |
| Drifted | differs from NodePool/NodeClass |
| Drained | drained during termination |
| VolumesDetached | volumes detached during termination |
| InstanceTerminating | instance is being terminated |
| ConsistentStateFound | instance state verified consistent |

The page says the conditions are particularly useful when pods are not deploying to a node; a NotReady node may show the claim failed to launch, register or initialize.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Added the NAME column; replaced unsupported diagnostic guesses (bootstrap, security group, role, device plugin) with what the page states.
