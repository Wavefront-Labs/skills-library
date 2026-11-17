---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-consolidation-policy
name: karpenter-consolidation-policy
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [consolidation, consolidationpolicy, consolidateafter, whenemptyorunderutilized, whenempty, nodepool]
level: practitioner
status: docs-checked
description: "Consolidation settings and mechanisms: consolidationPolicy, consolidateAfter, empty/multi/single node consolidation, selection preference, Unconsolidatable events."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter consolidation policy

Set in the NodePool `spec.disruption` block. Defaults when unset:

```yaml
spec:
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 0s
```

- `consolidationPolicy`: `WhenEmpty` (only nodes with no running non-daemon pods) or `WhenEmptyOrUnderutilized` (consolidatable once `consolidateAfter` elapses, empty or not).
- `consolidateAfter`: how long to wait after a pod schedules to or leaves the node before it is consolidatable.

Two actions: Deletion (pods fit on free capacity of other nodes) and Replace (pods fit on other nodes plus one cheaper replacement).

Three mechanisms are tried in order: Empty Node Consolidation (delete empty nodes in parallel), Multi Node Consolidation (two or more nodes together, possibly with one cheaper replacement, picked by a heuristic), Single Node Consolidation (each node individually, possibly with one cheaper replacement).

Karpenter prefers the least disruptive option: nodes with fewer pods, nodes expiring soon, nodes with lower-priority pods.

Consolidation is a graceful method, rate limited by NodePool disruption budgets (reason `Underutilized` or `Empty`).

Spot: spot nodes get deletion consolidation by default. Spot-to-spot replacement needs the `SpotToSpotConsolidation` feature flag; single-node spot-to-spot replacement needs at least 15 instance type options, multi-node has no such requirement.

Diagnose a node that will not consolidate by reading its events: Karpenter emits `Unconsolidatable` events giving the reason, such as a blocking PDB or no cheaper replacement.

Preferred anti-affinity and topology spread constraints can block consolidation to avoid churn; Karpenter logs such pods.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 disruption.md page; removed the verbatim event and log message strings (page describes the reasons, not exact text) and added budget and spot detail from the page. Defaults, policy values and mechanism order unchanged.
