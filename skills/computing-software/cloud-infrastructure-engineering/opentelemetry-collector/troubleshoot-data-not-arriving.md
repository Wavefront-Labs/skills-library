---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.troubleshoot-data-not-arriving
name: troubleshoot-data-not-arriving
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, troubleshooting, dropped-data, receiver, exporter, null-maps]
level: practitioner
status: docs-checked
description: "Work out why telemetry does not reach the backend: check receivers, refused data, exporter errors and empty (null) config maps."
sources:
  - https://opentelemetry.io/docs/collector/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Work through the pipeline in order.

1. Is data reaching the receiver? Send a small test payload to a Collector with the `debug` exporter and look at the logs; `verbosity: detailed` prints the whole payload. Causes the page lists for no data: a network configuration issue, an incorrect receiver configuration, or an incorrect client configuration.
2. Is data dropped? The page's most common causes are an undersized Collector and an exporter destination that is unavailable or too slow. Configure the queued retry and sending queue options on the exporters. Memory pressure from a missing or misconfigured `memory_limiter` can also make the Collector exit or restart.
3. Is the exporter failing? Causes listed are a network configuration issue (firewall, DNS or proxy), an incorrect exporter configuration, and an unavailable destination. Check the Collector logs and zPages (local port 55679).
4. Is the component actually wired? A component that is configured but not listed in `service::pipelines` never runs.

A configuration trap is null maps: when multiple configs are resolved together, values in earlier configs are removed in favour of later configs, even if the later value is null. Write `{}` for an empty map (for example `processors: {}` instead of `processors:`), or omit empty configurations.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/troubleshooting page (docs repo raw markdown).
