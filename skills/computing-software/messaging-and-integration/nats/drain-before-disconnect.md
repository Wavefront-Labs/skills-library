---
id: computing-software.messaging-and-integration.nats.drain-before-disconnect
name: drain-before-disconnect
category: computing-software
field: messaging-and-integration
product: nats
tags: [drain, graceful-shutdown, close, queue-subscriptions, drain-timeout]
level: practitioner
status: docs-checked
description: "Shut a NATS client down without losing in-flight messages using drain on a connection or subscription, with timeout handling."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/developing-with-nats/receiving/drain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop an application without dropping messages that are already buffered or in flight.

Close and unsubscribe are immediate: pending messages in the queue or cache are halted. Drain instead lets a subscription finish what it already has. Connection drain, per the page, does: (1) drain all subscriptions, (2) stop new publishes, (3) flush remaining published messages, (4) close. Use it in place of `close()`.

Queue groups are the key use case: bring up a new queue member, drain and stop the old one, and no messages sent to the old client are lost. Without drain, messages routed to the old client during the shutdown race can be lost. Drain can generally be done per subscription or per connection.

Go pattern: connect with `nats.DrainTimeout(10*time.Second)` plus an `nats.ErrorHandler` and a `nats.ClosedHandler`; call `nc.Drain()`, then wait on the closed handler and check the error channel. A timeout is simulated by setting `DrainTimeout` shorter than the time the message callback takes (for example 10ms).

Gotchas: if the drain timeout elapses before callbacks finish, the connection is closed with an error reported to the error handler, so size the timeout to your slowest handler.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
