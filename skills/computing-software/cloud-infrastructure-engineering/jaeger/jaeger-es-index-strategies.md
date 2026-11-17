---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-index-strategies
name: jaeger-es-index-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, index-management, use-aliases, create-mappings, date-layout]
level: practitioner
status: docs-checked
description: "Compare time-based indices, manual rollover and rollover with ILM, and the config flags that select each."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick an index lifecycle strategy.

- Time-based (default): Jaeger creates daily or hourly indices such as jaeger-span-2024-06-18. Cleanup by the `jaeger-es-index-cleaner` cron job. No other tooling.
- Manual rollover: operator runs `jaeger-es-rollover init` once (first index like jaeger-span-000001); a cron job runs `jaeger-es-rollover rollover`; cleanup by index cleaner plus optional `lookback`.
- Rollover with ILM (recommended): `init` once plus an ILM policy; Elasticsearch handles rollover and retention.

Config properties:
- `date_layout`: default 2006-01-02 (time-based)
- `use_aliases`: default false; true enables rollover mode with read/write aliases
- `use_ilm`: default false; requires `use_aliases: true`
- `create_mappings`: default true; creates index templates at startup. Must be false when `use_ilm: true`, since `jaeger-es-rollover init` already creates the templates. In any mode you may set it false to manage templates yourself.

Why rollover: daily indices can waste shards on empty indices while another index grows much larger. Rollover conditions: `max_age` (units d, h, m), `max_docs`, `max_size` (tb, gb, mb; primary shard size). It is more complex than daily indices and needs an init job plus cron jobs.

## Checked

2026-11-03. Confirmed against the Elasticsearch page: the three index management strategies and their tooling, the defaults and meaning of date_layout, use_aliases, use_ilm and create_mappings, the create_mappings rule for ILM, and the rollover conditions with their units. Nothing removed.
Method: documentation only; no commands were run.
