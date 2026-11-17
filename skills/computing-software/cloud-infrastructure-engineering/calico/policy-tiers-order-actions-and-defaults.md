---
id: computing-software.cloud-infrastructure-engineering.calico.policy-tiers-order-actions-and-defaults
name: policy-tiers-order-actions-and-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [network-policy, tiers, order, pass, defaultaction, kube-admin, kube-baseline, globalnetworkpolicy]
level: advanced
status: docs-checked
description: "Use Calico tiers for policy precedence: tier order, fixed default tier at 1000000, Pass versus implicit tier deny, defaultAction Pass, and kube-admin/kube-baseline tiers."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/policy-tiers/tiered-policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tiers group policies and enforce higher precedence that other teams cannot override. All Calico and Kubernetes network policies live in a tier. Lower `order` is evaluated first. A suggested split is platform, security and application tiers.

```yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
  name: security
spec:
  order: 300
```

**Built-in tiers.**

- `default`: order 1,000,000, fixed. Holds Kubernetes network policies and any Calico policy without an explicit tier; evaluated last.
- `kube-admin`: order 1,000, default action `Pass`, fixed. Holds Kubernetes `ClusterNetworkPolicy` with `tier: Admin`.
- `kube-baseline`: order 10,000,000, default action `Pass`, fixed. Holds `ClusterNetworkPolicy` with `tier: Baseline`.

For `ClusterNetworkPolicy`, `priority` maps to `order` so they sort with Calico policies placed in those tiers.

**Actions.** `Allow` and `Deny` end evaluation. `Pass` skips to the next tier that applies to the endpoint. `Log` logs and continues. At the end of each tier is an **implicit default deny** for endpoints the tier selects, so you must either end with a `Pass` rule or set the tier's `defaultAction: Pass`:

```yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
  name: devops
spec:
  order: 300
  defaultAction: Pass
```

If no policy in a tier selects an endpoint, evaluation moves on to the next tier.

**Default endpoint behaviour:** Calico workloads deny; Kubernetes workloads allow ingress from the same namespace and all egress; host endpoints deny, except auto host endpoints which get default-allow.

Limit tier creation and reordering to admins, and re-check Pass rules whenever tiers change.

## Checked

2026-11-04. Tier orders, actions, YAML and best practices were confirmed on the policy tiers page.

Method: documentation only; no commands were run.
