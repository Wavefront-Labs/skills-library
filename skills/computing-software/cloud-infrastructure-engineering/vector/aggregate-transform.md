---
id: computing-software.cloud-infrastructure-engineering.vector.aggregate-transform
name: aggregate-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [aggregate, transform, metrics, interval, event-time, volume-reduction, vector]
level: advanced
status: docs-checked
description: "Reduce metric volume by aggregating series over an interval, optionally by event time."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/aggregate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`aggregate` combines metrics with the same series (name, namespace, tags, kind) during an `interval_ms` window (default 10000). It reduces cost and processing downstream while keeping numerical correctness. It handles metrics only (counter, distribution, gauge, histogram, set, summary).

Behaviour by kind: incremental metrics are added and newer absolute metrics replace older ones. Two incremental counters of 10 and 13 become 23; two absolute gauges of 93 and 95 become 95.

```yaml
transforms:
  agg:
    type: aggregate
    inputs: [host_metrics]
    interval_ms: 30000
    mode: Auto
```

`mode` selects the function: `Auto` (default; sums incremental, latest for absolute), `Count`, `Diff`, `Latest`, `Max`, `Mean`, `Min`, `Stdev` and `Sum`. Several apply only to one kind, and others pass the rest through unchanged.

Event-time aggregation: add an `event_time` block to bucket by each metric's timestamp instead of processing time. Buckets align to multiples of `interval_ms` from the Unix epoch. This helps sinks that key on timestamp, such as the Datadog Metrics sink, which overwrites earlier values for an identical timestamp. A watermark tracks the last emitted bucket; late events are dropped and counted in `component_discarded_events_total`. Tune lateness with `event_time.allowed_lateness_ms`, future drift with `max_future_ms` (default 10000), and `missing_timestamp` (default `drop`).

Aggregate is stateful, and state is not preserved across restarts, so the buckets in flight reset when Vector restarts.

Verify flush counts with the `aggregate_flushes_total` metric.

## Checked

2026-11-03. Read transforms/aggregate. Confirmed: the interval window and series identity, `interval_ms` default, the `mode` values and their per-kind behaviour, the 10/13 and 93/95 examples, event-time bucketing aligned to the Unix epoch, watermark and late-event drops, `max_future_ms` and `missing_timestamp` defaults, the Datadog Metrics sink note, and the `aggregate_flushes_total` metric. Reworded: the load-balancer routing advice, replaced by the documented statefulness and restart behaviour.

Method: documentation only; no commands were run.
