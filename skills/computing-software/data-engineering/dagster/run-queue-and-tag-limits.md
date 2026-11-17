---
id: computing-software.data-engineering.dagster.run-queue-and-tag-limits
name: run-queue-and-tag-limits
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, max-concurrent-runs, tag-concurrency-limits, apply-limit-per-unique-value, dagster-code-location, run-queue]
level: advanced
status: docs-checked
description: "Cap in-progress Dagster runs with max_concurrent_runs and tag_concurrency_limits, per tag value, per backfill, or per code location."
sources:
  - https://docs.dagster.io/guides/operate/managing-concurrency/run-queue-limits
  - https://github.com/dagster-io/dagster/blob/master/docs/docs/guides/operate/managing-concurrency/run-tag-limits.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run queue and run tag limits

Deployment-wide cap (OSS `dagster.yaml` or Dagster+ full deployment settings):
```yaml
concurrency:
  runs:
    max_concurrent_runs: 15
```

## By run tag
```yaml
concurrency:
  runs:
    tag_concurrency_limits:
      - key: 'dagster/sensor_name'
        value: 'my_cool_sensor'
        limit: 5
      - key: 'dagster/backfill'
        limit: 10
```

## Per unique value
Add `value: {applyLimitPerUniqueValue: true}` to give each distinct tag value its own limit (for example 10 runs per backfill rather than across all backfills).

## Per code location
Every run is tagged `dagster/code_location`. Use key `dagster/code_location` with `applyLimitPerUniqueValue: true` and `limit: 10` so each of `team_a`, `team_b`, `team_c` can have 10 runs in progress.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/operate/managing-concurrency/run-queue-limits
- https://github.com/dagster-io/dagster/blob/master/docs/docs/guides/operate/managing-concurrency/run-tag-limits.md

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
