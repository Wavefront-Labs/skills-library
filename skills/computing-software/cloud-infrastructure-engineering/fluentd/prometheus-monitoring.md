---
id: computing-software.cloud-infrastructure-engineering.fluentd.prometheus-monitoring
name: prometheus-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, prometheus, fluent-plugin-prometheus, metrics, scrape, monitoring]
level: practitioner
status: docs-checked
description: "Monitor Fluentd with fluent-plugin-prometheus: count incoming and outgoing records per tag, expose /metrics on 24231, and the built-in output metrics."
sources:
  - https://docs.fluentd.org/monitoring-fluentd/monitoring-prometheus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd with Prometheus
Install `fluent-gem install fluent-plugin-prometheus` (td-agent: `td-agent-gem`). Three parts:

1. **Count incoming** with a `prometheus` filter:
```
<filter company.*>
  @type prometheus
  <metric>
    name fluentd_input_status_num_records_total
    type counter
    desc The total number of incoming records
    <labels>
      tag ${tag}
      hostname ${hostname}
    </labels>
  </metric>
</filter>
```
2. **Count outgoing** by adding a `<store> @type prometheus` (same `<metric>` shape, name `fluentd_output_status_num_records_total`) inside a `copy` match next to the real output.
3. **Expose**:
```
<source>
  @type prometheus
  bind 0.0.0.0
  port 24231
  metrics_path /metrics
</source>
<source>
  @type prometheus_output_monitor
  interval 10
</source>
```
Scrape `localhost:24231` from a Prometheus `scrape_configs` job (`job_name: 'fluentd'`, `static_configs` targets). Test with `fluent-cat company.test1`, then `curl http://localhost:24231/metrics`.

Metrics listed: `fluentd_input_status_num_records_total`, `fluentd_output_status_buffer_queue_length`, `fluentd_output_status_buffer_total_bytes`, `fluentd_output_status_emit_count`, `fluentd_output_status_num_errors`, `fluentd_output_status_num_records_total`, `fluentd_output_status_retry_count`, `fluentd_output_status_retry_wait`.

## Checked

2026-11-04. Confirmed against the Fluentd Monitoring by Prometheus page (docs.fluentd.org/monitoring-fluentd/monitoring-prometheus): install commands, the three config parts, port 24231 and /metrics, scrape config, fluent-cat test and the eight metric names. The page's sample prometheus_output_monitor block also has a hostname label, omitted here. Nothing removed.

Method: documentation only; no commands were run.
