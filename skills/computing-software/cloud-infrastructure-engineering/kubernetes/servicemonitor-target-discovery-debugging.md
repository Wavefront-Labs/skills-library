---
id: computing-software.cloud-infrastructure-engineering.kubernetes.servicemonitor-target-discovery-debugging
name: servicemonitor-target-discovery-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, prometheus-operator, target-discovery, servicemonitor, podmonitor, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug ServiceMonitors and PodMonitors whose targets never appear in Prometheus: selectors, namespace selectors, port names, RBAC and the generated config."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/developer/getting-started/", "https://prometheus-operator.dev/docs/api-reference/api/", "https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml", "https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/", "https://github.com/prometheus-operator/kube-prometheus/blob/main/docs/customizations/monitoring-additional-namespaces.md", "https://prometheus.io/docs/prometheus/latest/getting_started/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ServiceMonitor targets never appear

Work down this chain; it breaks at exactly one link.

## 1. Does Prometheus select the ServiceMonitor?
```bash
kubectl get prometheus -A -o jsonpath='{range .items[*]}{.metadata.name}: sel={.spec.serviceMonitorSelector} nssel={.spec.serviceMonitorNamespaceSelector}{"\n"}{end}'
```
In the Prometheus resource an empty `serviceMonitorSelector` matches all ServiceMonitors and a null one
matches none; for `serviceMonitorNamespaceSelector` an empty selector matches all namespaces and null (the
default) matches only the Prometheus's own namespace. With kube-prometheus-stack's default
`prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues: true` the chart builds the selector from
the Helm release values, so label the ServiceMonitor to match what the command above prints, or set
`serviceMonitorSelectorNilUsesHelmValues=false` to select everything.

## 2. Does the ServiceMonitor select the Service?
`spec.selector` matches **Service** labels (not pod labels) and `namespaceSelector` must include
the Service's namespace.
```bash
kubectl get svc -n shop -l app=web
```

## 3. Does the endpoint port match?
`endpoints[].port` is the name of the Service port (`.spec.ports[].name`) and takes precedence over
`targetPort`, which is a container port name or number on the selected Pods. An unnamed Service port
cannot be matched by name.

## 4. Does the Service have endpoints?
`kubectl get endpointslices -n shop -l kubernetes.io/service-name=web`

## 5. Can Prometheus list them?
Prometheus must be allowed to discover targets in the Service's namespace: kube-prometheus grants this per
namespace with a Role and RoleBinding (by default only `default`, `kube-system` and its own namespace).

## 6. What config was generated?
```bash
kubectl -n monitoring get secret prometheus-<name> -o jsonpath='{.data.prometheus\.yaml\.gz}' | base64 -d | gunzip | grep -n 'web'
kubectl -n monitoring logs deploy/prometheus-operator | grep -i -E 'web|error'
```
The operator stores the generated configuration in the `prometheus-<name>` Secret under `prometheus.yaml.gz`.

## Verify
Status > Target health (`/targets`) lists the `web` endpoints with state UP.

## Checked
2026-10-28. Confirmed: selector semantics (`serviceMonitorSelector`, `serviceMonitorNamespaceSelector`)
and the `endpoints[].port` / `targetPort` fields against the Prometheus Operator API reference; the
`prometheus-<name>` Secret and `prometheus.yaml.gz` key against the troubleshooting page and API reference;
`serviceMonitorSelectorNilUsesHelmValues` against the chart README and `values.yaml`; the
`kubernetes.io/service-name` EndpointSlice label against the Kubernetes docs; the per-namespace Role and
RoleBinding against the kube-prometheus page; Target health against the Prometheus getting-started page.
Removed: the exact `get/list/watch` verb list, the `forbidden` log hint, the Service Discovery UI remark and
the generated job name `serviceMonitor/shop/web/0` (not on the pages read).
Method: documentation only; no commands were run.
