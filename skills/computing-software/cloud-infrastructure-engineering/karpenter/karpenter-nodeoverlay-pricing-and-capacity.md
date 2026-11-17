---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodeoverlay-pricing-and-capacity
name: karpenter-nodeoverlay-pricing-and-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodeoverlay, price, priceadjustment, capacity, extended-resources, requirements, alpha, feature-gate]
level: advanced
status: docs-checked
description: "NodeOverlay (alpha, karpenter.sh/v1alpha1): requirements selecting instance types, price vs priceAdjustment, extended resource capacity, the NodeOverlay gate and its limitations."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeoverlays.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodeOverlay pricing and capacity

Alpha. NodeOverlays change the instance type data Karpenter uses in its scheduling simulation: pricing (savings plans, licensing) and added extended resources. Enable the gate: `--feature-gates NodeOverlay=true` or set it in the ConfigMap.

```yaml
apiVersion: karpenter.sh/v1alpha1
kind: NodeOverlay
metadata:
  name: example-overlay
spec:
  weight: 10
  requirements:
    - {key: node.kubernetes.io/instance-type, operator: In, values: ["m5.large","m5.xlarge"]}
    - {key: karpenter.sh/capacity-type, operator: In, values: ["spot"]}
  priceAdjustment: "+10%"
  capacity:
    hugepages-2Mi: 100Mi
    custom-device/gpu-slice: 4
```

- `requirements`: same format as NodePool requirements (max 100); empty array matches all instance types.
- `price`: absolute hourly price string replacing the provider price; currency-agnostic. Mutually exclusive with `priceAdjustment`.
- `priceAdjustment`: absolute (`"+5.00"`, `"-2.50"`) or percent (`"+15%"`, `"-10%"`).
- `capacity`: extended resources only; added to existing capacity, cannot change CPU, memory or storage.

Limitations: capacity changes affect only the simulation, so the node must really provide the resource (device plugin, config); price adjustments steer decisions but do not change AWS billing; the API (v1alpha1) may change.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Replaced the unsupported FEATURE_GATES environment variable with the ConfigMap option the page mentions.
