---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-delivery-semantics-and-duplicate-dependencies
name: argo-events-sensor-delivery-semantics-and-duplicate-dependencies
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, delivery-guarantee, exactly-once, at-least-once, duplicate-dependencies, ordering, nats-streaming, jetstream]
level: advanced
status: docs-checked
description: "Know what the Sensor guarantees about event order, duplicates and repeated dependencies on each EventBus type."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/more-about-sensors-and-triggers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor delivery semantics and duplicate dependencies

Delivery guarantees:
- NATS Streaming offers at-least-once delivery. JetStream adds features that get closer to exactly-once.
- The Sensor keeps an in-memory cache of event IDs delivered in the last 5 minutes to drop duplicates. With that, delivery is exactly-once in almost all cases (not when pods die while processing) and at-least-once in all cases.

Ordering (per the NATS Streaming description): events normally arrive in publish order but there is no guarantee. If the Sensor fails to acknowledge message one and acknowledges message two before one is redelivered, order flips.

Multiple dependencies: for `A && B`, when the condition becomes true the latest event from each dependency is used and older ones are dropped.

Duplicate dependencies: on the NATS Streaming bus the same `eventSourceName` plus `eventName` combination cannot be referenced twice in one Sensor, even with different filters (for example one dependency with `body.value < 20` and another with `> 50`). Reference it from separate Sensor objects instead. This restriction does not apply to the JetStream bus.

## Checked

2026-11-04. Confirmed against the More About Sensors And Triggers page: multiple dependencies and the `A && B` example, the duplicate-dependency restriction on the NATS Streaming bus with the `body.value` example and the separate-Sensor workaround, no issue for JetStream, delivery order, and the delivery guarantee with the 5-minute event ID cache. Removed the closing advice on trigger idempotency, which the page does not give. The "cannot be referenced twice" rule is stated for the NATS Streaming bus only.
Method: documentation only; no commands were run.
