---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-topology-spread-and-zonal-shift
name: karpenter-topology-spread-and-zonal-shift
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [topologyspreadconstraints, maxskew, zone-spread, zonal-shift, arc-zonal-shift, capacity-type-spread]
level: advanced
status: docs-checked
description: "Topology spread with Karpenter: supported topology keys, maxSkew behaviour, no automatic zone balancing, and AWS Zonal Shift integration permissions."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Topology spread and Zonal Shift

Karpenter honours `topologySpreadConstraints` with three topology keys: `topology.kubernetes.io/zone`, `kubernetes.io/hostname`, `karpenter.sh/capacity-type`.

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels: {dev: jjones}
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels: {dev: jjones}
```

- Use a selector matching all pods of the Deployment. With three nodes and five pods and `maxSkew: 1`, spreads like 1,2,2 are allowed; `maxSkew: 5` permits 5,0,0.
- NodePools do not balance or rebalance zones by themselves. Add zonal spread constraints on pods that need multi-zone durability.
- `ScheduleAnyway` is a preference and can create extra nodes; it also lowers consolidation effectiveness.

Zonal Shift: if AWS ARC Zonal Shift is enabled for the EKS cluster, Karpenter watches for active shifts and does not launch nodes in the impaired zone. Requirements: the Karpenter IAM policy must allow `arc-zonal-shift:GetManagedResource`, and the EKS cluster must be enabled for Zonal Shift (see the getting-started Zonal Shift Onboarding section). Zonal Shift itself cordons nodes, stops termination and eviction, and removes endpoints from EndpointSlices in the impaired zone.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Added the Disruption page as a source for the claim that preferred spreads reduce consolidation effectiveness; other claims matched.
