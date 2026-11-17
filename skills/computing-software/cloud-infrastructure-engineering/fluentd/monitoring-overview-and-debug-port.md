---
id: computing-software.cloud-infrastructure-engineering.fluentd.monitoring-overview-and-debug-port
name: monitoring-overview-and-debug-port
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, monitoring, process-monitoring, port-monitoring, debug-agent, fluent-debug]
level: practitioner
status: docs-checked
description: "Monitor Fluentd health: the two ruby processes, port checks on 9880 and 24224, metrics options, and the local debug_agent port with fluent-debug."
sources:
  - https://docs.fluentd.org/monitoring-fluentd/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd monitoring overview
- **Metrics**: expose via REST API (`monitor_agent`), Prometheus (the page recommends it), or Datadog.
- **Process monitoring**: Fluentd runs two `ruby` processes (parent and child). Check both exist, for example for td-agent `ps w -C ruby -C td-agent --no-heading` should list two.
- **Port monitoring**: check ports from your config; defaults named are TCP 9880 (HTTP) and 24224 (forward).
- **Debug port**: a local port for troubleshooting.
```
<source>
  @type debug_agent
  bind 127.0.0.1
  port 24230
</source>
```
Attach with `fluent-debug` (dRuby). Since v1.19.3 `bind` defaults to `127.0.0.1` instead of `0.0.0.0`; the page warns that this feature has no access control, so exposing it remotely is at your own risk.

See `monitor-agent-rest-api` and `prometheus-monitoring`.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/monitoring-fluentd/overview and confirmed: two ruby processes, default ports, debug_agent configuration and bind default change. Removed or reworded: the claim that Prometheus is recommended because both are CNCF projects (reworded to the page wording).

Method: documentation only; no commands were run.
