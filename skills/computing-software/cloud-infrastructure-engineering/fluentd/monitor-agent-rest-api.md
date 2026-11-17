---
id: computing-software.cloud-infrastructure-engineering.fluentd.monitor-agent-rest-api
name: monitor-agent-rest-api
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, monitor-agent, rest-api, metrics, include-retry, include-config, plugins-json]
level: practitioner
status: docs-checked
description: "Expose Fluentd internal metrics as JSON or LTSV with in_monitor_agent: endpoints, bind and port, include_config/include_retry/include_debug_info, and @id advice."
sources:
  - https://docs.fluentd.org/monitoring-fluentd/monitoring-rest-api
  - https://docs.fluentd.org/input/monitor_agent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd monitor_agent
```
<source>
  @type monitor_agent
  bind 0.0.0.0
  port 24220
</source>
```
Endpoints (no `.json` suffix returns LTSV): `/api/plugins.json` (per-plugin metrics), `/api/config.json` (process info and startup options, not config contents). `/api/config.reload` belongs to RPC, not this plugin.

Parameters: `port` (default 24220), `bind` (default `0.0.0.0`; no authentication, so use `127.0.0.1` if remote access is unneeded), `tag` with `emit_interval` (default 60) to emit metrics as records, `include_config`, `include_retry` (both default false since v1.19.3; `config` may contain secrets), `include_debug_info` (1.19.3, enables `debug` and `with_ivars` query parameters; exposes internal state including sensitive values).

Metrics include `plugin_id`, `plugin_category`, `type`, `output_plugin`, `retry_count`, `emit_records`, `emit_size`, and for buffered outputs `buffer_queue_length`, `buffer_total_queued_size`, `buffer_stage_length`, `buffer_available_buffer_space_ratios`, `write_count`, `rollback_count`, `slow_flush_count`, `drop_oldest_chunk_count`, and more.

Set `@id` on every plugin; otherwise `plugin_id` is an `object_id`-style value that is hard to map to a plugin. The page points to the `flowcounter` and `flowcounter_simple` plugins for event-flow monitoring and describes Datadog's dd-agent integration.

Under multiple workers each worker takes a sequential port (see `multi-process-workers`).

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/monitoring-fluentd/monitoring-rest-api, https://docs.fluentd.org/input/monitor_agent and confirmed: endpoints, port and bind defaults, include_* options, metric field names, @id advice, multi-worker ports. Removed or reworded: the plugin name fluent-plugin-flowcounter (the page names flowcounter and flowcounter_simple).

Method: documentation only; no commands were run.
