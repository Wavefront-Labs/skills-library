---
id: computing-software.cloud-infrastructure-engineering.kubernetes.admin-network-policy-cluster-guardrails
name: admin-network-policy-cluster-guardrails
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, adminnetworkpolicy, baselineadminnetworkpolicy, network-policy, sig-network, multi-tenancy, cluster-network-policy]
level: practitioner
status: docs-checked
description: "Use AdminNetworkPolicy and BaselineAdminNetworkPolicy for cluster-admin guardrails that tenants cannot override: priority, Allow/Deny/Pass, evaluation order, CNI support."
sources: ["https://network-policy-api.sigs.k8s.io/", "https://network-policy-api.sigs.k8s.io/api-overview/", "https://network-policy-api.sigs.k8s.io/implementations/", "https://github.com/kubernetes-sigs/network-policy-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AdminNetworkPolicy and BaselineAdminNetworkPolicy

## Problem they solve
Namespaced NetworkPolicy is owned by tenants and is allow-only; the Kubernetes docs list
default policies applied to all namespaces or pods and explicit deny as things core NetworkPolicy
does not provide. Admins need rules tenants cannot undo ("nobody reaches the metadata API",
"monitoring can always scrape") and cluster defaults tenants *can* override ("deny
cross-namespace by default").

## API status
SIG Network's Network Policy API project defines `AdminNetworkPolicy` and
`BaselineAdminNetworkPolicy` in group `policy.networking.k8s.io`, version `v1alpha1`, installed as
CRDs from the kubernetes-sigs/network-policy-api repository (not part of core Kubernetes). The
repository also contains a `v1alpha2` `ClusterNetworkPolicy` with `tier` (`Admin` or `Baseline`),
`priority` (0 to 1000) and actions `Accept`, `Deny`, `Pass`. Implementation status is tracked on the
project's implementations page: for the v1alpha1 resources it lists kube-network-policies,
OVN-Kubernetes, Antrea, Kube-OVN and Calico, with Cilium as a tracking issue only; for
ClusterNetworkPolicy it lists kube-network-policies, Kube-OVN (experimental) and Calico (standard
support in v3.32, as of that page's April 2026 update). Check which version your CNI ships.

## Evaluation order
1. **AdminNetworkPolicy** (ANP), by `priority` 0 to 1000, **lower number = higher precedence**.
   Actions: `Allow`, `Deny`, `Pass`. `Pass` skips the remaining ANP rules and hands the traffic to
   NetworkPolicy. All ANP rules take precedence over NetworkPolicy and BaselineAdminNetworkPolicy.
2. Namespaced **NetworkPolicy**.
3. **BaselineAdminNetworkPolicy** (BANP), a singleton that must be named `default`
   (enforced by a validation rule). Actions: `Allow`, `Deny`.

## Examples
Always allow monitoring to scrape, cannot be blocked by tenants:
```yaml
apiVersion: policy.networking.k8s.io/v1alpha1
kind: AdminNetworkPolicy
metadata: {name: allow-monitoring}
spec:
  priority: 10
  subject: {namespaces: {}}
  ingress:
  - name: prometheus
    action: Allow
    from: [{namespaces: {matchLabels: {kubernetes.io/metadata.name: monitoring}}}]
```
Default isolation between tenant namespaces that tenants may open up with their own NPs:
```yaml
apiVersion: policy.networking.k8s.io/v1alpha1
kind: BaselineAdminNetworkPolicy
metadata: {name: default}
spec:
  subject: {namespaces: {matchLabels: {tenant: "true"}}}
  ingress:
  - name: deny-other-namespaces
    action: Deny
    from: [{namespaces: {matchExpressions: [{key: tenant, operator: Exists}]}}]
```
Egress to a CIDR uses the `networks` peer, for example `to: [{networks: ["169.254.169.254/32"]}]`
with `action: Deny`. The API's own comments say `networks` can hold up to 25 CIDRs and that a rule
using it will also match pod traffic unless an earlier rule passes pod traffic; some implementations
list `networks` support as experimental, so check your CNI.

## Design rules
- If two or more ANPs with the same priority could match a connection, the API says the implementation
  may apply any of them and you cannot rely on which; use unique priority values (leave gaps such as
  10, 20, 30 for later inserts).
- Use `Pass` to delegate traffic to namespace owners rather than `Allow`.
- Name every rule (each rule has a `name` field).

## Verify
```bash
kubectl get adminnetworkpolicies,baselineadminnetworkpolicies
```
Test from a tenant namespace with a NetworkPolicy that tries to deny monitoring; scraping must still
succeed.

## Checked
Checked 2026-10-24 against the kubernetes-sigs/network-policy-api repository (main): `apis/v1alpha1`
types (group `policy.networking.k8s.io`, priority 0 to 1000, lower wins, same-priority ambiguity,
actions, `networks` limits, BANP name `default`), `apis/v1alpha2` ClusterNetworkPolicy (tiers, actions)
and `site-src/implementations.md` (implementations, as updated 21 April 2026), plus the Kubernetes
Network Policies page (listed limitations of core NetworkPolicy).
Method: documentation only; no commands were run.
