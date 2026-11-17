---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-clock-skew-adjustment
name: jaeger-clock-skew-adjustment
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, max-clock-skew-adjust, clock-skew, trace-timestamps, jaeger-query-clock]
level: advanced
status: docs-checked
description: "Control how much clock-skew correction jaeger_query applies to span timestamps with max_clock_skew_adjust."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide how much Jaeger should correct host clock drift in traces.

Spans come from hosts whose hardware clocks drift. That can make a server span appear to start before its client span. The `jaeger_query` extension corrects this using causal relationships between spans. Every adjusted span shows a warning in the UI with the exact clock skew delta applied.

The adjustment can itself confuse. When Jaeger repositions a server span inside the bounds of its parent span, it does not know the exact split between request and response latency, so it assumes they are equal and places the child in the middle of the parent (issue #961).

Limit it with:
```
extensions:
  jaeger_query:
    max_clock_skew_adjust: 30s
```
Setting `0s` disables clock skew adjustment completely. The setting applies to all traces retrieved from that query service. There is an open ticket (#197) to toggle the adjustment on and off directly in the UI, so for now it is a server-side setting.

Use: if timelines look rearranged and the warnings on spans show large deltas, lower the value or set it to `0s` and compare the raw timestamps; fix NTP on the offending hosts when the deltas are large.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Configuration page, read in full (Clock Skew Adjustment section, max_clock_skew_adjust, 0s disables, issues #961 and #197). The final paragraph is practical advice, not a documented claim.

Method: documentation only; no commands were run.
