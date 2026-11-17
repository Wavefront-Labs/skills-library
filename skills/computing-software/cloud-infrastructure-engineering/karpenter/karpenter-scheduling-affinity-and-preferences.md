---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-scheduling-affinity-and-preferences
name: karpenter-scheduling-affinity-and-preferences
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [node-affinity, preferences, nodeselectorterms, relaxation, pod-affinity, anti-affinity, backoff]
level: advanced
status: docs-checked
description: "How Karpenter treats node affinity: preferred treated as required then relaxed one at a time, nodeSelectorTerms tried in order, and pod affinity/anti-affinity examples."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Affinity, preferences and anti-affinity

Preferences (preferred node affinity, pod affinity/anti-affinity, topology spread) are treated as requirements first. If they cannot be met Karpenter relaxes the pod's preferences one at a time and retries. Side effect: Karpenter prefers to create new nodes to satisfy preferences, so preferred affinities and `ScheduleAnyway` spreads can produce more nodes than expected. Preferred affinities are not treated as required when building topology requirements; use required affinities if that matters.

Node affinity terms: `matchExpressions` inside one term are ANDed; `nodeSelectorTerms` are ORed and tried in order, taking the first that works. If all fail Karpenter backs off and retries, so the pod schedules when capacity appears.

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - {key: topology.kubernetes.io/zone, operator: In, values: ["us-west-2a","us-west-2b"]}
          - {key: topology.kubernetes.io/zone, operator: NotIn, values: ["us-west-2b"]}
        - matchExpressions:
          - {key: karpenter.sh/capacity-type, operator: In, values: ["spot"]}
          - {key: topology.kubernetes.io/zone, operator: In, values: ["us-west-2d"]}
```

Pod affinity and anti-affinity:

```yaml
podAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
  - labelSelector: {matchExpressions: [{key: system, operator: In, values: [backend]}]}
    topologyKey: topology.kubernetes.io/zone
podAntiAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
  - labelSelector: {matchLabels: {app: inflate}}
    topologyKey: kubernetes.io/hostname
```

The first restricts to zones already running `system=backend` pods; the second prevents two `app=inflate` pods per node.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
