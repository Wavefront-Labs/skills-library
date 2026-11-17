---
id: computing-software.messaging-and-integration.temporal.worker-graceful-shutdown
name: worker-graceful-shutdown
category: computing-software
field: messaging-and-integration
product: temporal
tags: [worker-shutdown, graceful-shutdown, workerstoptimeout, graceful-shutdown-period, local-activities]
level: practitioner
status: docs-checked
description: "What happens to workflow tasks, activities and local activities when a Temporal Worker shuts down: graceful period settings per SDK and Go versus Core differences."
sources:
  - https://docs.temporal.io/encyclopedia/workers/worker-shutdown
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On shutdown a Worker stops polling for new tasks and starts the shutdown sequence. In-flight Workflow Tasks may fail if not completed in time, after exhausting retry attempts. An Activity can detect shutdown through its context.

Graceful shutdown sets how long the Worker may finish current work. Settings:
- Core-based SDKs: `graceful_shutdown_period`
- Go: `WorkerStopTimeout`
- Java: `shutdown()` then `awaitTermination(timeout, unit)`. By default Java Activities cannot heartbeat during graceful shutdown; `heartbeat()` throws `ActivityWorkerShutdownException` (a Java setting changes this).

During the graceful period:
- Workflow Tasks are attempted to completion; only incorrectly blocking workflow code or Local Activities delay them.
- Activities may complete.
- Local Activities in the current Workflow Task may run to completion unless the code yields. If one cannot finish by the period ending, its attempt is sent a cancel signal, no new Local Activities start or retry, and the Worker shuts down. The Worker still waits for the current Workflow Task, so you may hit a Workflow Task or execution timeout unless another Worker runs.

Non-graceful (no period, or the period elapsed): the Activity context is cancelled and shutdown finishes when the current Workflow Task ends, successfully or not. Local Activities get a cancel signal and Workflow Task heartbeats stop. If the task timeout passes while an Activity still runs, Go completes shutdown but the Activity keeps running and holds a slot, whereas Core will not finish shutdown until the Activity completes.

Guidance: make Activities and Local Activities honour context cancellation; hung Local Activities block shutdown.

## Checked

2026-11-08. Read in full: the Worker Shutdown Behavior page (docs.temporal.io/encyclopedia/workers/worker-shutdown). Every remaining claim matches those pages. Nothing removed.

Method: documentation only; no commands were run.
