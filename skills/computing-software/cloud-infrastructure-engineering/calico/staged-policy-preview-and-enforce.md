---
id: computing-software.cloud-infrastructure-engineering.calico.staged-policy-preview-and-enforce
name: staged-policy-preview-and-enforce
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [network-policy, staged, stagednetworkpolicy, stagedglobalnetworkpolicy, whisker, preview, policies-pending]
level: practitioner
status: docs-checked
description: "Test a policy without enforcing it with Staged resources: the staged kinds, a sample, previewing via policies.pending, then enforcing."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/staged-network-policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Staged policies behave as if enforced for the purpose of evaluation but change no actual traffic. They have the same structure as their enforced counterparts:

| Enforced | Staged |
|---|---|
| `NetworkPolicy` (Calico) | `StagedNetworkPolicy` (the page also names `StagedCalicoNetworkPolicy`) |
| `GlobalNetworkPolicy` | `StagedGlobalNetworkPolicy` |
| Kubernetes `NetworkPolicy` | `StagedKubernetesNetworkPolicy` |

Apply them with `kubectl`. A best practice is to stage before enforcing, to avoid unintentionally exposing or blocking traffic. Example:

```yaml
apiVersion: projectcalico.org/v3
kind: StagedGlobalNetworkPolicy
metadata:
  name: default.allow-tcp-6379
spec:
  tier: default
  selector: role == 'database'
  types:
    - Ingress
    - Egress
  ingress:
    - action: Allow
      protocol: TCP
      source:
        selector: role == 'frontend'
      destination:
        ports:
          - 6379
  egress:
    - action: Allow
```

`StagedNetworkPolicy` adds `namespace`. `StagedKubernetesNetworkPolicy` uses Kubernetes fields (`podSelector`, `policyTypes`, `from` with `ipBlock`, `namespaceSelector`, `podSelector`, and `ports`).

**Preview.** The effect shows in the `policies.pending` field of the flow logs in the Calico Whisker web console: it says what would happen to the traffic if the staged policy were enforced.

**Enforce.** When the result is satisfactory, create an identical policy (the enforced kind) and apply it. RBAC for staged resources is configured like tiered policy.

Pair this with the global default deny recipe: stage the deny, add allows, then enforce.

## Checked

Read in full on 2026-11-08: the Stage, preview impacts, and enforce policy page. The resource-name mapping, the staged YAML, the policies.pending field and the enforcement step match it.

Method: documentation only; no commands were run.
