---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.adaptive-flush-intervals
name: adaptive-flush-intervals
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, flush-adaptive, backpressure, flush-interval, tuning]
level: advanced
status: docs-checked
description: "Let Fluent Bit shorten or lengthen its flush interval with chunk backpressure using the flush.adaptive keys."
sources: ["https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/service-section"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adaptive flush intervals

Adaptive flush intervals are available in Fluent Bit version 5.1 and greater. A fixed `flush` is a trade-off: short keeps latency low but wastes cycles when idle; long delays delivery under load. Setting `flush.adaptive: on` (default `off`) makes Fluent Bit sample the highest chunk backpressure percentage across all inputs and scale `flush`:

| Sample | Interval |
| --- | --- |
| at or above `flush.adaptive.high_pressure` (`75`) | `flush` x 0.5 |
| at or above `flush.adaptive.medium_pressure` (`50`) | `flush` x 0.75 |
| above `flush.adaptive.low_pressure` (`25`) | `flush` unchanged |
| at or below the low threshold | `flush` x 2 |

The result is clamped between `flush.adaptive.min_interval` (`0.5`) and `flush.adaptive.max_interval` (`2`), which take precedence over the multipliers.

To stop oscillation, a change needs repeated samples: `flush.adaptive.up_steps` (`2`) consecutive samples to move to higher pressure, `flush.adaptive.down_steps` (`3`) to move lower. A sample matching the current level resets the count.

```yaml
service:
  flush: 1.5
  flush.adaptive: on
  flush.adaptive.min_interval: 0.5
  flush.adaptive.max_interval: 3
  flush.adaptive.high_pressure: 80
```

This flushes every 1.5 seconds normally, 0.75 seconds at 80 percent backpressure, and backs off to at most 3 seconds when idle.

## Checked

2026-11-03. Confirmed on the Fluent Bit YAML Service section page (Adaptive flush intervals): the 5.1 availability, defaults and multipliers, clamping, up_steps and down_steps, and the 1.5 s / 80 percent example. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
