---
id: computing-software.messaging-and-integration.dapr.jobs-api-scheduling
name: jobs-api-scheduling
category: computing-software
field: messaging-and-integration
product: dapr
tags: [jobs, scheduler, cron, schedule, duration, rfc3339, at-least-once, etcd, repeats]
level: practitioner
status: docs-checked
description: "Schedule Dapr jobs with six-field cron, Go durations, @every expressions or RFC3339 dates; names overwrite and execution is at least once."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/jobs/jobs-overview.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/jobs/jobs-features-concepts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The jobs API schedules work in the future, once or repeatedly. It is a scheduler, not an executor: at trigger time Dapr sends a message back to the app that scheduled the job (HTTP or gRPC, whichever the app registered), and your handler runs the work.

Guarantees: at least once execution, biased to durability and horizontal scaling over precision. A job is never invoked before its schedule time; there is no ceiling on how late it may be invoked. Job details and user data live in the embedded Etcd database of the Scheduler service, which also schedules actor reminders.

Identity: job names are case sensitive and unique across services using the runtime. Creating a job with an existing name overwrites it and resets its count, so multiple replicas can schedule the same job at startup safely. The Scheduler ensures a job is triggered by only one Scheduler instance.

Schedule options:

- Cron with six fields: seconds, minutes, hours, day of month, month, day of week. `"0 30 * * * *"` is every hour on the half hour; `"0 15 3 * * *"` is daily at 03:15.
- Go duration strings with units ns, us, ms, s, m, h: `"2h45m"`, `"37m25s"`.
- Period expressions: `@every 1h30m`, `@yearly` or `@annually`, `@monthly`, `@weekly`, `@daily` or `@midnight`, `@hourly`.
- A specific time in RFC3339: `"2025-12-09T16:09:53+00:00"`.

Time zone: a zone in the RFC3339 timestamp is used; otherwise the server running Dapr decides. Do not assume UTC.

## Checked

Delivery guarantees, name overwrite rule, single-Scheduler trigger, schedule formats and time zone rule confirmed on the Jobs overview and features pages. The Go SDK `Repeats` example was dropped because neither page shows it.

Method: docs-checked 2026-11-09 against raw v1.15 jobs-overview.md and jobs-features-concepts.md (both read in full); no commands were run.
