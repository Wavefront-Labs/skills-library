---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tenant-network-isolation-patterns
name: tenant-network-isolation-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-tenancy-isolation, tenant-network-isolation, network-policy, adminnetworkpolicy, default-deny]
level: practitioner
status: docs-checked
description: "Isolate tenant namespaces on the network with default-deny, intra-tenant allow rules, cluster-wide admin baselines and controlled access to shared services."
sources: ["https://kubernetes.io/docs/concepts/security/multi-tenancy/", "https://github.com/kubernetes-sigs/network-policy-api", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tenant network isolation

## Baseline per tenant namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: tenant-isolation, namespace: tenant-a}
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
  ingress:
  - from:
    - namespaceSelector: {matchLabels: {tenant: a}}     # all namespaces of the same tenant
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: ingress-nginx}}
  egress:
  - to:
    - namespaceSelector: {matchLabels: {tenant: a}}
  - to:
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: kube-system}}
      podSelector: {matchLabels: {k8s-app: kube-dns}}
    ports: [{port: 53, protocol: UDP}, {port: 53, protocol: TCP}]
```
Tenants could delete or loosen namespaced policies if RBAC allows; deny them write access to
NetworkPolicy, or enforce at cluster level.

## Cluster-level enforcement
ClusterNetworkPolicy (API group `policy.networking.k8s.io`, where the CNI supports it) in the `Admin`
tier is evaluated before namespaced NetworkPolicies, so tenants cannot override it (an Admin-tier
`Pass` rule can deliberately delegate a decision). In v1alpha2 it replaced the v1alpha1
AdminNetworkPolicy and BaselineAdminNetworkPolicy kinds; the tier is now a field:
```yaml
apiVersion: policy.networking.k8s.io/v1alpha2
kind: ClusterNetworkPolicy
metadata: {name: tenant-a-deny-others}
spec:
  tier: Admin
  priority: 10
  subject: {namespaces: {matchLabels: {tenant: a}}}
  ingress:
  - name: deny-other-tenants
    action: Deny
    from: [{namespaces: {matchExpressions: [{key: tenant, operator: NotIn, values: [a]}, {key: tenant, operator: Exists}]}}]
```
Alternatives: Cilium `CiliumClusterwideNetworkPolicy`, Calico `GlobalNetworkPolicy`.

## Shared services
Monitoring, ingress, DNS and logging must be reachable; list them explicitly. Shared ingress
controllers can route any host to any backend; restrict which Ingresses tenants can create
(admission policy on hosts) or give each tenant its own Gateway.

## Verify
From a tenant-a pod, reaching a tenant-b Service times out; DNS and the tenant's own services work.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026; network-policy-api (main)
- Corrected the cluster-level example: the network-policy-api project replaced `AdminNetworkPolicy` and `BaselineAdminNetworkPolicy` (v1alpha1) with `ClusterNetworkPolicy` in v1alpha2, where `tier: Admin|Baseline` sets evaluation order; confirmed actions `Accept`, `Deny` and `Pass`, lower `priority` numbers taking precedence, and the example shape from the project's user-story YAML.
- Confirmed NetworkPolicy semantics, `ipBlock` guidance and Cilium `CiliumClusterwideNetworkPolicy` and Calico `GlobalNetworkPolicy` as cluster-wide alternatives in their docs. The `matchExpressions` selector inside `namespaces` follows the label-selector form used in the project's example.

Method: documentation only; no commands were run.
