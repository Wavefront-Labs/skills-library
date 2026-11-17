---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.scheduler-backoff
name: scheduler-backoff
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, scheduler, retry, exponential-backoff, scheduler-base, scheduler-cap, jitter]
level: practitioner
status: docs-checked
description: "Compute Fluent Bit's retry wait time from scheduler.base and scheduler.cap using exponential backoff with jitter."
sources: ["https://docs.fluentbit.io/manual/administration/scheduling-and-retries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scheduler backoff

When an output flushes data it returns `OK`, `Retry` or `Error`. On `Retry` the scheduler decides how long to wait; `Error` is unrecoverable and the data is not retried.

Two service keys (supported in v1.8.7 or later) set the wait:

| Key | Default | Meaning |
| --- | --- | --- |
| `scheduler.base` | `5` | base of the exponential backoff, the lower bound |
| `scheduler.cap` | `2000` | maximum retry wait in seconds, the upper bound |

Fluent Bit uses exponential backoff with jitter. For the Nth retry the wait is a random number between `base` and `min(base * 2^N, cap)`.

Example with `scheduler.base: 3` and `scheduler.cap: 30`:

| Retry | Wait range (seconds) |
| --- | --- |
| 1 | 3 to 6 |
| 2 | 3 to 12 |
| 3 | 3 to 24 |
| 4 | 3 to 30 |

```yaml
service:
  flush: 5
  scheduler.base: 3
  scheduler.cap: 30
```

Retry counts per output are covered in `computing-software.cloud-infrastructure-engineering.fluent-bit.retry-limit`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Scheduling and retries page: OK, Retry and Error statuses, scheduler.base and scheduler.cap defaults and v1.8.7 support, the backoff-with-jitter bounds, and the base 3 / cap 30 wait table. Removed: unsourced tuning advice and verification step.

Method: documentation only; no commands were run.
