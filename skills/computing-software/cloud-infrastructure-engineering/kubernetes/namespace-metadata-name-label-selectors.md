---
id: computing-software.cloud-infrastructure-engineering.kubernetes.namespace-metadata-name-label-selectors
name: namespace-metadata-name-label-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespaces, metadata-name-label, namespaceselector, network-policy, admission-webhooks]
level: practitioner
status: docs-checked
description: "Use the automatic kubernetes.io/metadata.name namespace label to select namespaces by name in NetworkPolicies, webhooks and affinity rules."
sources: ["https://kubernetes.io/docs/reference/labels-annotations-taints/#kubernetes-io-metadata-name", "https://kubernetes.io/docs/concepts/services-networking/network-policies/#targeting-a-namespace-by-its-name", "https://github.com/kubernetes/kubernetes/blob/release-1.37/staging/src/k8s.io/api/core/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubernetes.io/metadata.name

The API server sets `kubernetes.io/metadata.name=<name>` on every namespace, and you can't
change its value, so it is safe to select on, unlike user labels a tenant could add.

## NetworkPolicy: allow from one namespace by name
```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels: {kubernetes.io/metadata.name: monitoring}
    podSelector:
      matchLabels: {app.kubernetes.io/name: prometheus}
```
Put both selectors in one `from` element for AND; separate elements mean OR.

## Webhooks: skip system namespaces
```yaml
namespaceSelector:
  matchExpressions:
  - key: kubernetes.io/metadata.name
    operator: NotIn
    values: [kube-system, kube-node-lease, cert-manager]
```

## Pod affinity across named namespaces
```yaml
podAffinityTerm:
  namespaceSelector:
    matchLabels: {kubernetes.io/metadata.name: cache}
  labelSelector: {matchLabels: {app: redis}}
  topologyKey: kubernetes.io/hostname
```

## Why not custom labels
A tenant with `patch namespaces` rights could label their namespace `team=monitoring` and gain
access. The name label is set by the apiserver.

## Verify
```bash
kubectl get ns --show-labels | grep metadata.name
kubectl get ns -l kubernetes.io/metadata.name=monitoring
```

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37): well-known labels (`kubernetes.io/metadata.name` set by the API server on all
namespaces, value cannot be changed), Network Policies (targeting a namespace by its name;
one `from` element with both selectors versus two elements) and the core/v1
`PodAffinityTerm.namespaceSelector` field in kubernetes/kubernetes release-1.37. Removed the
unconfirmed "since 1.22" version claim.

Method: documentation only; no commands were run.
