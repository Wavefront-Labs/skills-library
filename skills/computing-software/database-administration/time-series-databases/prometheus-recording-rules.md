---
id: computing-software.database-administration.time-series-databases.prometheus-recording-rules
name: prometheus-recording-rules
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-recording, prometheus-recording-rules, prometheus]
level: practitioner
status: docs-checked
description: "Precompute expensive PromQL into new series with recording rules, load them via rule_files, check with promtool and backfill history."
sources:
  - https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/
  - https://prometheus.io/docs/prometheus/latest/command-line/promtool/
  - https://prometheus.io/docs/prometheus/latest/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording rules

**Goal:** Precompute expensive PromQL into new series that dashboards and alerts query cheaply.

## Steps
```
groups:
  - name: http
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
```
- Load with `rule_files:` in prometheus.yml; check syntax with `promtool check rules rules.yml`. Rule files reload on SIGHUP, and changes apply only if all rule files are well-formed.
- A group's `interval` defaults to `global.evaluation_interval`. Rules within a group run sequentially at the same evaluation time.
- Aggregate away high-cardinality labels in the expression.
- Add `labels:` (on the group or the rule) to tag results; labels on the rule override the group's on collision.
- `limit` on a group caps the series a recording rule can produce (0 is no limit).
- Unit-test with `promtool test rules <test file>`.
- A new rule has no history: backfill with `promtool tsdb create-blocks-from rules --start <time> --url <server> rules.yml`, then move the blocks into the data directory. Rules in the same group cannot see the results of previous rules during backfill.

**Gotcha:** Results are only as fresh as the group interval; a recorded 5m rate is evaluated once per interval, so do not set the interval below the scrape interval.

## Verify
- The new series appears in the Rules page of the UI with no errors.
- Its value matches the raw expression at a sampled time.

## Checked
2026-11-03. Confirmed against the recording rules page (rule_files, SIGHUP, promtool check rules, group interval default, sequential evaluation, labels, limit), promtool command-line page (`test rules`, `create-blocks-from rules` flags) and the storage page (backfill limitation). Removed: "a later rule can use the earlier one's output" (the docs say only that rules run sequentially; the backfill note says they cannot see each other there), the Thanos/Mimir downsampling-input claim and the "Status > Rules" menu path wording (now "Rules page").
Method: documentation only; no commands were run.
