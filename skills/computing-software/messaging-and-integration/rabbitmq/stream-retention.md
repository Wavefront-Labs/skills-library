---
id: computing-software.messaging-and-integration.rabbitmq.stream-retention
name: stream-retention
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, stream-retention]
level: practitioner
status: docs-checked
description: "Bound stream disk use with max-age and max-length-bytes policies applied per segment."
sources:
  - https://www.rabbitmq.com/docs/streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream retention

**Goal:** Prevent unbounded stream growth.

## Steps
1. Set `max-age` (units Y, M, D, h, m, s; for example `7D`) and/or `max-length-bytes`. They can be combined, set as queue arguments (`x-max-age`, `x-max-length-bytes`) at declaration or as a policy; the policy takes precedence.
2. Retention is evaluated per segment. Segment size is the `x-stream-max-segment-size-bytes` argument (default 500000000 bytes). Set it as a queue argument: a policy value is applied only if the policy exists when the stream is declared.
3. The stream always leaves at least one segment in place as long as that segment holds at least one message.

## Failure modes
- Because retention works on whole segments, a large segment size makes truncation coarse.
- With neither limit set the log grows until the disk is full.

## Verify
- `rabbitmq-streams stream_status [-p <vhost>] <stream>`.

## Checked

Date: 2026-11-02. Confirmed on the Streams guide: retention parameters and units, policy precedence, per-segment evaluation, the one-segment rule, segment-size default and policy caveat, `stream_status`. Removed as not stated there: the claim that old segments are deleted once a new segment exists, and watching disk usage as a check.

Method: documentation only; no commands were run.
