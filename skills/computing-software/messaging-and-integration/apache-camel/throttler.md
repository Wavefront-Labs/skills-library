---
id: computing-software.messaging-and-integration.apache-camel.throttler
name: throttler
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, throttle, rate-limiting, concurrency]
level: practitioner
status: docs-checked
description: "Camel Throttle EIP: TotalRequests vs ConcurrentRequests modes, timePeriodMillis 1000 default, asyncDelayed, rejectExecution, correlationExpression groups and dynamic limits."
sources:
  - https://camel.apache.org/components/next/eips/throttle-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throttle

The limit comes from the required `expression` (converted to a Long). Options (defaults):
- `mode` `TotalRequests` (limit per window) or `ConcurrentRequests` (leaky bucket, limits simultaneous processing)
- `timePeriodMillis` 1000
- `asyncDelayed` false (true delays through a scheduler without blocking the caller)
- `rejectExecution` false (true throws `ThrottlerRejectedExecutionException`)
- `callerRunsWhenRejected` true
- `correlationExpression` none (all messages share one group)
- `executorService` a `ScheduledExecutorService`

By default it waits for free capacity; the body is unchanged. If a header-based expression yields no value, the previous limit is kept.

```java
throttle(3).timePeriodMillis(10000)
throttle(50)
throttle(header("throttleValue")).timePeriodMillis(500)
throttle(100).asyncDelayed()
throttle(100).rejectExecution(true)
throttle(100).correlationExpression(header("region"))
throttle(3).concurrentRequestsMode()
```

`throttle(50)` means 50 messages per second. The correlation form throttles each region separately.

Verify: `throttle(3).timePeriodMillis(10000)` sends at most 3 messages to the next step in a running 10-second window; by default the rest wait for free capacity rather than being dropped.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Throttle EIP page: mode values and default, timePeriodMillis 1000, asyncDelayed false, rejectExecution false and the exception name, callerRunsWhenRejected true, correlationExpression grouping, executorService type, header-absent behaviour, unchanged body and all DSL examples match. The old verify line (3 of 10 through) was reworded to what the page states. No commands were run.
