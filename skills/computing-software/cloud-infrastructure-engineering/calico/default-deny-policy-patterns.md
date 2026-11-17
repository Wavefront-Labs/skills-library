---
id: computing-software.cloud-infrastructure-engineering.calico.default-deny-policy-patterns
name: default-deny-policy-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [network-policy, default-deny, globalnetworkpolicy, namespaceselector, kube-dns, staging, best-practice]
level: practitioner
status: docs-checked
description: "Apply default deny safely: namespaced deny for Calico or Kubernetes policy, and a global deny for non-system namespaces with a DNS allow."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/get-started/kubernetes-default-deny
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubernetes pods are default allow. Calico follows the convention: with no policy selecting a pod, all traffic is allowed; once a policy of type Ingress (or Egress) selects it, only traffic that policy allows is permitted for that direction. Other endpoints (VMs, host interfaces) default to deny, even with no policy.

**Namespaced default deny**, Calico form:

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: engineering
spec:
  selector: all()
  types:
    - Ingress
    - Egress
```

The Kubernetes equivalent uses `podSelector: {}` with `policyTypes: [Ingress, Egress]` under `networking.k8s.io/v1`.

**Global default deny: two best practices.**

1. Allow, stage, then deny: stage the global deny first (it shows what would be blocked), add allow policies until nothing legitimate is denied, then enforce.
2. Keep it to non-system pods. A cluster-wide deny also hits control plane and Calico components.

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-app-policy
spec:
  namespaceSelector: kubernetes.io/metadata.name not in {"calico-system", "kube-public", "kube-system", "tigera-operator"}
  types:
  - Ingress
  - Egress
  egress:
  - action: Allow
    protocol: UDP
    destination:
      selector: 'k8s-app == "kube-dns"'
      ports:
      - 53
  - action: Allow
    protocol: TCP
    destination:
      selector: 'k8s-app == "kube-dns"'
      ports:
      - 53
```

It denies by selecting traffic without allowing it. The DNS rules avoid repeating them per pod. Adjust the excluded namespaces to what you have installed.

The page warns against `selector: all()` in the default tier with both types: too broad, can break the cluster.

## Checked

Read in full on 2026-11-08: the Enable a default deny policy for Kubernetes pods page. Default behaviour, both namespaced examples, the global example, the two best practices and the "Don't try this" warning match it.

Method: documentation only; no commands were run.
