---
id: computing-software.cloud-infrastructure-engineering.vector.adaptive-request-concurrency
name: adaptive-request-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [arc, concurrency, http, rate-limit, congestion-control, sinks, vector]
level: advanced
status: docs-checked
description: "Let Vector tune HTTP request concurrency automatically instead of using a static rate limit."
sources:
  - https://vector.dev/docs/architecture/arc/
  - https://vector.dev/docs/setup/going-to-prod/high-availability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Adaptive Request Concurrency (ARC) is a Vector networking feature that replaces static rate limits with automatically optimised HTTP concurrency limits. The mechanism is a feedback loop based on downstream service responses, inspired by TCP congestion control algorithms. The documented outcome is better performance and reliability across your observability infrastructure.

On the high-availability page, ARC is the mitigation for data send failures: it automatically scales down the number of outgoing connections when Vector cannot send data, which minimises in-flight data, applies backpressure appropriately and prevents the stampede effect that stops downstream services recovering. It is paired there with buffers, which absorb backpressure when a service cannot accept data and replay it on recovery.

How to approach it:

1. Prefer ARC over hand-tuned static concurrency or rate limits on HTTP-based sinks.
2. Look up the exact request and concurrency options on each sink's reference page; the architecture page does not list them.
3. Pair ARC with a sensible buffer policy (see backpressure-and-buffer-basics) so that, when ARC lowers concurrency, events wait in the buffer instead of being dropped.

The architecture page itself is brief and links to a feature announcement titled "Adaptive request concurrency. Resilient observability at scale."

Verify by slowing the destination in a test and observing that Vector reduces its outgoing load and applies backpressure rather than flooding the destination.

## Checked

2026-11-03. Read the Vector pages 'Adaptive request concurrency (ARC)' (architecture/arc) and 'High Availability' (setup/going-to-prod/high-availability). Confirmed: ARC replaces static rate limits with automatically optimised HTTP concurrency limits, driven by a feedback loop on downstream responses and inspired by TCP congestion control; and that it scales down outgoing connections when Vector cannot send. Removed: the `request.concurrency` values, `request.adaptive_concurrency.*` option names and the `max_concurrency_limit` default (neither page lists them; see each sink's reference page), and the `vector top` verification.

Method: documentation only; no commands were run.
