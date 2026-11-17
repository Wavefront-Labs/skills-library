---
id: computing-software.database-administration.time-series-databases.promql-subqueries-staleness
name: promql-subqueries-staleness
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-promql-cost, promql-subqueries-staleness, prometheus]
level: practitioner
status: docs-checked
description: "Use PromQL subqueries, the @ and offset modifiers, the 5m lookback and staleness markers correctly."
sources:
  - https://prometheus.io/docs/prometheus/latest/querying/basics/
  - https://prometheus.io/docs/prometheus/latest/command-line/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subqueries and staleness

**Goal:** Use subqueries and staleness semantics correctly.

## Steps
- Subquery syntax: `<instant_query>[<range>:<resolution>]`, optionally followed by `@` and `offset`. It runs an instant query over a range at a resolution and returns a range vector. The resolution is optional and defaults to the global evaluation interval. Example: `max_over_time(rate(http_requests_total[5m])[1h:1m])` evaluates the inner `rate` every minute over one hour.
- Cost grows with the number of subquery steps, because the inner expression is evaluated at each one; avoid long ranges with small resolutions.
- Lookback: an instant selector returns the newest sample less than the lookback period old; the default is 5 minutes, set by `--query.lookback-delta` or per query with the `lookback_delta` parameter.
- Staleness: if a scrape or rule evaluation no longer returns a series that was present, the series is marked stale, and queries evaluated after the marker return no value for it. A removed target's series are marked stale soon after removal.
- Exporters that put their own timestamps on samples behave differently: series that stop being exported keep their last value for the lookback period (5 minutes by default) before disappearing; `track_timestamps_staleness` changes this.
- `@ <unix timestamp>` fixes the evaluation time of a selector (`start()` and `end()` are also allowed); `offset` shifts it. Both must directly follow the selector.

**Gotcha:** Series exposed with explicit timestamps (some exporters) can appear alive for the full lookback period after they stop.

## Verify
- A stopped target's series stop being returned shortly after it is removed.
- The subquery cost (see `stats=all`) is acceptable.

## Checked
2026-11-03. Confirmed against the PromQL basics page (subquery syntax and default resolution, `@` and `offset` rules, lookback, staleness behaviour, explicit-timestamp exporters) and the command-line page (`--query.lookback-delta`). Removed: the "stale after being absent 5 minutes" wording (the page ties staleness to markers, with lookback as the sampling window), the claim that markers are always written when a target stops exposing a series beyond the page's wording, and the "within one scrape interval" timing.
Method: documentation only; no commands were run.
