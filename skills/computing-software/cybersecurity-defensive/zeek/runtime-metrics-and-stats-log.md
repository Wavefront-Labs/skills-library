---
id: computing-software.cybersecurity-defensive.zeek.runtime-metrics-and-stats-log
name: runtime-metrics-and-stats-log
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, metrics, prometheus-endpoint, stats-log, report-interval]
level: practitioner
status: docs-checked
description: "Monitor Zeek health: the Prometheus endpoint on port 9911, which metric families it exposes, telemetry.log, and stats.log with Stats::report_interval."
sources: ["https://docs.zeek.org/en/current/advanced/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# runtime metrics and stats.log

**Prometheus**: the troubleshooting page recommends consuming metrics from the endpoint on the manager, `http://manager-ip:9911/metrics` as its example (the port is set by `Telemetry::metrics_port`). It exposes version info, network and process metrics, log records per stream and writer, event invocations, and Broker subsystem metrics. Check it with curl:

```
curl -s localhost:9911/metrics | grep -E '^(zeek_version|zeek_log|zeek_event|zeek_net|process_)'
```

Example families: `zeek_net_dropped_packets_total`, `zeek_net_received_packets_total`, `zeek_log_writer_writes_total`, `zeek_event_handler_invocations_total`, `zeek_active_sessions`, `process_resident_memory_bytes`. A Prometheus server normally scrapes it.

**telemetry.log** (`Telemetry::Info`) is an alternative for log-based consumption, though its format is unusual.

**stats.log** is enabled by loading `policy/misc/stats.zeek`, which the stock `local.zeek` does. Fields are described by `Stats::Info`. The default reporting interval is 5 minutes; shorten for troubleshooting:

```
redef Stats::report_interval=30sec;
```

Collection may cost performance, so avoid intervals like every second. For historic reasons it holds delta values (`pkts_proc`, `bytes_recv`, `events_proc`, `tcp_conns`), which suit counter-based metrics systems poorly. For custom metrics, log absolute counter values since deltas can be derived from them but not the reverse.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
