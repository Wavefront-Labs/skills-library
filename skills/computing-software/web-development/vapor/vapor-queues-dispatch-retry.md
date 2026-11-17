---
id: computing-software.web-development.vapor.vapor-queues-dispatch-retry
name: vapor-queues-dispatch-retry
category: computing-software
field: web-development
product: vapor
tags: [vapor,queues,job,dispatch,maxretrycount,delayuntil,queuename,testing,swift]
level: advanced
status: docs-checked
description: "Dispatch Vapor Queues jobs with retries, delays and named queues, observe them with JobEventDelegate, and test with the async test driver."
sources:
  - https://docs.vapor.codes/advanced/queues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: dispatch jobs with retry, delay and priority, monitor them, and test them.

**Dispatch** from a request (`req.queue`) or, without a request (e.g. in a command), from `context.application.queues.queue`:

```swift
try await req.queue.dispatch(
    EmailJob.self,
    .init(to: "email@email.com", message: "message"))
```

**Retries**: `maxRetryCount: 3` makes the job retry itself on error.

**Delay**: `delayUntil: Date` (e.g. `Date(timeIntervalSinceNow: 60 * 60 * 24)`). If a job is dequeued before that date, the driver re-queues it.

```swift
try await req.queue.dispatch(EmailJob.self, .init(to: "email@email.com", message: "message"),
    maxRetryCount: 3, delayUntil: futureDate)
```

**Named queues / priority.** Extend `QueueName`, optionally with a per-queue `workerCount` (`1` processes jobs consecutively, useful when order matters):

```swift
extension QueueName {
    static let emails = QueueName(string: "emails")
    static let serialEmails = QueueName(string: "serial-emails", workerCount: 1)
}
try await req.queues(.emails).dispatch(EmailJob.self, payload)
// from Application: app.queues.queue(.emails).dispatch(...)
```

Without a queue name the job runs on `default`. Start workers for each queue type (`swift run App queues --queue emails`).

**Event delegates.** Conform to `JobEventDelegate` (`dispatched(job:eventLoop:)`, `didDequeue(jobId:eventLoop:)`, `success(jobId:eventLoop:)`, `error(jobId:error:eventLoop:)`) and register with `app.queues.add(MyEventDelegate())`. Third-party users of this: QueuesDatabaseHooks, QueuesDash.

**Testing.** Use the testing driver for deterministic tests: after `Application.make(.testing)` and `configure(app)`, call `app.queues.use(.asyncTest)`; shut down with `asyncShutdown()`. The docs cite the `XCTQueue` library for this.

Related: computing-software.web-development.vapor.vapor-queues-setup-workers

## Checked

2026-11-08: read in full the Queues page at docs.vapor.codes/advanced/queues/ (dispatch, maxRetryCount, delayUntil, QueueName and workerCount, JobEventDelegate, testing). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
