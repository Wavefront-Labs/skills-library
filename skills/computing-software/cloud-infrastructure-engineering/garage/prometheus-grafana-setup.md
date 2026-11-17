---
id: computing-software.cloud-infrastructure-engineering.garage.prometheus-grafana-setup
name: prometheus-grafana-setup
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [prometheus-scrape, grafana, admin-api-bind-addr, metrics-endpoint]
level: practitioner
status: docs-checked
description: "Enable the admin endpoint and scrape every node on port 3903 with Prometheus, using a bearer token if set."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/cookbook/monitoring/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/monitoring/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/admin-api/
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage exports Prometheus metrics from its admin endpoint. Enable it in the config:

```
[admin]
api_bind_addr = "0.0.0.0:3903"
```

This lets anyone scrape `http://localhost:3903/metrics`. To restrict access, set `metrics_token` to a bearer token.

Add a scrape job covering every node:

```
scrape_configs:
  - job_name: 'garage'
    static_configs:
      - targets: ['node1.mycluster:3903', 'node2.mycluster:3903', 'node3.mycluster:3903']
```

With a metrics token, add under the job `authorization: { type: Bearer, credentials: 'your metrics token' }`.

For visualisation, either import the Garage Grafana dashboard linked from the cookbook page or build your own. The reference manual's Monitoring page gives the list of exported metrics, including cluster health gauges such as `cluster_healthy` and the `api_s3_request_counter` counter labelled by `api_endpoint`.

Access options: `metrics_token` is optional (without it, and without `metrics_require_token`, the endpoint needs no authentication). `metrics_require_token` (since v2.0.0) makes the metrics endpoint always require a token; valid tokens are the `metrics_token` and dynamically defined admin API tokens with the Metrics endpoint in their scope. The quick start config binds the admin API on port 3903 and sets both `admin_token` and `metrics_token`.

The admin API also serves `GET /health` (200 when enough nodes are up for quorum, otherwise 503) on the same admin port.

## Checked

Date: 2026-11-07

Read in full: the Garage cookbook Monitoring page (short page, the whole text including both config snippets). Read the relevant sections of the reference manual Configuration page (the `[admin]` keys `metrics_token` and `metrics_require_token`, the config example), the reference manual Monitoring page (list of exported metrics, cluster health section, `api_s3_request_counter`), the Admin API page (Metrics and Health special endpoints, the token table) and the Quick Start config block; these four pages are large and were searched by keyword, not read end to end.
Trimmed: "lists all exported metrics" reworded to "gives the list"; the claim that one port covers load balancer probes was dropped (the pages describe /health but not load balancer use); the dashboard is described as linked from the page rather than published by the project.
Not opened: the linked Grafana dashboard itself.

Method: documentation only; no commands were run.
