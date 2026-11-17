---
id: computing-software.messaging-and-integration.nats.reconnect-buffering
name: reconnect-buffering
category: computing-software
field: messaging-and-integration
product: nats
tags: [reconnect, reconnect-buffer, fire-and-forget, reconnectbufsize]
level: practitioner
status: docs-checked
description: "Understand client-side publish buffering during reconnect, its size limits, and why JetStream or acks are needed for delivery."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/developing-with-nats/reconnect/buffer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what happens to messages published while a client is disconnected and avoid false confidence.

Core NATS clients are fire and forget. Some libraries buffer messages published during a short reconnect and send them once the connection is back. When the maximum reconnect buffer is reached, further publishes are refused with an error. Where supported, the buffer can be sized in bytes, in messages, or both.

Go example from the page: `nats.Connect("demo.nats.io", nats.ReconnectBufSize(5*1024*1024))` sets a 5 MB buffer.

Gotchas stated by the docs:
- A publish that appeared to succeed may never reach the server if the connection is never re-established.
- Use acknowledgements at the application level or the JetStream publish call (which returns a stored-ack) when delivery matters.
- Behavior differs between client libraries; check the documentation of your language client for defaults and whether the feature exists.

Related knobs on sibling pages: disable reconnect, set maximum reconnect attempts, pause between attempts, random reconnect order (to avoid a thundering herd), and reconnect event handlers.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
