---
id: computing-software.software-engineering.deno.cron-schedule-jobs
name: cron-schedule-jobs
category: computing-software
field: software-engineering
product: deno
tags: [cron, deno-cron, scheduling, backoff, unstable, opentelemetry]
level: practitioner
status: docs-checked
description: "Schedule recurring work with Deno.cron: cron expressions or object schedules, UTC times, backoffSchedule retries, top-level registration and the unstable flag."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/cron.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Deno.cron(name, schedule, handler)` is unstable: run with `--unstable-cron` (or add `"cron"` to the `unstable` array in deno.json). All times are UTC.

```ts
Deno.cron("log-a-message", "* * * * *", () => {
  console.log("This runs once a minute.");
});
```

Fields: minute (0-59), hour (0-23), day of month (1-31), month (1-12 or JAN-DEC), day of week (0-6 or SUN-SAT, 0 is Sunday). Each takes a value, `*`, range `1-5`, list `1,3,5` or step `*/15`. `0 9 * * MON-FRI` is 09:00 UTC on weekdays. Object form:

```ts
Deno.cron("hourly-task", { hour: { every: 1 } }, () => {});
```

Register jobs at module top level, before any server starts; definitions inside handlers, conditionals or callbacks are not picked up.

Failed runs are not retried by default. Add `backoffSchedule` (millisecond delays):

```ts
Deno.cron("retry-example", "* * * * *", { backoffSchedule: [1000, 5000, 10000] }, () => {
  throw new Error("Will be retried up to three times.");
});
```

State is in memory per CLI process; Deno Deploy discovers definitions, schedules, retries and shows runs. With `OTEL_DENO=true` each invocation produces a span named after the job.

## Checked

2026-11-04. Confirmed against docs runtime/fundamentals/cron.md: --unstable-cron or unstable array, UTC, field ranges, expression forms, object schedule, top-level registration, no default retry, backoffSchedule, in-memory state, Deploy behaviour, OTel span.

Method: documentation only; no commands were run.
