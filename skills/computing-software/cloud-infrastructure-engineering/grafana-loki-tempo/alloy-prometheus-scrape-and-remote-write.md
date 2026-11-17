---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-prometheus-scrape-and-remote-write
name: alloy-prometheus-scrape-and-remote-write
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [alloy-prometheus-scrape, alloy, prometheus.scrape, prometheus.remote_write, prometheus.relabel, metric-relabeling]
level: practitioner
status: docs-checked
description: "Scrape metrics with Alloy and ship them to Mimir or Prometheus with relabeling, external labels and queue settings."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.scrape/", "https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.remote_write/", "https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.relabel/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace a Prometheus agent with Alloy.

```
prometheus.scrape "app" {
  targets         = discovery.relabel.pods.output
  forward_to      = [prometheus.relabel.drop_noise.receiver]
  scrape_interval = "30s"
  clustering { enabled = true }
}

prometheus.relabel "drop_noise" {
  forward_to = [prometheus.remote_write.mimir.receiver]
  rule {
    action        = "drop"
    source_labels = ["__name__"]
    regex         = "go_gc_.*|promhttp_.*"
  }
}

prometheus.remote_write "mimir" {
  external_labels = { cluster = "prod-eu" }
  endpoint {
    url = "https://mimir.example.com/api/v1/push"
    queue_config {
      max_shards = 30
      capacity   = 10000
    }
  }
}
```

Defaults and behaviour
- `prometheus.scrape` scrapes each target's `/metrics` over HTTP by default, with `scrape_interval` of `60s` and `scrape_timeout` of `10s`. `forward_to` and `targets` are required; the job name defaults to the component's identifier.
- With `clustering { enabled = true }` and Alloy running in cluster mode, scrape components share the target set by consistent hashing, each peer scraping only its subset. All peers must use the same configuration and service discovery. Without it, each replica scrapes all targets.
- `prometheus.relabel` rewrites the label set of each metric by applying `rule` blocks in order; metrics left with no labels are dropped. Its action defaults to `replace`; `drop` drops metrics whose source labels match `regex`. It filters series, not scrape targets: use `discovery.relabel` for targets.
- `prometheus.remote_write` writes metrics into a write-ahead log (WAL) and forwards them to the endpoints. `external_labels` adds labels to everything sent. Each endpoint has a queue; `queue_config` `capacity` (default `10000`) is samples buffered per shard and `max_shards` (default `50`) is the maximum number of concurrent shards.
- The WAL buffers unsent metrics through intermittent network problems and repopulates the in-memory cache after a restart. It lives in a component-specific directory under the configured storage path, so use persistent storage if it must survive restarts.
- Component metrics include `prometheus_remote_storage_samples_total`, `prometheus_remote_storage_samples_retries_total`, `prometheus_remote_storage_samples_failed_total` and `prometheus_remote_storage_samples_dropped_total`.

## Verify
Fetch the Alloy `/metrics` endpoint and check that `prometheus_remote_storage_samples_total` increases; the receiving store should show series with the external label.

## Checked
Method: docs-checked 2026-11-09 against the Alloy docs prometheus.scrape, prometheus.remote_write and prometheus.relabel reference pages (raw markdown, argument tables, clustering, queue_config, wal and metrics sections read) and the shared rule block. Removed the tenant header and operator-CRD claims as unconfirmed.
