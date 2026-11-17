---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodeoverlay-conflicts-and-consolidation
name: karpenter-nodeoverlay-conflicts-and-consolidation
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodeoverlay, weight, conflict-resolution, validationsucceeded, consolidation, merge]
level: advanced
status: docs-checked
description: "How multiple NodeOverlays combine: weight precedence, alphabetical tie-break, field-level merge, Conflict status, and effects on consolidation without drift."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeoverlays.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodeOverlay conflicts and consolidation effects

When several overlays match one instance type:
1. Higher `spec.weight` wins (default 0).
2. Equal weights: applied in alphabetical order by name. If same-weight overlays conflict, the status says so and the overlay is not applied.
3. Field-level merge: a higher weight overrides lower-weight fields such as the price adjustment, but `capacity` maps from different overlays are merged.

Example: overlay-a (weight 5: `priceAdjustment: -10%`, `hugepages-2Mi: 50Mi`) and overlay-b (weight 10: `-20%`, `custom-device/gpu: 1`) on m5.large yield price `-20%` and capacity `hugepages-2Mi: 50Mi` plus `custom-device/gpu: 1`.

Status: `Ready=True` means applied to matching types; `Ready=False` shows a conflict, requirement mismatch or other error. Example condition:

```yaml
- type: ValidationSucceeded
  status: "False"
  reason: "Conflict"
  message: "conflict with another overlay"
```

Consolidation: price adjustments change the cost calculation used to choose replacements, and capacity additions count when judging whether workloads fit on other nodes. No drift or forced replacement is triggered; changes are picked up in the next consolidation evaluation, which may replace nodes if the optimal instance choice changes materially.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
