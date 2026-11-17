---
id: computing-software.cybersecurity-defensive.authelia.prometheus-metrics-exporter
name: prometheus-metrics-exporter
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, prometheus, metrics, telemetry, observability, exporter]
level: practitioner
status: docs-checked
description: "Enable Authelia's Prometheus metrics exporter on its own listener address, with buffers and timeouts, and keep it off the public network."
sources:
  - https://www.authelia.com/configuration/telemetry/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia can expose Prometheus metrics from a separate HTTP server.

```yaml
telemetry:
  metrics:
    enabled: true
    address: 'tcp://:9959/metrics'
    buffers:
      read: 4096
      write: 4096
    timeouts:
      read: '6s'
      write: '6s'
      idle: '30s'
```

- `enabled` is false by default.
- `address` is a listener address whose scheme is `unix` or one of the `tcp` schemes. The example above listens on port 9959 at the path `/metrics`.
- `buffers` and `timeouts` use the common server buffers and server timeouts structures and configure this metrics server (the values above are the page's example).

The exporter is an HTTP server of its own, configured by its own `address`. The page does not describe access control for it, so restrict network access to your Prometheus scrape network yourself.

A Prometheus scrape config then targets host and port:

```yaml
scrape_configs:
  - job_name: 'authelia'
    static_configs:
      - targets: ['authelia.example.com:9959']
```

The page points to the Telemetry Reference Documentation for the exported metrics.

Check: `curl http://authelia.example.com:9959/metrics` from the monitoring host returns Prometheus text format.

## Checked

2026-11-08. Read the full Authelia Metrics page. Confirmed enabled default false, the listener address syntax and schemes, and the buffers and timeouts structures. Removed unsourced claims about reverse proxy routing and Docker or Kubernetes port publishing; the example values are labelled as examples.

Method: documentation only; no commands were run.
