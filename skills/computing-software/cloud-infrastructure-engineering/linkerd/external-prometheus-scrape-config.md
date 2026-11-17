---
id: computing-software.cloud-infrastructure-engineering.linkerd.external-prometheus-scrape-config
name: external-prometheus-scrape-config
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, prometheus, metrics, viz, scrape]
level: advanced
status: docs-checked
description: "Point an external Prometheus at the control plane and proxies with linkerd scrape jobs and configure Viz to use it."
sources:
  - https://linkerd.io/2.19/tasks/external-prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Viz ships its own Prometheus, but you can use an external one. Two things are required: scrape configuration on that Prometheus for both control plane and proxy metrics, and Viz configured to read from it.

The scrape config is a subset of the full `linkerd-prometheus` configuration. Replace the templated values (namespaces and so on) with real ones before applying. Jobs include:

- `linkerd-controller`: `kubernetes_sd_configs` with `role: pod` over the control plane namespaces, keeping targets whose container port name matches `admin-http`, and setting the `component` label from the container name
- `linkerd-service-mirror`: pods whose `component` label and port name match `linkerd-service-mirror;admin-http$`
- `linkerd-proxy`: the data plane proxies

```yaml
- job_name: 'linkerd-controller'
  kubernetes_sd_configs:
    - role: pod
  relabel_configs:
    - source_labels:
        - __meta_kubernetes_pod_container_port_name
      action: keep
      regex: admin-http
    - source_labels: [__meta_kubernetes_pod_container_name]
      action: replace
      target_label: component
```

The second half of the guide configures Viz to use the external Prometheus; follow its exact values.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/external-prometheus/.

Removed or reworded: Claim that components consume the labels.

Method: documentation only; no commands were run.
