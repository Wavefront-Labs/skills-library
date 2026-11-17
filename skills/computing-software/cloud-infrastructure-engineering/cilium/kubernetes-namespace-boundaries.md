---
id: computing-software.cloud-infrastructure-engineering.cilium.kubernetes-namespace-boundaries
name: kubernetes-namespace-boundaries
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, namespaces, ciliumnetworkpolicy, networkpolicy, namespace-isolation, endpointselector]
level: practitioner
status: docs-checked
description: "How Cilium policies scope to Kubernetes namespaces, cross-namespace access via fromEndpoints, and why endpointSelector cannot name a namespace."
sources:
  - https://docs.cilium.io/en/stable/security/policy/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Namespaces in Cilium policy

- A `CiliumNetworkPolicy` or `NetworkPolicy` applies only to pods in its own namespace. Grant access to or from other namespaces with `fromEndpoints` or `toEndpoints` selecting the label `k8s:io.kubernetes.pod.namespace`.
- Kubernetes prohibits naming a namespace in `endpointSelector`; it always applies to the policy namespace.
- Policies imported directly through the API apply to all namespaces unless a namespace selector is specified.

## Examples in the page
- Isolate namespaces `ns1` and `ns2`: default-deny ingress for all pods and allow only from pods in the same namespace. This locks down ingress only; pods can still egress anywhere except to ns1/ns2 where source and destination must share a namespace. Add egress rules to enforce boundaries at egress.
- Expose pods `name=leia` in `ns1` to pods `name=luke` in `ns2`.
- Allow all pods in namespace `public` to reach kube-dns on 53/UDP in `kube-system`.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/kubernetes/. 

Method: documentation only; no commands were run.
