---
id: computing-software.collaboration-platform-administration.matrix-synapse.prometheus-metrics-endpoint-and-workers
name: prometheus-metrics-endpoint-and-workers
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, prometheus, metrics, enable-metrics, grafana, listeners, workers, scrape]
level: practitioner
status: docs-checked
description: "Expose Synapse metrics to Prometheus with enable_metrics and a metrics resource or dedicated listener, scrape /_synapse/metrics, and add per-worker metrics listeners."
sources:
  - https://element-hq.github.io/synapse/latest/metrics-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `enable_metrics` to `True` in `homeserver.yaml`, then expose the `/_synapse/metrics` endpoint by one of two methods.

**Method 1: metrics resource on an existing listener.** Add `metrics` to the resource names, for example `names: [client, federation, metrics]` with `compress: false`. It is simple, but the endpoint is then served with normal traffic, so if you do not want it public you must filter it at your load balancer.

**Method 2: dedicated listener.** It runs in a different thread on another port, which makes it more resilient when Synapse is under load and easier to restrict to internal networks. Metrics are HTTP only:

```yaml
  - port: 9000
    type: metrics
    bind_addresses: ['::1', '127.0.0.1']
```

Restart Synapse, then add a Prometheus target with a non-default `metrics_path` under `scrape_configs`:

```yaml
  - job_name: "synapse"
    scrape_interval: 15s
    metrics_path: "/_synapse/metrics"
    static_configs:
      - targets: ["my.server.here:port"]
```

Here `port` is the listener carrying the `metrics` resource. Prometheus older than 1.5.2 needs `target_groups` in place of `static_configs`. Restart Prometheus afterwards. The docs also point to a Grafana dashboard and required recording rules.

**Workers.** Workers do not forward metrics to the main process; each must be scraped independently. Add a listener under `worker_listeners`:

```yaml
  - type: metrics
    bind_address: ''
    port: 9101
```

Choose an address and port that Prometheus can reach and that do not clash with another worker. In the Prometheus config give each target `job` and `index` labels (for example `master`, `generic_worker` index 1 and 2, `media_repository`); the labels can be anything and are used to group Grafana graphs.

## Checked

2026-11-04. Confirmed against the Synapse metrics howto page: enable_metrics, both listener methods, scrape config, older-Prometheus note, worker metrics listener and labels. Removed contrib directory names (not on the page).
Method: documentation only; no commands were run.
