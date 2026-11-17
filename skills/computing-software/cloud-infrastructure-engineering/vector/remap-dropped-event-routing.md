---
id: computing-software.cloud-infrastructure-engineering.vector.remap-dropped-event-routing
name: remap-dropped-event-routing
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [remap, dropped-events, reroute-dropped, error-handling, durability, backup, vector]
level: advanced
status: docs-checked
description: "Route events that fail remap processing to a backup sink with reroute_dropped."
sources:
  - https://vector.dev/docs/setup/going-to-prod/high-availability/
  - https://vector.dev/docs/reference/configuration/transforms/remap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Data processing failures, such as a VRL program that aborts, can be mitigated with dropped-event routing. A `remap` transform has a `dropped` output that sends dropped events through another pipeline instead of discarding them. The docs recommend routing them immediately to a backup destination to prioritise durability; after persisting them you can inspect, fix the error and replay.

The documented example sends failures from the `parsing` transform to S3:

```yaml
sources:
  input:
    type: datadog_agent
transforms:
  parsing:
    inputs: [input]
    type: remap
    reroute_dropped: true
    source: "..."
sinks:
  analysis:
    inputs: [parsing]
    type: datadog_logs
  backup:
    inputs: [parsing.dropped]
    type: aws_s3
```

Key points:

- Set `reroute_dropped: true` on the transform.
- Reference the dropped output as `<transform>.dropped` in a downstream component's `inputs`.
- Dropped events can be routed like any other event.

Limit stated in the docs: support for dropped channels in other components is forthcoming, so only rely on this for `remap`.

Related defaults from the remap reference: `drop_on_abort` is true and `drop_on_error` is false (an event whose program errors passes on unmodified). `reroute_dropped` forwards the original event, annotated with why it was dropped, to the `dropped` output.

Verify by sending a deliberately malformed event and confirming it lands in the backup sink.

## Checked

2026-11-03. Read setup/going-to-prod/high-availability and transforms/remap. Confirmed: the dropped output channel, the recommendation to route to a backup destination then inspect, fix and replay, the documented datadog_agent to aws_s3 example, the note that other components' dropped channels are forthcoming, and the `drop_on_abort`/`drop_on_error` defaults and `reroute_dropped` annotation. Reworded: the filter/tag/multiple-sink claim to the page's 'like any other event'.

Method: documentation only; no commands were run.
