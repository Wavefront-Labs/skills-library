---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-feature-gates
name: karpenter-feature-gates
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [feature-gates, spottospotconsolidation, noderepair, reservedcapacity, nodeoverlay, staticcapacity, drift]
level: practitioner
status: docs-checked
description: "Karpenter feature gates, defaults and stages (SpotToSpotConsolidation, NodeRepair, ReservedCapacity, NodeOverlay, StaticCapacity), setting FEATURE_GATES, drift gate removal."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/settings.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter feature gates

Set with `--feature-gates` or the `FEATURE_GATES` environment variable on the Karpenter deployment:

```
--feature-gates SpotToSpotConsolidation=true,ReservedCapacity=true
```

Current options and defaults: `NodeRepair=false`, `ReservedCapacity=true`, `SpotToSpotConsolidation=false`, `NodeOverlay=false`, `StaticCapacity=false`.

| Feature | Default | Stage | Since | Until |
|---|---|---|---|---|
| Drift | false | Alpha | v0.21.x | v0.32.x |
| Drift | true | Beta | v0.33.x | v0.37.x |
| SpotToSpotConsolidation | false | Alpha | v0.34.x | |
| NodeRepair | false | Alpha | v1.1.x | |
| ReservedCapacity | false | Alpha | v1.3.x | v1.5.x |
| ReservedCapacity | true | Beta | v1.6.x | |
| NodeOverlay | false | Alpha | v1.7.x | |
| StaticCapacity | false | Alpha | v1.8.x | |

In v1 drift is stable and its gate removed. Control it with disruption budgets by reason instead:

```yaml
budgets:
- nodes: 10%
- nodes: "0"
  schedule: "0 9 * * mon-fri"
  duration: 8h
  reasons: [Drifted]
- nodes: "10%"
  reasons: [Drifted]
```

## Checked

2026-11-04. Confirmed against the Settings reference (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed gate-to-feature mapping line.

Method: documentation only; no commands were run.
