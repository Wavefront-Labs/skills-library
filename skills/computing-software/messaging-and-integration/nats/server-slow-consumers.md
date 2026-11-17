---
id: computing-software.messaging-and-integration.nats.server-slow-consumers
name: server-slow-consumers
category: computing-software
field: messaging-and-integration
product: nats
tags: [slow-consumer, varz, slow-consumers-count, outbound-buffer, error-handler]
level: practitioner
status: docs-checked
description: "Detect and handle slow consumers on the server: log message, varz slow_consumers counter, client ErrSlowConsumer handler."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/slow_consumers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: recognise, count and respond to slow consumers in core NATS.

Definition: a subscriber that cannot keep up with the message flow. NATS protects the system as a whole over any one consumer.

Client detection: the library drops messages for that subscription and notifies the app through the async error callback. Go pattern: register `nats.ErrorHandler(func(nc *nats.Conn, sub *nats.Subscription, err error) {...})`, check `natsErr == nats.ErrSlowConsumer`, and read `sub.Pending()`. Default settings produce `error: nats: slow consumer, messages dropped` and `Falling behind with 65536 pending messages on subject "foo"`. Synchronous subscribers get the error from `Subscription.NextMsg(timeout)`.

Server detection: the server buffers outbound data per connection. If it cannot write fast enough it marks the consumer slow and may drop data or close the connection. The log shows `Slow Consumer Detected` for that client id, and the monitoring `varz` endpoint exposes a `slow_consumers` counter.

Handling: catch slow consumers in the client first (better than losing the connection); scale out with queue groups; throttle publishers; and for guaranteed delivery use JetStream consumers, which track acknowledgements instead of dropping.

Gotcha: client-side buffering only masks short bursts; sustained overload still ends with drops or disconnects.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
