---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-capacity-type-fallback
name: karpenter-capacity-type-fallback
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [capacity-type, spot, on-demand, reserved, fallback, capacity-reservation, ice-cache]
level: advanced
status: docs-checked
description: "Capacity type selection: spot, on-demand, reserved priority order, 3 minute unavailable-offering cache, fallback only to allowed types, and reserved meaning capacity reservations."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Capacity types and fallback

Label `karpenter.sh/capacity-type` takes `spot`, `on-demand` or `reserved` (analogous to EC2 purchase options). `reserved` means capacity reservations (On-Demand Capacity Reservations and Capacity Blocks), not Reserved Instances. The page states no default; requirements are optional and Karpenter does not enforce that you set any. It recommends `["on-demand"]` for most use cases.

Priority when a NodePool allows several: `reserved`, then `spot`, then `on-demand`; so with spot and on-demand allowed, spot is preferred.

Behaviour on shortage:
- If the provider API reports capacity unavailable, Karpenter caches that result for that instance type and zone for the next 3 minutes, across all provisioning attempts.
- If a higher-priority option is unavailable it moves to a lower one, generally within milliseconds.
- It only falls back to capacity types the NodePool allows. A NodePool allowing only `spot` never launches on-demand, and pods stay Pending until a spot offering can be launched.

`karpenter.sh/capacity-type` can also be used as a topology key for topology spread.

```yaml
- key: karpenter.sh/capacity-type
  operator: In
  values: ["spot", "on-demand"]
```

For spot instances the page's `minValues` section advises specifying `karpenter.sh/capacity-type: spot` in requirements.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodepools.md page; removed the 15-candidate spot-to-spot note (it comes from the disruption page, not this one) and the `minValues` flexibility advice beyond what the page says. Priority order, 3-minute cache and fallback rules unchanged.
