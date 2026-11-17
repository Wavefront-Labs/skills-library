---
id: computing-software.data-engineering.kestra.server-components
name: server-components
category: computing-software
field: data-engineering
product: kestra
tags: [architecture, executor, scheduler, worker, indexer, webserver, worker-controller]
level: practitioner
status: docs-checked
description: "The Kestra server roles and what each does: webserver, executor, worker controller, worker, scheduler and indexer, plus the cluster liveness model."
sources:
  - https://kestra.io/docs/architecture/server-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- Webserver: the only role reachable from outside; serves UI and REST API, reads the Repository, submits executions via the Queue. Embeds the Indexer by default.
- Executor: drives the execution state machine (next task, state, retries, termination), flowable tasks, flow triggers, concurrency limits, SLAs, kill signals. Lightweight; scale only for very high volume.
- Worker Controller: sole link between cluster and workers, over a persistent bidirectional gRPC stream. TLS, mTLS and JWT are Enterprise features; open source uses a plaintext channel.
- Worker: runs runnable tasks and polling triggers; the only role that loads user plugins and runs user code. Scale by adding worker agents; a thread pool sits behind a bounded buffer. A system worker is embedded in the Executor or standalone server.
- Scheduler: manages all triggers except Flow triggers (Executor). Polling triggers cannot be evaluated concurrently or while a previous execution runs. Uses the system timezone by default.
- Indexer: reads from the Queue and writes to the Repository; required in all deployments. Disable the embedded one with `server webserver --no-indexer`.

Worker Groups are Enterprise only and not in Kestra Cloud.

Liveness: each server registers and sends heartbeats; the Executor's coordinator releases orphaned worker jobs back to the queue.

## Checked

2026-11-04. Confirmed against "Executor, Worker, Scheduler, Webserver, and Indexer Roles" (architecture/server-components): each role description, gRPC stream and Enterprise-only TLS/mTLS/JWT, system worker, polling trigger constraints, system timezone default, --no-indexer option, Worker Groups Enterprise-only and not in Cloud, liveness coordinator. No claims removed.
Method: documentation only; no commands were run.
