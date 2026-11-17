---
id: computing-software.web-development.vapor.vapor-queues-setup-workers
name: vapor-queues-setup-workers
category: computing-software
field: web-development
product: vapor
tags: [vapor,queues,job,asyncjob,redis,workers,background-jobs,swift]
level: practitioner
status: docs-checked
description: "Set up Vapor Queues: add a driver package, configure it, define and register a Job, and run workers as a process or in-process."
sources:
  - https://docs.vapor.codes/advanced/queues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: offload work (emails, long database operations, delayed or scheduled tasks) to workers with Vapor Queues.

**Install a driver, not vapor/queues itself** (unless building a driver). Official: QueuesRedisDriver. Community: QueuesMongoDriver, QueuesFluentDriver.

```swift
.package(url: "https://github.com/vapor/queues-redis-driver.git", from: "1.0.0"),
// target dependency:
.product(name: "QueuesRedisDriver", package: "queues-redis-driver")
```

Run `swift package resolve` if not editing in Xcode.

**Configure** in `configure.swift`:

```swift
import QueuesRedisDriver
try app.queues.use(.redis(url: "redis://127.0.0.1:6379"))
```

**Define a job** with `Job` (futures) or `AsyncJob`. The `Payload` must be `Codable`.

```swift
struct EmailJob: AsyncJob {
    typealias Payload = Email

    func dequeue(_ context: QueueContext, _ payload: Email) async throws {
        // send the email
    }

    func error(_ context: QueueContext, _ error: Error, _ payload: Email) async throws {
        // optional; may be omitted
    }
}
```

**Register**: `app.queues.add(EmailJob())`.

**Run workers.**

- Separate process: `swift run App queues`, or one queue type: `swift run App queues --queue emails`. Keep workers running in production; on Heroku use a worker dyno, e.g. Procfile `worker: Run queues`, scaled with `heroku ps:scale worker=1`.
- In-process: `try app.queues.startInProcessJobs(on: .default)`; scheduled jobs: `try app.queues.startScheduledJobs()`.

Warning: if no worker is started (command line or in-process), jobs are not dispatched.

Troubleshooting: with a cluster-mode Redis/Valkey you may see `CROSSSLOT Keys in request don't hash to the same slot`. Fix by adding a hash tag: `app.queues.configuration.persistenceKey = "vapor-queues-{queues}"`.

Related: computing-software.web-development.vapor.vapor-queues-dispatch-retry

## Checked

2026-11-08: read in full the Queues page at docs.vapor.codes/advanced/queues/ (drivers, configuration, job protocols, registering, workers, CROSSSLOT troubleshooting). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
