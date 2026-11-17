---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-minvalues-flexibility
name: karpenter-minvalues-flexibility
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [minvalues, min-values-policy, besteffort, strict, flexibility, requirements, alpha]
level: advanced
status: docs-checked
description: "minValues in NodePool requirements: enforcing instance flexibility, Strict vs BestEffort via MIN_VALUES_POLICY, max of multiple minValues for a key, and examples."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# minValues flexibility

`minValues` on a NodePool requirement forces the scheduler to consider at least N unique values for the key when placing pods, keeping instance diversity (important for spot).

```yaml
requirements:
  - key: karpenter.sh/capacity-type
    operator: In
    values: ["spot"]
  - key: karpenter.k8s.aws/instance-category
    operator: In
    values: ["c", "m", "r"]
    minValues: 2
  - key: karpenter.k8s.aws/instance-family
    operator: Exists
    minValues: 5
  - key: node.kubernetes.io/instance-type
    operator: Exists
    minValues: 10
```

This needs 2 categories, 5 families and 10 instance types.

Policy: flag `--min-values-policy` or env `MIN_VALUES_POLICY`.
- `Strict`: if the minimum cannot be met, scheduling fails for that NodePool; Karpenter falls back to another NodePool that satisfies the pod, or the pod fails to schedule.
- `BestEffort`: Karpenter relaxes `minValues` until it can be met.

Several entries for the same key with different operators are allowed; the scheduler uses the maximum `minValues` for that key. For example `instance-family Exists minValues: 5` plus `instance-family In [m5,m5d,c5,c5d,c4,r4] minValues: 3` requires at least 5 families.

## Checked

2026-11-04. Confirmed against the NodePools concept page (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed 'alpha' labelling.

Method: documentation only; no commands were run.
