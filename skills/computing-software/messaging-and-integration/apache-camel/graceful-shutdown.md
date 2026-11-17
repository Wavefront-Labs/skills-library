---
id: computing-software.messaging-and-integration.apache-camel.graceful-shutdown
name: graceful-shutdown
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, shutdown, lifecycle, timeout, in-flight-exchanges]
level: practitioner
status: docs-checked
description: "Camel graceful shutdown: 45 second default timeout, reverse start order, ShutdownRoute and ShutdownRunningTask options, timeout logging and stopping single routes."
sources:
  - https://camel.apache.org/manual/graceful-shutdown.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Graceful shutdown

`DefaultShutdownStrategy` (implements `org.apache.camel.spi.ShutdownStrategy`) lets in-flight exchanges finish. Routes stop in reverse start order. Default timeout is 45 seconds; after it Camel forces a hard shutdown (behaviour can be set to force or ignore).

Logging on timeout:
- `camel.main.shutdownSuppressLoggingOnTimeout = true` hides rejected-exchange warnings.
- `camel.main.shutdownLogInflightExchangesOnTimeout = false` turns off the in-flight dump (exchange id, source route, current node, durations).
- DEBUG on `DefaultShutdownStrategy` logs the same during a normal shutdown.

Fine-grained options, at context or route level (route wins):
- `ShutdownRoute`: `Default` (stop early) or `Defer` (postpone; for internal routes other routes depend on).
- `ShutdownRunningTask`: `CompleteCurrentTaskOnly` (default) or `CompleteAllTasks` (for batch consumers, e.g. finish all picked-up files).

Single routes: `stopRoute(routeId)` is graceful. `stopRoute(routeId, cause)` marks the route failed, so health checks report DOWN; a manually stopped route reports UNKNOWN.

Custom consumers can implement `ShutdownAware` (`getPendingExchangesSize`, `deferShutdown`) so shutdown waits for in-memory queues such as SEDA.

Verify: stopping the context while an exchange is mid-route lets it complete, or logs it as in-flight once 45 seconds elapse.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel graceful shutdown manual page: 45 second default timeout, reverse start order, force-or-ignore on timeout, both camel.main property names and their Java setters, DEBUG logging on DefaultShutdownStrategy, ShutdownRoute Default and Defer, ShutdownRunningTask CompleteCurrentTaskOnly and CompleteAllTasks, context versus route precedence, stopRoute with and without a cause, DOWN versus UNKNOWN health status and the ShutdownAware methods all match. No commands were run.
