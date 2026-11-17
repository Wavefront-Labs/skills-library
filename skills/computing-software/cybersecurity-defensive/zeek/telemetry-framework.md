---
id: computing-software.cybersecurity-defensive.zeek.telemetry-framework
name: telemetry-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, telemetry, metrics-port, prometheus-sd, telemetry-log]
level: practitioner
status: docs-checked
description: "Zeek telemetry: counter, gauge and histogram types, node registries, telemetry.log via frameworks/telemetry/log, Telemetry::metrics_port Prometheus export and service discovery."
sources: ["https://docs.zeek.org/en/current/frameworks/telemetry.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# telemetry framework

Metrics describe Zeek's operation or monitored traffic; they are not another export of regular logs. The data model resembles Prometheus: counter (only increases, resets on restart), gauge (rises and falls), histogram (pre-set buckets). There is no Summary type. Labels disambiguate related observations, such as the `protocol` label on `zeek_active_sessions`; a family is the set of metrics differing only by labels.

Each cluster node keeps its own registry, and Zeek no longer aggregates across the cluster; the node name is added at collection. `Telemetry::collect_metrics` returns node-local metrics only.

**Logs**: not on by default. Load the policy script:

```
@load frameworks/telemetry/log
redef Telemetry::log_prefixes += { "my_prefix" };
```

This writes `telemetry.log` and `telemetry_histogram.log` every 60 seconds (`Telemetry::log_interval`), each with a `peer` field. Only prefixes `zeek` and `process` are logged unless you add more; clearing the set logs all. Hooks `Telemetry::log_policy` and `Telemetry::log_policy_histogram` filter.

**Prometheus**: `Telemetry::metrics_port` defaults to `0/unknown` (disabled); set a TCP port to serve text exposition format, then `curl -s http://<node>:<port>/metrics`. zeekctl and the management framework can assign cluster ports. The manager also serves `http://<manager>:<port>/services.json` for Prometheus HTTP service discovery (`http_sd_configs` in `prometheus.yml`), so Prometheus does the aggregation.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
