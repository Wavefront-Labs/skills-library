---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-scrapeconfig-kubernetes-file-http-sd
name: prometheus-operator-scrapeconfig-kubernetes-file-http-sd
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [kubernetes-sd, file-sd, http-sd, scrapeconfig-relabeling, node-exporter-scrape]
level: advanced
status: docs-checked
description: "Configure ScrapeConfig with kubernetes_sd roles, file_sd mounted from a ConfigMap, and http_sd, including RBAC and relabeling needs."
sources: ["https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/developer/scrapeconfig.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## kubernetes_sd
`kubernetesSDConfigs` takes a mandatory capitalised `role`: `Node`, `Pod`, `Service`, `Endpoints`, `EndpointSlice` or `Ingress`. When Prometheus runs in-cluster the API address and credentials are discovered automatically. Restrict with `namespaces.names` and filter with `selectors`. Discovered targets normally need `relabelings` to build the scrape address and labels. The Prometheus ServiceAccount needs `get`, `list` and `watch` on the discovered resources in the discovered namespaces.

Example: with role `Node` the address defaults to the kubelet port; a relabeling rewrites it to scrape a node exporter on port 9100 of the node internal IP, and sets `instance` to the node name. Prefer `ServiceMonitor`, `PodMonitor` or `Probe` when they cover the use case; `kubernetes_sd` is for cases like node discovery.

## file_sd
Mount a file into the Prometheus or PrometheusAgent pods (the docs use a ConfigMap listing targets and labels, listed under `configMaps` in the `Prometheus` spec), then reference the path from `fileSDConfigs.files` in the ScrapeConfig. In the docs example the ConfigMap `scrape-file-sd-targets` with key `targets.yaml` is referenced as `/etc/prometheus/configmaps/scrape-file-sd-targets/targets.yaml`.

## http_sd
`httpSDConfigs` points at a URL returning the target list, removing the need for a ConfigMap. The docs example sets `url: http://my-external-api/discovery` (a placeholder) and `refreshInterval: 15s`.

Select the ScrapeConfig with `scrapeConfigSelector` as for any other.

## Checked

2026-11-08. Read scrapeconfig.md in full. Removed unsourced claims (volumes mounting, file re-read, http_sd use case) and added the docs example paths and refreshInterval.

Method: documentation only; no commands were run.
