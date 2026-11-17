---
id: computing-software.cloud-infrastructure-engineering.kubernetes.networkpolicy-and-or-selector-semantics
name: networkpolicy-and-or-selector-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networkpolicy, netpol-and-or, podselector, namespaceselector, ipblock]
level: practitioner
status: gated
description: "Get NetworkPolicy selector logic right: AND within one peer element, OR across elements and rules, ports applying per rule, and the YAML dash that changes meaning."
sources: ["https://kubernetes.io/docs/concepts/services-networking/network-policies/#behavior-of-to-and-from-selectors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkPolicy AND vs OR

## One peer element, two selectors = AND
```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels: {team: payments}
    podSelector:
      matchLabels: {role: client}
```
Allows pods labelled `role=client` IN namespaces labelled `team=payments`.

## Two peer elements = OR
```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels: {team: payments}
  - podSelector:
      matchLabels: {role: client}
```
Allows ALL pods in `team=payments` namespaces, OR `role=client` pods in the policy's OWN
namespace (a lone podSelector is namespace-local). The only difference is the `-` before
`podSelector`. This is the most common NetworkPolicy bug and a favourite exam trap.

## Rules and ports
```yaml
ingress:
- from: [{podSelector: {matchLabels: {app: web}}}]
  ports: [{port: 8080, protocol: TCP}]
- from: [{podSelector: {matchLabels: {app: prometheus}}}]
  ports: [{port: 9090, protocol: TCP}]
```
Each rule is `(from) AND (ports)`; rules are ORed. Empty `from` with ports = any source on those
ports. Omitted `ports` = all ports.

## Policies combine additively
Multiple policies selecting the same pod are unioned; there is no deny rule in the core API
(the sig-network Network Policy API adds Deny and Pass actions through cluster-scoped policy; its current docs call the
resource `ClusterNetworkPolicy`, formerly `AdminNetworkPolicy`, so check the kind your cluster serves).

## ipBlock
`ipBlock` with `except` is its own peer. The Kubernetes docs say it should hold cluster-external IPs, because Pod IPs
are ephemeral, and that source/destination IP rewriting makes the order relative to NetworkPolicy undefined.
Use selectors for in-cluster peers.

## Verify
```bash
kubectl describe networkpolicy <name>     # the upstream docs say to use describe when in doubt about how a policy was read
```
The AND and OR examples above are the ones in the Kubernetes NetworkPolicy docs (single `from` element = AND, two
elements = OR with the lone `podSelector` limited to the policy's namespace). Cluster commands were not run (gated: unconfirmed, source is paywalled or blocked).
Then test both an allowed and a denied source pod with `curl -m 3`.
