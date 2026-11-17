---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodepool-weight-and-status
name: karpenter-nodepool-weight-and-status
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [weight, nodepool, status-conditions, nodeclassready, noderegistrationhealthy, validationsucceeded]
level: practitioner
status: docs-checked
description: "NodePool weight to prefer pools, mutually exclusive pools guidance, and status conditions NodeClassReady, ValidationSucceeded, NodeRegistrationHealthy, Ready."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePool weighting and status conditions

Behaviour:
- Karpenter does nothing without at least one NodePool, and loops through every NodePool.
- Recommended: make NodePools mutually exclusive, or weighted.
- If multiple NodePools match, Karpenter launches from the highest `spec.weight`, falling back to lower weights when it cannot use one (for example limits reached). No weight equals 0.
- `weight` cannot be set when `replicas` is set (static pool). Weight is a behavioural field that does not cause drift.

```yaml
spec:
  weight: 10
```

Kubelet settings now live on the EC2NodeClass, not the NodePool.

Status conditions:

| Condition | Meaning |
|---|---|
| NodeClassReady | underlying nodeClass is ready |
| ValidationSucceeded | NodePool CRD validation passed |
| NodeRegistrationHealthy | a misconfiguration is preventing launched nodes registering; needs manual investigation |
| Ready | top level, true only when all others are true |

`NodeRegistrationHealthy` is informational and does not affect `Ready`. A NodePool that is not Ready is not considered for scheduling. Each condition carries `observedGeneration`, `lastTransitionTime`, `reason` and `message`.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Added the Disruption page as a source for the claim that weight does not cause drift; other claims matched.
