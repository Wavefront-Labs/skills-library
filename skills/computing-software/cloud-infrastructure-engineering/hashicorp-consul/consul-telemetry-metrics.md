---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-telemetry-metrics
name: consul-telemetry-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-telemetry, consul-metrics, prometheus-retention]
level: practitioner
status: docs-checked
description: "Export Consul metrics to Prometheus or statsd, disable hostname prefixes, and alert on memory, GC and root CA expiry."
sources: ["https://developer.hashicorp.com/consul/docs/agent/telemetry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable telemetry in config and scrape the metrics endpoint.

```hcl
telemetry {
  prometheus_retention_time = "60s"
  disable_hostname = true
}
```

```sh
curl -s 'localhost:8500/v1/agent/metrics?format=prometheus' | head
kill -USR1 $(pidof consul)    # dump metrics to the agent's stderr
```

The telemetry guide suggests watching: `consul.runtime.sys_bytes` above 90% of total system memory (Consul keeps all of its data in memory and crashes if it runs out), `consul.runtime.total_gc_pause_ns` (warning above 2 seconds per minute, critical above 5), `consul.raft.leader.lastContact` (healthy is below 200ms) and `consul.mesh.active_root_ca.expiry`.

Gotchas: gauge metric names are prefixed with the agent hostname unless `telemetry.disable_hostname` is true. `prometheus_retention_time` (default 0s, which disables Prometheus export) should be at least 2 times the Prometheus scrape interval, and aggregates counters for that duration, which can affect memory. `total_gc_pause_ns` is a cumulative counter, so compute a rate. Consul does not automatically rotate the root CA, so monitor its expiry.

Verify: `curl -s 'localhost:8500/v1/agent/metrics?format=prometheus'` returns metrics.

## Checked

2026-11-03. Confirmed against the agent telemetry page (USR1 dump on Unix, hostname prefix and disable_hostname, memory, GC pause and lastContact thresholds, root CA not auto-rotated) and the telemetry configuration page (prometheus_retention_time default and the 2 times scrape interval guidance) and the agent metrics API page (format=prometheus). Removed: the Prometheus series name, the leader election counters and the dashboard advice.

Method: documentation only; no commands were run.
