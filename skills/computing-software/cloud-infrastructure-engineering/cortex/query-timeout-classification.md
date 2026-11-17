---
id: computing-software.cloud-infrastructure-engineering.cortex.query-timeout-classification
name: query-timeout-classification
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [timeouts, querier, promql, error-classification, 422]
level: advanced
status: docs-checked
description: "Classify Cortex query timeouts as user errors (422) or system errors (503) based on time spent in PromQL evaluation."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/timeout-classification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When enabled, a timed-out query that spent most of its time in PromQL evaluation returns `422 Unprocessable Entity` instead of `503 Service Unavailable`, so callers can tell an expensive query from a system fault.

How it works, for instant and range queries only: the querier subtracts time spent in the scheduler queue from the deadline, sets a proactive context timeout with the remaining budget so it cancels slightly before the PromQL engine's own timeout, and on timeout inspects phase timings (storage fetch versus total) to compute eval time. If eval time exceeds the threshold it is a user error (4XX); otherwise it stays a 5XX. When shards return at different times, the first shard to time out decides the classification.

```yaml
querier:
  timeout_classification_enabled: true
  timeout_classification_deadline: 1m59s
  timeout_classification_eval_threshold: 1m30s
```

`timeout_classification_enabled` defaults to false. The deadline defaults to `1m59s` and should be set a few seconds below the querier timeout. The eval threshold (default `1m30s`) is the eval time above which a timeout counts as a user error; it must be positive and no larger than the deadline. The deadline must be positive and strictly less than `querier.timeout`. Query stats must be enabled (`query_stats_enabled: true` on the frontend handler) or classification does not work. With `timeout_classification_enabled: false` the querier still logs the classification fields (`queue_wait_time`, `query_storage_wall_time`, `eval_time`, `decision`, `conversion_enabled`), which allows a dry run.

## Checked
Checked 2026-11-09: the 422 versus 503 behaviour, the four-step mechanism, the first-timed-out-shard rule, the three config keys, their defaults and the constraints all match the Timeout Classification guide. Added the constraints and logging notes from the same page.
Method: docs-checked 2026-11-09 against the Cortex docs page guides/timeout-classification.md, read in full as raw markdown from the repository.
