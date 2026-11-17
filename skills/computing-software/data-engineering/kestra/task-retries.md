---
id: computing-software.data-engineering.kestra.task-retries
name: task-retries
category: computing-software
field: data-engineering
product: kestra
tags: [retry, maxattempts, exponential-backoff, maxduration, timeout, global-retry]
level: practitioner
status: docs-checked
description: "Configure Kestra task retries: constant, exponential and random types, maxAttempts and maxDuration, global defaults, and retry vs restart vs replay."
sources:
  - https://kestra.io/docs/workflow-components/retries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each retry creates a new attempt.

```yaml
- id: retry_sample
  type: io.kestra.plugin.core.log.Log
  message: my output for task {{ task.id }}
  timeout: PT10M
  retry:
    type: constant
    maxAttempts: 5
    interval: PT15M
```

Options:

- `type`: `constant` (fixed `interval`), `exponential` (`interval`, `maxInterval`, `delayFactor` default `2`), `random` (between `minInterval` and `maxInterval`).
- `maxAttempts`: total attempts including the first; `1` means no retry.
- `maxDuration`: total time across attempts and delays.
- `warningOnRetry`: mark the execution `WARNING` if retried (default `false`).

`timeout` limits one attempt; `maxDuration` limits all retries. Keep `interval` smaller than `maxDuration` or retries may never run. Durations are ISO 8601; weeks, months and years are unsupported.

Global default:

```yaml
kestra:
  plugins:
    configurations:
      - type: io.kestra
        values:
          retry:
            type: constant
            maxAttempts: 3
            interval: PT30S
```

Retry (task, automatic, same execution), Restart (flow, manual, same execution), Replay (new execution ID, reuses cached outputs when available).

## Checked

2026-11-04. Confirmed against "Configure Retry Strategies for Transient Task Failures" (workflow-components/retries): constant, exponential and random options and delayFactor default, maxAttempts and maxDuration semantics, warningOnRetry default, timeout versus maxDuration and interval warning, ISO 8601 limits, global configuration block, retry versus restart versus replay table. No claims removed.
Method: documentation only; no commands were run.
