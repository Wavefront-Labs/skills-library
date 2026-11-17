---
id: computing-software.cloud-infrastructure-engineering.calico.networkpolicy-resource-spec-types-and-hints
name: networkpolicy-resource-spec-types-and-hints
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [network-policy, networkpolicy, order, types, selector, performancehints, serviceaccountselector, spec]
level: advanced
status: docs-checked
description: "Spec essentials of the Calico NetworkPolicy resource: namespaced scope, tier and order, selector, how types is defaulted from rules present, and the AssumeNeededOnEveryNode hint."
sources:
  - https://docs.tigera.io/calico/latest/reference/resources/networkpolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`NetworkPolicy` is namespaced: it applies only to workload endpoints in its own namespace (`GlobalNetworkPolicy` is the non-namespaced form). It takes precedence over profiles.

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-tcp-6379
  namespace: production
spec:
  selector: role == 'database'
  types:
    - Ingress
    - Egress
  ingress:
    - action: Allow
      metadata:
        annotations:
          from: frontend
          to: database
      protocol: TCP
      source:
        selector: role == 'frontend'
      destination:
        ports:
          - 6379
  egress:
    - action: Allow
```

Names: lowercase alphanumeric with `-` and at most one `.`; namespace defaults to `default`.

Key spec fields: `tier` (must exist before the policy is created), `order` (lowest value applied first within the tier), `selector`, `types`, `ingress`, `egress`, `serviceAccountSelector` (select by name with the `projectcalico.org/name` label) and `performanceHints`.

**`types` default** when omitted:

| Ingress rules | Egress rules | types |
|---|---|---|
| none | none | `Ingress` |
| yes | none | `Ingress` |
| none | yes | `Egress` |
| yes | yes | `Ingress, Egress` |

Leave out `ingress` or `egress` when empty, since an empty list such as `ingress: []` can count as rules present.

**Performance hint.** Normally Calico computes a policy's rules and selectors only on nodes where its selector matches a local endpoint. `AssumeNeededOnEveryNode` treats the policy as in use on every node, preloading it for large policy sets that apply to nearly all endpoints and avoiding teardown work when the last endpoint drains. Hints never change enforcement.

Application layer match criteria are ingress-only and must be enabled first.

## Checked

2026-11-08. The Network policy resource page was read in full. Sample YAML, field descriptions, the types table and the hint were confirmed on the Network policy resource page.

Method: documentation only; no commands were run.
