---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-spot-to-spot-consolidation
name: karpenter-spot-to-spot-consolidation
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [spot, spottospotconsolidation, feature-gate, price-capacity-optimized, instance-type-flexibility, consolidation]
level: advanced
status: docs-checked
description: "Spot consolidation: deletion on by default, SpotToSpotConsolidation gate for replacement, the 15 instance-type flexibility minimum and why multi-node is exempt."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spot-to-spot consolidation

For spot nodes, deletion consolidation is on by default. Replacing one spot node with a cheaper spot node requires the `SpotToSpotConsolidation` feature gate (see the Karpenter settings feature gates).

Replacement spot types are chosen with the EC2 `price-capacity-optimized` allocation strategy. The cheapest type is sometimes not launched because of interruption likelihood, so Karpenter uses the count of instance types cheaper than the current one as a heuristic. This count is the launch's "instance type flexibility".

Rules when evaluating a spot replacement:
- Single node spot-to-spot (1 node to 1 node) needs a minimum instance type flexibility of 15 instance types in the launch request.
- Multi-node spot-to-spot (many nodes to 1) has no flexibility requirement, because it cannot cause a "race to the bottom".

Purpose of the 15-type floor:
1. Avoid repeatedly consolidating down to the lowest-priced spot type, which may have a high interruption rate.
2. Launch with enough types that the replacement likely has availability comparable to the current instance.

Implication (inferred from the 15-type rule): a NodePool restricted to few spot instance types is unlikely to meet the single-node minimum. The page names the `SpotToSpotConsolidation` gate and refers to the settings reference for how to enable it.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Removed the unsupported --feature-gates/FEATURE_GATES enable instructions and the advice to broaden requirements by family, size and generation; the implication is now marked as inferred.
