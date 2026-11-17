---
id: computing-software.cloud-infrastructure-engineering.vector.throttle-transform
name: throttle-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [throttle, transform, rate-limit, quotas, key-field, gcra, vector]
level: practitioner
status: docs-checked
description: "Rate limit log streams per key with the throttle transform and read its quota semantics."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/throttle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`throttle` rate limits one or more log streams to protect downstream services or enforce quotas. It is stable, stateful and handles logs only. State resets on restart.

```yaml
transforms:
  limit:
    type: throttle
    inputs: [logs]
    threshold: 100
    window_secs: 1.0
    key_field: "{{ service }}"
    exclude: '.severity == "error"'
```

Options: `threshold` (events allowed per bucket per window) and `window_secs` are required; `key_field` is a template that places events in separate buckets limited independently (omit it for a single bucket); `exclude` is a condition for events that bypass limiting.

How it works: the transform uses a Generic Cell Rate Algorithm, spreading load across the window. Each event consumes a cell. A limiter holds up to `threshold` cells, replenished at one per `window_secs / threshold`. For `window_secs: 60` and `threshold: 10` a cell returns every 6 seconds and a burst of up to 10 events is allowed.

When a bucket is at capacity, extra events are discarded and counted in `events_discarded_total`, tagged by the bucket key. Per-key emission of that metric is opt-in through `internal_metrics.emit_events_discarded_per_key` (default false), because high-cardinality keys create many series.

Compare with `sample`: throttle bounds throughput, sample reduces by proportion.

Verify the discard metric rises only for the noisy key under a load test.

## Checked

2026-11-03. Read transforms/throttle. Confirmed: stable, stateful, logs only; `threshold`, `window_secs`, `key_field`, `exclude`; Generic Cell Rate Algorithm with the 60-second, threshold-10 worked example; `events_discarded_total` tagged by bucket key; and `internal_metrics.emit_events_discarded_per_key` default false because of cardinality. Nothing removed.

Method: documentation only; no commands were run.
