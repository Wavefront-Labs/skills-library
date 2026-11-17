---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodepool-disruption-budgets
name: karpenter-nodepool-disruption-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [budgets, disruption-budgets, nodes, reasons, schedule, duration, rate-limit, nodepool]
level: advanced
status: docs-checked
description: "NodePool disruption budgets: default 10 percent, percentage vs static math, reasons Drifted/Underutilized/Empty, schedule and duration windows, minimum across budgets."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePool disruption budgets

`spec.disruption.budgets` rate-limits voluntary disruption (drift, emptiness, consolidation). Default if undefined: one budget with `nodes: 10%`. Budgets do not stop expiration, and forceful methods ignore them. Nodes already deleting count against the budget.

Math: percentage = `roundup(total * pct) - total_deleting - total_notready`; a static number = `n - total_deleting - total_notready`. With several budgets, the minimum (most restrictive) applies per reason.

`reasons`: any of `Drifted`, `Underutilized`, `Empty`; omitted means all reasons.

`schedule` is cron (five fields or `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly`), always UTC, no time zones. `duration` is minutes/hours only (`10h5m`, `30m`, `160h`). They must be set together; if both are omitted the budget is always active.

```yaml
spec:
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    budgets:
    - nodes: "20%"
      reasons: ["Empty", "Drifted"]
    - nodes: "5"
    - nodes: "0"
      schedule: "@daily"
      duration: 10m
      reasons: ["Underutilized"]
```

With 19 nodes the first budget allows 4 (19 x 0.2 = 3.8 rounded up). The second caps at 5. The third blocks underutilized disruption for 10 minutes after 00:00 UTC.

Block all voluntary disruption on a NodePool with a single budget of `nodes: "0"`.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
