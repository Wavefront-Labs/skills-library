---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-multiple-collectors-faq
name: jaeger-multiple-collectors-faq
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, collector-high-availability, dropped-spans, rolling-restart, multiple-collectors]
level: practitioner
status: docs-checked
description: "Know when running multiple Jaeger collectors helps (throughput, availability) and when it does not (data loss from slow storage)."
sources:
  - https://www.jaegertracing.io/docs/2.22/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide whether to add collectors.

Reasons to run multiple instances:
- Clients send more data than one collector can accept fast enough.
- Higher availability, for example rolling restarts for upgrades while some instances keep processing inbound data.

Not a reason:
- Avoiding data loss. Jaeger drops data when the storage cannot save it fast enough. More collector instances, with more memory in their internal queues, give small, temporary relief but do not remove the storage bottleneck.

## Checked

2026-11-08: read the whole FAQ (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed both lists. Removed unsupported claims: the stateless-components and upgrade-order deployment notes.

Method: documentation only; no commands were run.
