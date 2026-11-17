---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-do-not-disrupt-pods-and-pdbs
name: karpenter-do-not-disrupt-pods-and-pdbs
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [do-not-disrupt, pdb, pod-annotation, node-annotation, duration, voluntary-disruption]
level: advanced
status: docs-checked
description: "Blocking voluntary disruption: PDB combination rules, karpenter.sh/do-not-disrupt on pods (boolean or duration) and nodes, and which disruption methods ignore it."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Do-not-disrupt annotations and PDBs

PDBs: pods with blocking PDBs are not evicted by the Termination Controller and are excluded from voluntary disruption. A pod matching several PDBs needs all of them to permit eviction, and when pods on a node belong to different PDBs every PDB must allow eviction at the same time, so one blocking PDB can stop disruption of the whole node.

Pod annotation `karpenter.sh/do-not-disrupt`:

| Format | Example | Effect |
|---|---|---|
| Boolean | `"true"` | permanent protection |
| Go duration | `"30m"` | protected for that long after the pod starts running |

An invalid duration is ignored and an event is emitted on the pod. Duration protection stops misbehaving or long-running workloads blocking drift or consolidation indefinitely; permanent protection suits things like a long batch job that would have to restart.

Effects: nodes with active annotated pods are excluded from consolidation and conditionally from drift (nodes with a `terminationGracePeriod` can still drift). The annotated pods are not gracefully evicted; termination completes only when they are removed, the annotation expires, they reach Succeeded/Failed, or the NodeClaim `terminationGracePeriod` elapses.

Node-level: annotating a Node with `karpenter.sh/do-not-disrupt: "true"` blocks voluntary disruption of that node. To stop voluntary disruption for every node a NodePool launches, set a budget of `nodes: "0"`.

Not covered: the annotation does not block Expiration, Interruption, Node Repair or manual deletion. Do not use `expireAfter` with do-not-disrupt pods unless `terminationGracePeriod` is also set.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 disruption.md page; removed the specific "maxUnavailable: 0 / minAvailable: 100%" PDB examples and the pod-template YAML snippet as not in the page; added node-level budget and use-case notes from the page.
