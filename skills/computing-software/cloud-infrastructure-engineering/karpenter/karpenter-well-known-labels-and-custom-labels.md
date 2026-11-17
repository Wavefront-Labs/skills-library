---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-well-known-labels-and-custom-labels
name: karpenter-well-known-labels-and-custom-labels
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [labels, well-known-labels, instance-labels, exists-operator, custom-labels, restricted-labels, zone-id]
level: practitioner
status: docs-checked
description: "Karpenter well-known label catalogue, the domain-confusion trap, user-defined labels via Exists, restricted karpenter.sh labels, and deprecated label translation."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Well-known and custom labels

Well-known labels can be NodePool requirements or pod selectors. Core: `topology.kubernetes.io/zone`, `topology.k8s.aws/zone-id` (consistent across accounts, for example `use1-az1`), `node.kubernetes.io/instance-type`, `kubernetes.io/os`, `kubernetes.io/arch`, `node.kubernetes.io/windows-build` (10.0.17763 WS2019, 10.0.20348 WS2022, 10.0.26100 WS2025), `karpenter.sh/capacity-type`, `karpenter.sh/nodepool`.

AWS labels: `karpenter.k8s.aws/` plus `instance-category`, `-generation`, `-family`, `-size`, `-cpu`, `-cpu-manufacturer`, `-memory` (MiB), `-ebs-bandwidth`, `-network-bandwidth`, `-pods`, `-hypervisor`, `-local-nvme` (GiB), `-tenancy`, `-capability-flex`, `-encryption-in-transit-supported`, GPU and accelerator labels, `ec2nodeclass`, `capacity-reservation-id/-type/-interruptible`, `placement-group-id`, `placement-group-partition`.

Trap: `karpenter.k8s.aws/instance-family` enforces node properties, but `node.kubernetes.io/instance-family` is unknown to Karpenter and treated as a custom label that enforces nothing.

Custom labels: a nodeSelector or required nodeAffinity on a label Karpenter does not know leaves pods Pending. Declare it on the NodePool so Karpenter can satisfy it:

```yaml
requirements:
  - key: user.defined.label/type
    operator: Exists
```

Restricted: `karpenter.sh` labels outside the well-known table (for example `karpenter.sh/registered`, `karpenter.sh/initialized`) match existing nodes but never trigger provisioning, and NodePool CEL rejects `Exists` on them. Pin with `karpenter.sh/nodepool` instead.

Extra operators `Gte` and `Lte` work on numeric labels. Deprecated `failure-domain.beta.kubernetes.io/*` and `beta.kubernetes.io/*` labels are translated to stable equivalents.

## Checked

2026-11-04. Confirmed against the Scheduling concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
