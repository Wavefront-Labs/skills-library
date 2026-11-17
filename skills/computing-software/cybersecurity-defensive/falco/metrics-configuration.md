---
id: computing-software.cybersecurity-defensive.falco.metrics-configuration
name: metrics-configuration
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falco-metrics, metrics-interval, output-rule, prometheus-metrics, webserver]
level: practitioner
status: docs-checked
description: "Enable Falco native metrics in falco.yaml, choose counters and output, and expose a Prometheus /metrics endpoint."
sources:
  - https://falco.org/docs/concepts/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco metrics are disabled by default. Enable them in `falco.yaml`:

```yaml
metrics:
  enabled: true
  interval: 1h
  output_rule: true
  # output_file: /tmp/falco_stats.jsonl
  rules_counters_enabled: true
  resource_utilization_enabled: true
  state_counters_enabled: true
  kernel_event_counters_enabled: true
  libbpf_stats_enabled: true
  plugins_metrics_enabled: true
```

The documented example configuration also sets `kernel_event_counters_per_cpu_enabled: false` (setting it true automatically enables `kernel_event_counters_enabled`), `jemalloc_stats_enabled: false`, `convert_memory_to_mb: true` and `include_empty_values: false`. In production you normally use `output_rule` or `output_file`, not both.

Snapshots appear as an alert from the internal rule `Falco internal: metrics snapshot` with fields like `falco.evts_rate_sec`, `falco.num_evts`, `falco.outputs_queue_num_drops` and `scap.n_drops_perc`.

Prometheus: keep `metrics.enabled: true` and also enable the web server:

```yaml
webserver:
  enabled: true
  prometheus_metrics_enabled: true
```

`/metrics` is then served on the same port as the health endpoint.

Gotcha: plugin metrics appear only if the plugin provides them, and only the container plugin supports them so far.

The `output_file` option writes snapshots to a file (the example path is `/tmp/falco_stats.jsonl`), and `interval` sets how often a snapshot is produced (1h in the example).

## Checked

2026-11-08. Read: the Falco Metrics page (raw markdown `docs/content/en/docs/concepts/metrics/_index.md`), first 150 lines of about 650 (configuration block, plugin metrics, Prometheus support, and the start of the JSON example). The later lines are per-metric example output and were not read. Confirmed the config keys, Prometheus webserver keys, `/metrics` port and the container-plugin note. Reworded the "shipped defaults" and JSON-lines claims to match what the page shows.

Method: documentation only; no commands were run.
