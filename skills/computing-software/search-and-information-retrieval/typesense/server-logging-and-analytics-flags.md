---
id: computing-software.search-and-information-retrieval.typesense.server-logging-and-analytics-flags
name: server-logging-and-analytics-flags
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [logging, slow-requests, access-logging, typesense]
level: practitioner
status: docs-checked
description: "Enable Typesense log files, access and search logging, slow request and slow search thresholds, and analytics flags with their defaults."
sources: ["https://typesense.org/docs/30.2/api/server-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging and analytics flags

## Logging

By default Typesense logs to stdout and stderr.

- `--log-dir`: write `typesense.log` inside this directory.
- `--enable-access-logging` (default `false`): log API requests and IP addresses to `typesense-access.log` in the log dir.
- `--enable-search-logging` (default `false`): log each search request and payload at the start of its lifecycle to `typesense.log`.
- `--log-slow-requests-time-ms`: requests slower than this are logged; default `-1` disables it. It can be toggled at runtime through the `/config` API.
- `--log-slow-searches-time-ms`: applies to `/documents/search` and `/multi_search`; default `30000`, `-1` disables. Also changeable at runtime via the `/config` API using the key `log-slow-searches-time-ms`.

## Analytics

- `--enable-search-analytics` (default `false`): allow search queries to be aggregated for query analytics.
- `--analytics-dir`: where analytics data is stored.
- `--analytics-flush-interval`: seconds between persisting aggregated queries, default `3600`.
- `--analytics-minute-rate-limit`: maximum analytics events per minute, default `5`.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Server Configuration (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
