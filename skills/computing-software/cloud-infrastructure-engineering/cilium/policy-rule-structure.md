---
id: computing-software.cloud-infrastructure-engineering.cilium.policy-rule-structure
name: policy-rule-structure
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, policy-rule, endpointselector, nodeselector, labels, description]
level: practitioner
status: docs-checked
description: "Anatomy of a Cilium policy rule: endpointSelector or nodeSelector, ingress, egress, labels, description, and the auto-added policy name label."
sources:
  - https://docs.cilium.io/en/stable/security/policy/intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policy rule structure

A Cilium rule has:
- `endpointSelector` or `nodeSelector` (mutually exclusive, not both empty). Both use the Kubernetes LabelSelector format; the endpoint selector matches endpoint labels only. `nodeSelector` is allowed only in CiliumClusterwideNetworkPolicy (see host policies).
- `ingress`: rules for packets entering the endpoint. Omitted or empty means no ingress rule.
- `egress`: rules for packets leaving it.
- `labels`: identify the rule so it can be listed or deleted by label; not required to be unique. Rules imported via Kubernetes automatically get `io.cilium.k8s.policy.name=NAME` from the NetworkPolicy or CiliumNetworkPolicy name.
- `description`: free text not interpreted by Cilium.

Rule with neither ingress nor egress has no effect. The Go type is `Rule` with `json` keys `endpointSelector`, `nodeSelector`, `ingress`, `egress`, `labels`, `description`.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the policy enforcement modes and rule basics page: https://docs.cilium.io/en/stable/security/policy/intro/. Confirmed the statements above. Nothing was removed.

Method: documentation only; no commands were run.
