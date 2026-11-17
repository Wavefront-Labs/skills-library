---
id: computing-software.web-development.vapor.vapor-queues-scheduled-jobs
name: vapor-queues-scheduled-jobs
category: computing-software
field: web-development
product: vapor
tags: [vapor, queues, scheduledjob, scheduling, cron, swift, background-jobs]
level: advanced
status: docs-checked
description: "Schedule recurring Vapor Queues jobs with ScheduledJob, calendar and every() builders, and run the scheduler worker."
sources:
  - https://docs.vapor.codes/advanced/queues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run a job on a calendar or fixed-interval schedule using the Vapor Queues package.

## Define the job
Conform to `ScheduledJob` (futures) or `AsyncScheduledJob` (async/await). Extra services can be injected as properties.

```swift
struct CleanupJob: AsyncScheduledJob {
    func run(context: QueueContext) async throws {
        // Do some work here, perhaps queue up another job.
    }
}
```

The future version is `func run(context: QueueContext) -> EventLoopFuture<Void>`, e.g. returning `context.eventLoop.makeSucceededFuture(())`.

## Register it
Register in `configure.swift`. Scheduled jobs only work when set up before the app boots; they do not work in route handlers.

```swift
app.queues.schedule(CleanupJob())
    .yearly()
    .in(.may)
    .on(23)
    .at(.noon)
```

That runs every year on 23 May at 12:00 PM. The scheduler uses the server's timezone.

## Calendar builders
Keep chaining until the compiler stops warning about an unused result.

| Start | Modifiers |
|-|-|
| `yearly()` | `in(_ month)` then Monthly |
| `monthly()` | `on(_ day)` then Daily |
| `weekly()` | `on(_ weekday)` then Daily |
| `daily()` | `at(_ time)`, `at(_ hour: Hour24, _ minute)`, `at(_ hour: Hour12, _ minute, _ period)` (final) |
| `hourly()` | `at(_ minute)` (final) |
| `minutely()` | `at(_ second)` (final) |

Helper values: months `.january`...; days `.first`, `.last`, `.exact(1)`; weekdays `.sunday`...; times `.midnight`, `.noon`. Examples: `.yearly().in(.january)`, `.monthly().on(.first)`, `.weekly().on(.sunday)`, `.daily().at(.midnight)`.

## Interval builders
`every(seconds:)`, `every(minutes:)`, `every(hours:)`, `every(days:)`, `every(weeks:)` (all take an `Int`).

```swift
app.queues.schedule(CleanupJob())
    .every(hours: 6)
```

## Run the scheduler
The scheduler needs its own worker, like the queue worker:

```sh
swift run App queues --scheduled
```

Or in-process: `try app.queues.startScheduledJobs()`. If no worker is started, jobs will not dispatch. In production keep the worker alive (Heroku Procfile example: `worker: App queues --scheduled`).

## Checked

2026-11-08: read in full the Queues page at docs.vapor.codes/advanced/queues/ (ScheduledJob, calendar and every() builders, helper enums, scheduler worker). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
