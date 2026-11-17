---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-discovery-kubernetes-and-relabeling
name: alloy-discovery-kubernetes-and-relabeling
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [discovery-relabel, alloy, discovery.kubernetes, discovery.relabel, kubernetes-pod-labels, relabel-rules]
level: practitioner
status: docs-checked
description: "Discover Kubernetes pods in Alloy and relabel targets into clean labels for logs and metrics."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/discovery/discovery.kubernetes/", "https://grafana.com/docs/alloy/latest/reference/components/discovery/discovery.relabel/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: collect pod logs or metrics with consistent labels and without needless API load.

```
discovery.kubernetes "pods" {
  role = "pod"

  namespaces {
    names = ["payments"]
  }
}

discovery.relabel "pods" {
  targets = discovery.kubernetes.pods.targets

  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    target_label  = "namespace"
    action        = "replace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    target_label  = "pod"
    action        = "replace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_label_app_kubernetes_io_name"]
    target_label  = "app"
    action        = "replace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_container_name"]
    target_label  = "container"
    action        = "replace"
  }
}
```
Pass `discovery.relabel.pods.output` as the `targets` of a downstream scrape or log source component.

How it works
- `role` is one of `node`, `pod`, `service`, `endpoints`, `endpointslice` or `ingress`. The `pod` role discovers all Pods and creates one target per declared container port, or a port-free target per container if none is declared. For port-free targets you must inject a port with `discovery.relabel` before collecting metrics.
- Pod targets carry `__meta_kubernetes_*` labels, including `namespace`, `pod_name`, `pod_container_name`, `pod_node_name`, `pod_uid`, `pod_label_<labelname>` and `pod_annotation_<annotationname>`.
- `discovery.relabel` applies its `rule` blocks to each target in order. With no rules the targets pass through unchanged. Labels starting with `__` are internal and may be removed by other components before telemetry collection, so copy what you need to a normal label (or use a `labelmap` action to strip the prefix). Use the `__tmp` prefix for temporary labels.
- A `keep` rule with `source_labels` and `regex` filters targets, as in the docs example that keeps only targets whose `app` label is `backend`.

Performance
- By default discovery covers all namespaces. In DaemonSet deployments every Alloy Pod then watches the whole cluster, which can raise API server load and memory use and cause throttling on managed Kubernetes services.
- Limit it with the `namespaces` block, `selectors` (label or field selectors), `discovery.kubelet` for node-local Pods, or clustering for larger deployments.
- `attach_metadata` can attach node or namespace metadata, but needs permission to list and watch Nodes or Namespaces.

## Verify
In the Alloy UI, the `discovery.relabel.pods` component page shows its exports; targets should carry the new labels.

## Checked
Method: docs-checked 2026-11-09 against the Alloy docs discovery.kubernetes and discovery.relabel reference pages (raw markdown, read in full except generated sections). Removed unconfirmed RBAC, loki.source.kubernetes and drop-rule claims.
