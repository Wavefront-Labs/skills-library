---
id: computing-software.cloud-infrastructure-engineering.datadog.log-indexes-exclusion
name: log-indexes-exclusion
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, log-indexes, exclusion-filters, retention, index-routing]
level: practitioner
status: docs-checked
description: "Route logs to Datadog indexes by filter order, drop or sample noisy logs with exclusion filters, and set retention and daily quotas."
sources: ["https://docs.datadoghq.com/logs/log_configuration/indexes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log indexes and exclusion filters
Goal: control what is stored and searchable by index design.

Example layout (Logs > Configuration > Indexes):

```
Index "audit": filter service:audit, longer retention
Index "main":  filter *, exclusion filter status:DEBUG (100%, toggled off during incidents)
```

- Logs enter the first index whose filter they match, so index order matters. Drag and drop to reorder. A broad filter above a narrower one captures the logs first.
- Exclusion filters have a query (default `*`, which excludes everything in the index), a sampling rule and an active/inactive toggle. Excluded logs are discarded from the index but still flow through Live Tail, can generate metrics and can be archived.
- Only the first active exclusion filter a log matches applies; once a log matches one (even if not sampled out) later filters are ignored. Drag to reorder them.
- Debug pattern from the docs: a 100% exclusion on `status:DEBUG`, toggled on and off from the UI or the API when needed.
- Sampling can be keyed on an attribute (for example exclude 90% by `@user.email`, or 50% by trace ID, which needs the trace ID remapper upstream in the pipeline) so related logs are kept or dropped together. For consistent sampling across indexes, put an exclusion rule in each index with the same rate and attribute.
- Retention is a per-index setting limited to values enabled for your account.
- Daily quota: a hard limit, in millions of logs, on logs stored per index per day, applied after exclusion filters. After it is reached logs are no longer indexed but still reach Live Tail and archives and can generate metrics. Default reset is 2:00pm UTC (a custom reset time is optional). An optional warning threshold is a percentage of the quota (minimum 50%). Quota and warning events are generated when reached; changes take effect immediately.
- The `datadog.estimated_usage.logs.ingested_events` usage metric, with tags `datadog_index`, `datadog_is_excluded`, `service` and `status`, can be graphed and monitored.
- Deleting an index stops it accepting logs; its logs become unavailable for querying.

Gotcha: a quota stops indexing at the cap, so set a warning threshold and monitor the quota events.

## Verify
- Excluded logs are absent from Log Explorer but still visible in Live Tail.
- Index volume matches expectations on the Indexes page.

## Checked
2026-11-03. Confirmed against the Log Indexes page. Removed: Flex Logs/tiered storage statement and "confirm" markers, the "warn at 80%" figure (the page says warning threshold is configurable, minimum 50%), the "catch-all index with short retention" and monthly review advice, and the "90% of INFO" suggestion.
Method: documentation only; no commands were run.
