---
id: computing-software.messaging-and-integration.dapr.prometheus-scrape-dapr-on-kubernetes
name: prometheus-scrape-dapr-on-kubernetes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [prometheus, metrics, kubernetes, helm, service-discovery, scrape-config, dapr-monitoring]
level: practitioner
status: docs-checked
description: "Scrape Dapr sidecars with Prometheus: local config for port 9090, Helm install into dapr-monitoring, and kubernetes_sd relabel rules on dapr.io/enabled and enable-metrics."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/observability/metrics/prometheus.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local scrape config (targets the Dapr metrics port, default 9090):

```yaml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
scrape_configs:
  - job_name: 'dapr'
    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090'] # Replace with Dapr metrics port if not default
```

Run Prometheus on a different port, for example `./prometheus --config.file=/tmp/prometheus.yml --web.listen-address=:8080`, or in Docker with `--net=host` so it can reach Dapr instances on the host.

Kubernetes (needs Kubernetes above 1.14, kubectl, Helm 3):

```bash
kubectl create namespace dapr-monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install dapr-prom prometheus-community/prometheus -n dapr-monitoring
```

For automatic discovery pass a values file: `helm install dapr-prom prometheus-community/prometheus -f values.yaml -n dapr-monitoring --create-namespace`. The page values.yaml disables persistence for alertmanager, pushgateway and server (development) and adds `extraScrapeConfigs` with job `dapr-sidecars` using `kubernetes_sd_configs` with `role: pod`. Its relabel rules keep only pods whose annotations `dapr.io/enabled` and `dapr.io/enable-metrics` are `"true"`, copy the namespace and pod name into labels, set the `service` label to the app ID plus `-dapr` for the `daprd` container, and set `__address__` to the pod IP with port `9090`.

So a pod is only scraped when both annotations are present. The page's `static_configs` comment says to replace the target with the Dapr metrics port if it is not the default.

## Checked

2026-11-04. Prometheus configuration, Helm commands and values.yaml scrape config confirmed on the Observe metrics with Prometheus page.

Method: documentation only; no commands were run.
