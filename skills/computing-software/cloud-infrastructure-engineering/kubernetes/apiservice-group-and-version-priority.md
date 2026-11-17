---
id: computing-software.cloud-infrastructure-engineering.kubernetes.apiservice-group-and-version-priority
name: apiservice-group-and-version-priority
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, aggregation-layer, grouppriorityminimum, versionpriority, apiservice, api-discovery]
level: practitioner
status: docs-checked
description: "Set APIService groupPriorityMinimum and versionPriority correctly, understand how they order discovery and which version kubectl prefers, and avoid shadowing core groups."
sources: ["https://kubernetes.io/docs/reference/kubernetes-api/apiregistration/api-service-v1/", "https://kubernetes.io/docs/tasks/extend-kubernetes/setup-extension-api-server/", "https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/", "https://github.com/kubernetes-sigs/metrics-server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APIService groupPriorityMinimum and versionPriority

```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata: {name: v1beta1.metrics.k8s.io}
spec:
  group: metrics.k8s.io
  version: v1beta1
  groupPriorityMinimum: 100
  versionPriority: 100
  service: {name: metrics-server, namespace: kube-system, port: 443}
  insecureSkipTLSVerify: false
  caBundle: <base64-encoded PEM CA bundle>
```
metrics-server's own manifest uses `groupPriorityMinimum: 100` and `versionPriority: 100`.

## What they control
- `groupPriorityMinimum`: the minimum priority of the group; higher priority means clients
  prefer the group over lower ones. Groups sort highest number first, then alphabetically by
  object name. Another version of the same group can set a higher value and raise the whole
  group, so keep the value consistent across a group's APIServices. The API reference recommends
  about 18000 for `*.k8s.io` groups and the 2000s for PaaS groups; small add-ons such as
  metrics-server use 100.
- `versionPriority`: ordering of versions within the group, highest first; it must be greater
  than zero. On equal priority, Kubernetes-style version strings sort GA > beta > alpha, then by
  major and minor number.

## Name collisions
Extension groups can serve resource names that also exist in core (metrics.k8s.io serves `nodes`
and `pods`). Keep extension group priorities low and refer to extension resources with the full
name (`kubectl get nodes.metrics.k8s.io`).

## Upgrading versions
When adding `v1` beside `v1beta1`, give `v1` the higher `versionPriority` so it sorts first;
keep `v1beta1` served until clients migrate.

## Verify
```bash
kubectl get --raw /apis | jq -r '.groups[] | "\(.name) preferred=\(.preferredVersion.version)"' | grep metrics
kubectl api-resources | grep -w nodes
```
The preferred version is the intended one, and `nodes` resolves to the core group first.

## Checked
2026-10-27 against the APIService v1 API reference and the aggregation layer and resource
metrics pipeline pages (kubernetes/website main, v1.38 development tree; v1.37 is the latest
release) and metrics-server's `manifests/base/apiservice.yaml`. Confirmed: field names, the sort
rules and recommended values for `groupPriorityMinimum`, the `versionPriority` rules and
kube-like version ordering, metrics-server's priorities of 100, and the metrics API `nodes` and
`pods` paths. Corrected the invented "17000-18000+ / 100-1000" ranges and removed an unchecked
claim that a high-priority extension group overrides `kubectl get nodes`.
Method: documentation only; no commands were run.
