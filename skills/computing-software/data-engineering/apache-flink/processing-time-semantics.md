---
id: computing-software.data-engineering.apache-flink.processing-time-semantics
name: processing-time-semantics
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-processing-time, processing-time, event-time, timers, windows]
level: practitioner
status: docs-checked
description: "Use processing time in Flink deliberately: processing-time windows and timers, their non-determinism on replay, and when it is the right choice over event time."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/time/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/windows/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/execution_mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Processing-time semantics

Processing time = the wall clock of the TaskManager when the operator handles the record. No watermarks, no late data, lowest latency, and results that depend on when the job ran.

## Using it
```java
stream.keyBy(Event::key)
      .window(TumblingProcessingTimeWindows.of(Duration.ofMinutes(1)))
      .aggregate(new CountAgg());
// timers
ctx.timerService().registerProcessingTimeTimer(ctx.timerService().currentProcessingTime() + 60_000);
```
SQL: declare `proc AS PROCTIME()` as a computed column and window on it: `TUMBLE(TABLE t, DESCRIPTOR(proc), INTERVAL '1' MINUTE)`.
Processing-time windows are chosen explicitly through the assigner type (`TumblingProcessingTimeWindows`) rather than a global time characteristic.

## When it is right
- Monitoring/alerting on "what arrived in the last minute" where arrival time is the question.
- Timeouts that relate to wall-clock (session expiry for live users, retry delays, flushing buffers every N seconds).
- Sources without trustworthy timestamps, where approximate results are acceptable.

## When it is wrong
- Anything that must be reproducible or correct on replay/backfill: processing-time results depend on when records are processed, so a fast replay packs a long span of data into few windows.
- Results after downtime or backpressure: records that queued up land in the window when they are processed, not when they happened.
- Joins between streams with different latency.

## Behaviour details
- Processing-time timers fire on wall-clock even without new records; event-time timers need watermarks.
- On restore from a checkpoint/savepoint, processing-time timers whose time already passed fire immediately (a burst after downtime).
- In BATCH execution mode processing time does not advance during the job; processing-time timers fire at the end of the input.
- Windows are aligned to the epoch; the window offset argument adjusts alignment (for example the windows docs use `TumblingEventTimeWindows.of(Duration.ofDays(1), Duration.ofHours(-8))` to adapt daily windows to a time zone other than UTC).

## Hybrid
Event-time windows can use a custom trigger to emit early partial results before the final event-time result.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Timely Stream Processing page (processing time is the machine's system clock; no watermarks), the windows page (processing-time assigners, offsets, triggers), the DataStream execution mode page (processing-time timers fire at the end in BATCH mode) and the ProcessFunction page (due processing-time timers fire immediately on restore). Removed the unconfirmed version history and replay arithmetic.

Method: documentation only; no commands were run.

## Verify
- [ ] Documented why processing time is acceptable for this output.
- [ ] Replay test shows the expected (different) results, and consumers know about it.
