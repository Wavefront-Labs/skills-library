---
id: computing-software.cloud-infrastructure-engineering.kubernetes.network-policy-security-boundary
name: network-policy-security-boundary
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networkpolicy, default-deny, egress, ingress, dns, coredns, cni, calico, cilium, flannel, podselector, namespaceselector, ipblock, zero-trust, network-segmentation]
level: advanced
status: docs-checked
description: "NetworkPolicy's default-allow-until-selected posture, the default-deny-plus-DNS pattern, CNI enforcement gaps, and where NetworkPolicy stops being a real security boundary."
sources: ["https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://kubernetes.io/docs/concepts/cluster-administration/addons/", "https://github.com/flannel-io/flannel#network-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkPolicy as a security boundary — and where it stops being one

**Goal:** use NetworkPolicy to actually constrain lateral movement, not just
document intended traffic flows that the cluster doesn't enforce. RBAC is a
separate boundary (who can call the API) covered in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`;
NetworkPolicy constrains what already-running pods can reach over the network,
which matters most *after* some other control has already failed (container
compromise, SSRF, a malicious dependency).

## 1. The default is allow-everything, and it's a resource, not a setting
By default a pod is non-isolated for ingress and for egress: all connections are
allowed. A pod becomes isolated for a direction only when some NetworkPolicy both
selects it and lists that direction in `policyTypes`; there is no cluster-wide "default
deny" unless you create one per namespace (the Kubernetes docs list namespace-wide or
cluster-wide default policies as something core NetworkPolicy does not provide; see
`computing-software.cloud-infrastructure-engineering.kubernetes.admin-network-policy-cluster-guardrails`).
Pods selected by zero policies remain fully open. This means adding
your first policy to a namespace is additive-restrictive for the pods it
targets, but does nothing for every pod it doesn't select — a namespace with one
narrow policy and nine unselected deployments is not "mostly protected," it's
nine deployments still fully open.

## 2. The default-deny-plus-DNS pattern (start every namespace here)
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny-all, namespace: shop}
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-dns, namespace: shop}
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to: [{namespaceSelector: {}, podSelector: {matchLabels: {k8s-app: kube-dns}}}]
    ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]
```
The Kubernetes docs warn that a default deny-all egress policy also blocks DNS
traffic, so workloads that need name resolution need a separate policy allowing egress to
the cluster DNS service. The DNS pods carry the label `k8s-app=kube-dns` in the standard
CoreDNS deployment (as used in the Kubernetes DNS debugging docs); confirm the label in your cluster.

## 3. Rules are additive across policies, and selectors only match labels
- The `ingress` lists of all policies that apply to a pod combine additively, and so do the
  `egress` lists; core NetworkPolicy has no explicit deny. If any policy permits the traffic,
  it is permitted, so "lock this down" often requires *editing* an existing broad policy
  rather than *adding* a narrower one next to it.
- `podSelector`/`namespaceSelector` match **labels**, not identity — a pod that gains the
  right labels falls into an allowed selector's scope, so NetworkPolicy is only as strong as who
  can set labels on pods and namespaces; pair with RBAC restricting `patch`/`update` on pods
  in sensitive namespaces.
- A single `from`/`to` entry with both `namespaceSelector` and `podSelector` is an AND (pods
  with that label in matching namespaces); two separate entries are an OR.
- `ipBlock` (CIDR-based rules) references traffic by IP; the docs say it should be used for
  cluster-external IPs because Pod IPs are ephemeral. `except` carves sub-ranges out of the CIDR.
  Traffic to and from the node a pod runs on is always allowed, regardless of IP.

## 4. CNI enforcement is not guaranteed — check, don't assume
`NetworkPolicy` is an API object; **enforcing** it is the network plugin's job. The
Kubernetes docs say your cluster must use a network plugin that supports NetworkPolicy
enforcement; creating a policy on a cluster whose plugin does not enforce it has no effect.
The Flannel README says the `flanneld` binary does not natively enforce Network Policies;
its documented options are the Helm chart's `netpol.enabled` (deploys the Kubernetes SIGs
network policy controller) or a separate policy provider such as Calico (Canal). For managed
Kubernetes services, read your provider's documentation for how policy enforcement is
enabled (it can be a separate setting or add-on).
Deploying a `NetworkPolicy` and never verifying enforcement is the most common
way teams believe they have network segmentation and don't.

## 5. L3/L4 only — the policy ceiling
Standard `NetworkPolicy` works at the IP address or port level (OSI layers 3 and 4) for TCP,
UDP and SCTP. The Kubernetes docs list what it cannot do: anything TLS related (use a service
mesh or ingress controller), targeting Services by name, node-specific policies by Kubernetes
identity, logging of blocked or accepted connections, explicit deny policies, and preventing loopback or
resident-node traffic. "Allow this service to call only one HTTP path on that service" is
therefore not expressible; it needs an L7-aware layer such as a service mesh or a CNI's own
L7 policy. Know which layer you are enforcing at before promising "least privilege".

## Gotchas
- Egress rules by `ipBlock` to an external service stop matching if that service's IP
  range changes; core NetworkPolicy has no hostname-based rule.
- Pods cannot block localhost access or access from their resident node (documented
  limitation), so sidecar-to-container traffic over `127.0.0.1` is not restricted.
- Cluster ingress and egress mechanisms often rewrite source or destination IPs, and the docs say it
  is not defined whether that happens before or after NetworkPolicy processing, so behaviour differs
  by network plugin, cloud provider and Service implementation.
- Testing with `kubectl exec ... -- curl` from inside the cluster only proves what
  that specific source pod can reach — test from a pod with the labels and namespace of the
  client you intend to block.

## Verify
- [ ] Every namespace with sensitive workloads has a `default-deny-all`
      (ingress+egress) policy plus an explicit DNS-egress allow.
- [ ] The running CNI is confirmed to enforce `NetworkPolicy` (not just accept
      the object) — test with a known-should-be-blocked connection, not inference.
- [ ] No policy intended to restrict a pod is defeated by a broader, overlapping
      policy also selecting it (policies are additive/OR'd).
- [ ] Egress rules depending on external-service IPs are reviewed for IP changes.
- [ ] Anyone relying on "this policy enforces API-path-level access" has been
      told that's an L7 claim standard NetworkPolicy cannot make.

## Checked
Checked 2026-10-24 against the kubernetes/website Network Policies page (isolation defaults, additive
lists, AND/OR selector semantics, ipBlock and node traffic, DNS caution, listed limitations, address
rewriting caveat), the Kubernetes DNS debugging page (`k8s-app=kube-dns`) and the Flannel README
(network policy options). Vendor-specific enablement details were removed rather than kept unchecked.
Method: documentation only; no commands were run.
