---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.input-rate-gate
name: input-rate-gate
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, rate-gate, rate-window, input-throttling, max-bytes, max-records]
level: advanced
status: docs-checked
description: "Pause an input when its byte or record rate exceeds a limit, using rate_gate and resume_ratio hysteresis."
sources: ["https://docs.fluentbit.io/manual/pipeline/buffering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Input rate gate

Rate gate is available in Fluent Bit version 5.1 and greater. Per-input rate gating pauses ingestion when an input exceeds byte or record rate limits. Keys, all set on the input:

| Key | Default | Meaning |
| --- | --- | --- |
| `rate_gate` | `false` | enable the gate |
| `rate_gate.max_bytes` | `0` | bytes per second before pausing, unit-size syntax; `0` means no limit |
| `rate_gate.max_records` | `0` | records per second before pausing; `0` means no limit |
| `rate_gate.resume_ratio` | `0.80` | hysteresis: measured rate must fall under this ratio of the limits before resuming |
| `rate_gate.backpressure` | `true` | factors retry and busy-chunk pressure into the effective limit |
| `rate_window` | `1s` | time window used to compute the rate; the published rate is always per second |

If both limits are set, both measured rates must fall under their resume thresholds before ingestion resumes, whichever limit triggered the pause.

```yaml
pipeline:
  inputs:
    - name: forward
      rate_window: 1s
      rate_gate: true
      rate_gate.max_bytes: 5M
      rate_gate.max_records: 10000
      rate_gate.resume_ratio: 0.80
```

This pauses above 5 MB per second or 10,000 records per second and resumes once both rates fall back to 80 percent of their limits.

This differs from `mem_buf_limit`, which limits the memory an input can use for buffered data rather than the ingest rate. The `throttle` filter instead drops records above an average rate (see `computing-software.cloud-infrastructure-engineering.fluent-bit.throttle-filter`).

## Checked

2026-11-03. Confirmed on the Fluent Bit Buffering page (Per-input settings): all rate_gate keys and defaults, rate_window, resume_ratio behaviour, 5.1 availability, and the forward example. Removed: the claim that throttle limits by tag.

Method: documentation only; no commands were run.
