---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-agent-collection-scheduling
name: telegraf-agent-collection-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [agent, interval, round-interval, collection-jitter, flush-jitter, precision]
level: practitioner
status: docs-checked
description: "Documents the agent settings that control collection and flush timing: interval, round_interval, jitter, offset, flush_interval and precision."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/agent/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agent collection and flush scheduling

The `[agent]` table sets defaults used across plugins. Define it once, in the first configuration file read. Durations are TOML strings such as `"10s"`.

## Collection

- `interval` (default `"10s"`): default collection interval for all inputs.
- `round_interval` (default true): collect on interval boundaries; with 10s, at :00, :10, :20.
- `collection_jitter` (default `"0s"`): each plugin sleeps a random time within the jitter before collecting, so many plugins do not hit resources such as sysfs together.
- `collection_offset` (default `"0s"`): shifts collection to stagger plugins that query constrained devices.

## Flush

- `flush_interval` (default `"10s"`): default for all outputs. Maximum time between flushes is `flush_interval + flush_jitter`.
- `flush_jitter` (default `"0s"`): random flush offset that avoids write spikes from many instances.

## Batching

`metric_batch_size` (1000) and `metric_buffer_limit` (10000).

## Timestamps

`precision` (default `"0s"`, no rounding) rounds timestamps but is not applied to service inputs, which set their own precision. On service inputs, per-plugin precision can cause events with identical timestamps to merge in the database.

## Host identity

`hostname` overrides the `host` tag value; `omit_hostname = true` removes the tag.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): [agent] reference: interval, round_interval, jitter, offset, flush, batch and buffer defaults, precision, hostname, omit_hostname; plugin-options (service-input precision merge). Removed: nothing.

Method: documentation only; no commands were run.
