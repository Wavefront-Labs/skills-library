---
id: computing-software.systems-network-administration.healthchecks.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, prometheus, hc-metrics, grafana-cloud, scrape-config]
level: advanced
status: docs-checked
description: "Export Healthchecks check status to Prometheus: read-only API key, scrape job config, hc_ metric names and labels, unique_key links and Grafana Cloud bearer auth."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_prometheus.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Create a read-only API key in Project Settings, API Access.
2. Add a scrape job:

```
  - job_name: "healthchecks"
    scrape_interval: 60s
    scheme: https
    metrics_path: /projects/{your-project-uuid}/metrics/{your-readonly-api-key}
    static_configs:
      - targets: ["<site-hostname>"]
```

The project UUID is in the browser address bar on the project's check list. Reload Prometheus afterwards.

Metrics (prefix `hc_`):
- Per check, labels `name`, `tags`, `unique_key`; value 1 or 0: `hc_check_up`, `hc_check_started`, `hc_check_grace`, `hc_check_paused`.
- Per tag: `hc_tag_up{tag}`, 1 when all checks with the tag are up.
- Aggregates: `hc_checks_total`, `hc_checks_down_total`.

Link an alert to a check's page with `<site-root>/cloaked/{unique_key}/`.

Grafana Cloud will not scrape public endpoints, so use the endpoint that takes Bearer auth: scrape URL `<site-root>/projects/{your-project-uuid}/metrics/`, authentication type Bearer, token set to the read-only API key.

Self-hosted: `PROMETHEUS_ENABLED` (default True) toggles the integration.

## Checked

2026-11-04. Confirmed against the Healthchecks Configuring Prometheus page and server configuration page: the read-only key in Project Settings, API Access, the scrape job fields, the project UUID location, all hc_ metric names and labels, the cloaked unique_key URL, the Grafana Cloud Bearer endpoint, and PROMETHEUS_ENABLED default True. Nothing removed.

Method: documentation only; no commands were run.
