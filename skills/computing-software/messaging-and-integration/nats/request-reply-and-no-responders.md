---
id: computing-software.messaging-and-integration.nats.request-reply-and-no-responders
name: request-reply-and-no-responders
category: computing-software
field: messaging-and-integration
product: nats
tags: [request-reply, inbox, no-responders, 503]
level: practitioner
status: docs-checked
description: "Implement NATS request-reply with inbox reply subjects, multiple responders, and the 503 no-responders fast failure."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/core-nats/request-reply/reqreply.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use core request-reply for services and fail fast when nobody is listening.

How it works: the requester publishes on a subject with a reply subject, called an inbox, which is a unique dynamically routed subject. Responders subscribe to the request subject and publish the response to the reply subject. No sidecar or proxy is required; location of requester and responder is irrelevant.

Key behaviours from the docs:
- Several responders can form a dynamic queue group, so scaling up or down needs no registration.
- Applications should drain before exiting so buffered requests are processed and scale-down does not drop requests.
- Because it is plain pub-sub, an observer can subscribe to see requests and responses for latency and anomaly monitoring.
- Multiple responses are possible: the first is used and the extra ones are discarded, a pattern for lowering latency and jitter.

No responders: a client can opt in to `no_responders` messages (needs server and client with header support). A request to a subject with no subscribers then gets an immediate reply with no body and status `503`. Most clients surface this as an error, for example in Go `nc.Request("foo", nil, time.Second)` returns `nats.ErrNoResponders`.

Gotcha: without the no-responders opt-in, a request to an unserved subject just waits until its timeout.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
