---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodepool-requirements-and-labels
name: karpenter-nodepool-requirements-and-labels
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodepool, requirements, well-known-labels, instance-category, instance-generation, operators, zone, arch]
level: practitioner
status: docs-checked
description: "NodePool spec.template.spec.requirements: supported operators, AWS well-known labels, pod/NodePool overlap rule, tenancy label and the 100 requirement limit."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodepools.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePool requirements and well-known labels

`spec.template.spec.requirements` constrains launched nodes. Operators: `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt`, `Gte`, `Lte`. They are combined with the pod's nodeSelector, node affinity, pod affinity and topology spread; a pod's requirements must fall inside the NodePool's, otherwise no node launches. Undefined well-known labels allow any value the cloud provider offers; `requirements: []` is fully flexible, but some constraints are recommended to avoid exotic types.

Labels:
- Instance: `node.kubernetes.io/instance-type`, `karpenter.k8s.aws/instance-family`, `-category`, `-generation`, `-capability-flex`, `-cpu`, `-hypervisor`. Leave undefined where possible; non-HVM types unsupported.
- Zone: `topology.kubernetes.io/zone` (zone names differ across AWS accounts; use zone IDs for consistency).
- `kubernetes.io/arch`: `amd64`, `arm64`. `kubernetes.io/os`: `linux`, `windows`.
- `karpenter.k8s.aws/instance-tenancy`: `default`, `dedicated` (dedicated launches on a Dedicated Instance; if unspecified, default).

Recommended generic starting point:

```yaml
requirements:
  - {key: kubernetes.io/arch, operator: In, values: ["amd64"]}
  - {key: kubernetes.io/os, operator: In, values: ["linux"]}
  - {key: karpenter.sh/capacity-type, operator: In, values: ["on-demand"]}
  - {key: karpenter.k8s.aws/instance-category, operator: In, values: ["c","m","r"]}
  - {key: karpenter.k8s.aws/instance-generation, operator: Gte, values: ["3"]}
```

Limit: 100 requirements total on a NodePool and NodeClaim, and `spec.template.metadata.labels` are propagated as requirements, so requirements plus labels cannot exceed 100.

## Checked

2026-11-04. Confirmed against the NodePools concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
