---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-expiration-expireafter
name: karpenter-expiration-expireafter
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [expiration, expireafter, forceful-disruption, terminationgraceperiod, node-lifetime, do-not-disrupt]
level: advanced
status: docs-checked
description: "Expiration as forceful disruption: spec.expireAfter default 720h, upper-bound semantics, interaction with budgets, and the stalled-drain risk without terminationGracePeriod."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter expiration (expireAfter)

Expiration is a forceful method: once a node's age exceeds the NodeClaim `spec.expireAfter`, draining starts. It is not rate limited by NodePool disruption budgets and does not wait for replacements to be healthy. PDBs are the only built-in way to pace application impact.

- Default `expireAfter` is `720h` (30 days).
- The NodePool field is `spec.template.spec.expireAfter`. Editing it does not update existing NodeClaims; it causes drift, and replacements get the new value.
- `expireAfter` is an upper bound: Drift, Consolidation or Emptiness can disrupt a node sooner if budgets allow. For a hard maximum, combine `expireAfter` with `terminationGracePeriod` and restrictive budgets.
- With `terminationGracePeriod`, maximum node lifetime = `expireAfter` + `terminationGracePeriod`.

Warning: blocking PDBs or `karpenter.sh/do-not-disrupt` pods can stall draining indefinitely. Do not use `expireAfter` with do-not-disrupt pods unless `terminationGracePeriod` is also set.

```yaml
spec:
  template:
    spec:
      expireAfter: 720h
      terminationGracePeriod: 48h
```

The do-not-disrupt annotation does not block Expiration, Interruption, Node Repair or manual deletion. The `48h` value is illustrative, not a recommendation from the page.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 disruption.md page; removed the claim about partially drained nodes raising cost and needing manual cleanup, and corrected "budgets that block the other reasons" to the page's wording. Default, drift and lifetime claims unchanged.
