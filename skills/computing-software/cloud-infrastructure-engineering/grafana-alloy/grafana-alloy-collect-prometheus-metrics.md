---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-collect-prometheus-metrics
name: grafana-alloy-collect-prometheus-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [prometheusscrape-targets, address, scheme, metrics-path, discoverykubernetes-selectors, namespaces-block, multiple-endpoints]
level: practitioner
status: docs-checked
description: "Collect Prometheus metrics with Alloy: remote_write endpoints, Kubernetes discovery with selectors, custom targets."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/collect/prometheus-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collecting Prometheus metrics

First define delivery, then scrapers that forward to it.

```alloy
prometheus.remote_write "default" {
  endpoint {
    url = "http://localhost:9009/api/v1/push"
  }
  endpoint {
    url = "https://prometheus.example.com/api/prom/push"
    basic_auth {
      username = sys.env("REMOTE_WRITE_USERNAME")
      password = sys.env("REMOTE_WRITE_PASSWORD")
    }
  }
}
```
Repeat the `endpoint` block per destination; labels must be unique per component type.

## Kubernetes pods or services
`discovery.kubernetes` with `role = "pod"` (or `"service"`) yields one target per exposed port. Narrow it:
```alloy
discovery.kubernetes "pods" {
  role = "pod"
  namespaces {
    own_namespace = false
    names         = ["default"]
  }
  selectors {
    role  = "pod"
    label = "environment in (production)"   // or field = "FIELD_SELECTOR"
  }
}
prometheus.scrape "pods" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.remote_write.default.receiver]
}
```
Add one `selectors` block per selector. Set `own_namespace = false` to stop searching Alloy's own namespace.

## Custom targets
Each target object needs `__address__` (HOST:PORT). Optional `__scheme__` (`http` or `https`, default inherited from the component, `http`) and `__metrics_path__` (default `/metrics`). Any other key becomes a label on the metrics; labels starting with `__` are dropped before scraping.
```alloy
prometheus.scrape "custom" {
  targets = [
    { __address__ = "mimir:8080", __scheme__ = "https" },
    { __address__ = "app:80", __metrics_path__ = "/custom-metrics-path", environment = "production" },
  ]
  forward_to = [prometheus.remote_write.default.receiver]
}
```

## Checked

2026-11-08. Read in full the raw Alloy docs page behind the cited URL (docs/sources/collect/prometheus-metrics.md): remote_write endpoints and basic_auth, pod and service discovery, namespaces and selectors blocks, own_namespace, and the custom-target rules for `__address__`, `__scheme__`, `__metrics_path__` and dropped `__` labels. Nothing removed.

Method: documentation only; no commands were run.
