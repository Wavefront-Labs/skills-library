---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-discovery-kubernetes-relabel
name: grafana-alloy-discovery-kubernetes-relabel
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [discoverykubernetes, kubernetes-roles, attach-metadata, discoveryrelabel-rules, prometheusrelabel, relabel-cache]
level: practitioner
status: docs-checked
description: "Use discovery.kubernetes roles, __meta_kubernetes labels, namespaces and selectors, then reshape with discovery.relabel and prometheus.relabel including its cache modes."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/discovery/discovery.kubernetes.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/discovery/discovery.relabel.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/prometheus/prometheus.relabel.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes discovery and relabeling

`discovery.kubernetes` needs `role`: `node`, `pod`, `service`, `endpoints`, `endpointslice` or `ingress`. With no connection arguments it uses in-cluster config; override with `kubeconfig_file` or `api_server`. Use at most one of `bearer_token`, `bearer_token_file`, `basic_auth`, `authorization` or `oauth2`.

## Cost control
By default every namespace is watched, and in a DaemonSet every pod watches the whole cluster, which can throttle the API server. Add a `namespaces` block (`names`, `own_namespace`), `selectors` (`role`, `label`, `field`), use `discovery.kubelet` for node-local pods, or enable clustering. `attach_metadata` adds `node` or `namespace` metadata.

## Labels
Targets carry `__meta_kubernetes_*` labels, such as `__meta_kubernetes_namespace`, `__meta_kubernetes_pod_name` and `__meta_kubernetes_pod_label_<name>`.

## discovery.relabel
```alloy
discovery.relabel "keep_backend" {
  targets = discovery.kubernetes.pods.targets
  rule {
    source_labels = ["__meta_kubernetes_pod_label_app"]
    action        = "keep"
    regex         = "backend"
  }
}
```
Rules run in order. Labels beginning `__` are internal and may be removed before collection unless you `labelmap` them; use a `__tmp` prefix for scratch labels. Exports: `output` and `rules`.

## prometheus.relabel
Same `rule` block but on metric series. `max_cache_size` defaults to 100000 (LRU); alternatively set `max_cache_size = 0` and `cache_ttl` (minimum 1m) for TTL mode. Exactly one must be non-zero; prefer TTL when cardinality is unknown.

## Checked

2026-11-04. Confirmed against discovery.kubernetes, discovery.relabel and prometheus.relabel reference pages: roles, at-most-one auth rule, DaemonSet load caution, namespaces, selectors, attach_metadata, __meta labels, __tmp prefix, exports, LRU and TTL cache modes. Fixed: internal labels are 'may be removed', not always dropped. Removed the unconfirmed claim about pod ports.

Method: documentation only; no commands were run.
