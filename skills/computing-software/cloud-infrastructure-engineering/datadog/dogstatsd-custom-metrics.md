---
id: computing-software.cloud-infrastructure-engineering.datadog.dogstatsd-custom-metrics
name: dogstatsd-custom-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, dogstatsd, custom-metrics, statsd, metric-submission]
level: practitioner
status: docs-checked
description: "Send custom metrics from code through DogStatsD on UDP 8125 or a unix socket, with datagram format, naming rules and buffering."
sources: ["https://docs.datadoghq.com/extend/dogstatsd/", "https://docs.datadoghq.com/metrics/custom_metrics/", "https://docs.datadoghq.com/metrics/custom_metrics/dogstatsd_metrics_submission/", "https://docs.datadoghq.com/extend/dogstatsd/datagram_shell/", "https://docs.datadoghq.com/extend/dogstatsd/high_throughput/", "https://docs.datadoghq.com/extend/dogstatsd/unix_socket/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DogStatsD custom metrics
Goal: emit application metrics through the DogStatsD server bundled with the Agent.

```python
from datadog import initialize, statsd
initialize(statsd_host="127.0.0.1", statsd_port=8125)
statsd.increment("example_metric.increment", tags=["environment:dev"])
statsd.gauge("example_metric.gauge", 42, tags=["environment:dev"])
statsd.distribution("example_metric.distribution", 12, tags=["environment:dev"])
```

From a shell, send a datagram directly:

```
echo -n "custom.metric.name:1|c" | nc -4u -w1 localhost 8125
```

Datagram forms from the docs: `page.views:1|c`, `fuel.level:0.5|g`, `song.length:240|h|@0.5` (sample rate), `users.online:1|c|#country:china` (tags after `#`), `page.views:1:2:32|d` (three distribution values).

- The DogStatsD server is on by default over UDP port `8125` (Agent v6+); `dogstatsd_port` changes it.
- If metrics come from outside localhost (for example other containers), set `DD_DOGSTATSD_NON_LOCAL_TRAFFIC` to `true` on the Agent container and publish `8125/udp`.
- For a unix domain socket, set `DD_DOGSTATSD_SOCKET=<path>` on the Agent; clients must connect to that path.
- Metric names: start with a letter, only ASCII alphanumerics, underscores and periods (other characters, including spaces, become underscores), at most 200 characters (under 100 preferred), case sensitive.
- Increments and counts are stored as RATE (time-normalised over the flush period); gauges keep the last value in the flush period; submission calls are asynchronous, so `flush`/`close` the client before exit.
- Many clients send one metric per datagram by default; enable buffering so several metrics share a datagram. The Agent-side datagram buffer is 8KB by default (`dogstatsd_buffer_size`); keep client max datagram size under it. Client-side aggregation exists in the Go client from v5.0.0.

Gotcha: at high throughput datagrams can be dropped; check the high-throughput page for tuning. Every unique tag combination on a custom metric counts as a separate time series for custom-metric volume.

## Verify
- The metric appears in Metrics Summary.

## Checked
2026-11-03. Confirmed against the DogStatsD overview, datagram and shell, high-throughput and unix-socket pages, the custom metrics page (naming rules) and the DogStatsD metrics submission page (Python client code, flush note, RATE storage). Removed: the `datadog.` name-prefix claim, `statsd_aggregation` option name, `datadog-agent status` packet-counter claim, and unsupported advice.
Method: documentation only; no commands were run.
