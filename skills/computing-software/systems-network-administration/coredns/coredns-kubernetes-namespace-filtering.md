---
id: computing-software.systems-network-administration.coredns.coredns-kubernetes-namespace-filtering
name: coredns-kubernetes-namespace-filtering
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, kubernetes, namespaces, labels, filtering]
level: practitioner
status: docs-checked
description: "Limit which namespaces and objects the kubernetes plugin exposes using namespaces, namespace_labels and labels selectors."
sources:
  - https://coredns.io/plugins/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose only a subset of the cluster in DNS.

- `namespaces NAMESPACE...`: only these namespaces are exposed. If omitted, all are.
- `namespace_labels EXPRESSION`: expose only namespaces matching a label selector. the docs example exposes only namespaces labelled `istio-injection=enabled`.
- `labels EXPRESSION`: expose only Kubernetes objects matching the selector. The docs example exposes objects labelled `application=nginx` in the staging or qa environments:

`labels environment in (staging, qa),application=nginx`

The selector syntax is the one described in the Kubernetes documentation on labels and selectors.

Example for two namespaces:

```
kubernetes cluster.local {
    namespaces test staging
}
```

The `fallthrough` option passes an NXDOMAIN result on to later plugins in the chain:

```
kubernetes cluster.local {
    fallthrough in-addr.arpa ip6.arpa
}
```

Only queries for the listed zones then fall through; others return NXDOMAIN. If ZONES is omitted for fallthrough, it applies to every zone the plugin is authoritative for.

Both selector options use the Kubernetes label selector syntax. Objects and namespaces that do not match are not exposed.

## Checked

2026-11-08. Read the kubernetes plugin README in full. Removed an unsupported claim about shrinking the watch set and reworded the fallthrough text; noted the README's own namespace_labels example is written as labels.

Method: documentation only; no commands were run.
