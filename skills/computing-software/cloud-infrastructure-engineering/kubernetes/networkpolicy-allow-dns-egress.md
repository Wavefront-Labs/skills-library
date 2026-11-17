---
id: computing-software.cloud-infrastructure-engineering.kubernetes.networkpolicy-allow-dns-egress
name: networkpolicy-allow-dns-egress
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networkpolicy, allow-dns-egress, default-deny, coredns, egress]
level: practitioner
status: gated
description: "Allow DNS from pods under default-deny egress: selecting kube-dns pods across namespaces, UDP and TCP 53, NodeLocal DNSCache, and verifying resolution."
sources: ["https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allowing DNS egress under default-deny

The first thing that breaks after `policyTypes: [Egress]` default-deny is DNS: every
connection by name fails with lookup timeouts.

## Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-dns, namespace: shop}
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to:
    - namespaceSelector:
        matchLabels: {kubernetes.io/metadata.name: kube-system}
      podSelector:
        matchLabels: {k8s-app: kube-dns}
    ports:
    - {protocol: UDP, port: 53}
    - {protocol: TCP, port: 53}
```
- `namespaceSelector` and `podSelector` in the SAME `to` element: AND (kube-dns pods in
  kube-system). Splitting them into two elements would allow all of kube-system OR any
  kube-dns-labelled pod anywhere.
- TCP 53 is needed for large responses and some resolvers.
- Policies match the pod's port after Service translation, so 53 is right for CoreDNS (which
  listens on 53 in its pod) (gated: unconfirmed, source is paywalled or blocked). The `k8s-app: kube-dns` label is the one in the upstream CoreDNS deployment manifest
  (still used by the Service in kubeadm clusters; confirm on your cluster with `kubectl -n kube-system get pods --show-labels`).

## NodeLocal DNSCache
Pods query a node-local listen address. The Kubernetes docs say it can be any non-colliding address and recommend the
link-local range `169.254.0.0/16`; `169.254.20.10` is the value in the sample manifest (check yours). Allow it as an ipBlock:
```yaml
  - to:
    - ipBlock: {cidr: 169.254.20.10/32}
    ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]
```
Some CNIs treat node-local traffic specially; test (gated: unconfirmed, source is paywalled or blocked).

## Cilium
`CiliumNetworkPolicy` with `toEndpoints` for kube-dns plus `rules.dns: [{matchPattern: "*"}]`
is required for FQDN policies to learn names (the Cilium DNS docs show this pairing with `toEndpoints` on
`k8s:k8s-app: kube-dns`).

## Verify
The policy YAML above passes `kubeconform -strict` (run). The commands below need a cluster and were not run.
```bash
kubectl -n shop run t --rm -it --image=busybox:1.36 --restart=Never -- nslookup kubernetes.default
kubectl -n shop run t --rm -it --image=busybox:1.36 --restart=Never -- nslookup example.com
```
