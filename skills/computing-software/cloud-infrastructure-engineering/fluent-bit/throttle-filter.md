---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.throttle-filter
name: throttle-filter
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, throttle-filter, rate-limiting, leaky-bucket, sliding-window, log-flooding]
level: advanced
status: docs-checked
description: "Limit record rate with the throttle filter's rate, window and interval, which drops records above the average."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/throttle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Throttle filter

The `throttle` filter limits the average rate of messages per interval using a leaky bucket and sliding window. In a flood it leaks at a set rate and drops the excess.

| Key | Meaning |
| --- | --- |
| `rate` | number of messages allowed for the time |
| `window` | number of intervals to average over; default `5` |
| `interval` | time per interval in sleep format such as `3s`, `1.5m`, `0.5h` |
| `print_status` | log current rate and limits at info level |

```yaml
pipeline:
  filters:
    - name: throttle
      match: '*'
      rate: 5
      window: 5
      interval: 1s
      print_status: true
```

With `rate 5`, `window 5` and `interval 1s`, the filter uses a slow start to prevent flooding at startup, so you might get 1 message in the first second, 3 in the second and 5 in the third. Early averages are over the intervals seen so far, not a full window.

Once `window x interval` has elapsed it is a true sliding window. When the average over the window is above `rate`, Fluent Bit drops messages: the last pane is overwritten so the average falls back to the rate, and the extra messages are lost.

The docs warn that Fluent Bit might drop some data if the rate is ragged: use bigger intervals and rates for streams of rare but important events, and a bigger window with a smaller interval for constantly intensive inputs. For ingest-side pausing rather than dropping, see `computing-software.cloud-infrastructure-engineering.fluent-bit.input-rate-gate`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Throttle filter page: keys, window default 5, sleep-format interval, slow start (1, 3, 5), true sliding window, dropping above average, and the interval versus window guidance. Removed: an unsourced rate-setting rule.

Method: documentation only; no commands were run.
