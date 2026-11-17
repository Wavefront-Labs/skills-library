---
id: computing-software.data-engineering.streaming-architecture.windowing-and-time-semantics
name: windowing-and-time-semantics
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, windowing, tumbling-window, sliding-window, session-window, global-window, watermark, allowed-lateness, event-time, processing-time, trigger-policy, late-data-handling]
level: advanced
status: draft
description: "Pick the correct window type (tumbling/sliding/session) and time semantics (event time vs processing time) for a streaming aggregation, engine-agnostic."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/
  - https://beam.apache.org/documentation/programming-guide/#windowing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windowing and time semantics — the engine-agnostic model

**Goal:** pick the window shape and time semantics that match the actual business question, independent of whether the engine is Flink, Spark Structured Streaming, Kafka Streams or Beam — the concepts (and their failure modes) are the same across all of them. See computing-software.data-engineering.apache-flink.event-time-watermarks-and-checkpoints for Flink-specific watermark mechanics this generalizes from.

## 1. Window types — match the shape to the question
- **Tumbling** (fixed-size, non-overlapping: "every 5 minutes"): each event belongs to exactly one window. Right for periodic rollups ("orders per hour") where double-counting across windows would be wrong.
- **Sliding** (fixed-size, overlapping, advancing by a smaller step than the window size: "5-minute window, every 1 minute"): each event contributes to multiple overlapping windows. Right for "trailing N-minute rate" style metrics (a moving average, a rolling rate limit check) where you want a smoothed, continuously-updating view rather than discrete buckets — but every event is now processed once per overlapping window, multiplying compute cost roughly by (window size / slide interval).
- **Session** (dynamic size, closes after a gap of inactivity: "group clicks into a session, closed after 30 min idle"): the only window type whose boundaries depend on the data itself, not a fixed clock — right for user-session/activity-burst analysis, wrong for anything needing a fixed, predictable reporting cadence (a session window's close time is unknown until the gap is observed, which complicates anything downstream expecting output "by 5 minutes past the hour").
- **Global** (one window for the whole unbounded stream, closed only by an explicit trigger): right when windowing itself isn't the point and you're accumulating all-time state (e.g. a running total) with a custom trigger deciding when to emit — rare as a primary pattern, common as a building block.

## 2. Event time vs processing time — pick based on what "when" means for the business question
**Event time** is when the thing actually happened (a timestamp in the record); **processing time** is when the engine happens to process it. If the business question is "how many orders *occurred* between 2 and 3pm" (reproducible, backfill-safe, correct even if the pipeline was down and catches up later), event time is the only correct choice — processing time would silently include/exclude orders based on unrelated pipeline delays and give different answers on a replay than it gave live. If the business question is closer to "what's happening right now, monitoring-style, approximate is fine" (ops dashboard tolerant of jitter), processing time is simpler and avoids watermark/lateness complexity entirely for a use case that doesn't need it. Default to event time for anything financial, reporting, or reproducibility-sensitive; reserve processing time for genuinely approximate, live-monitoring use cases.

## 3. Watermarks — the mechanism that decides when a window is "done"
A watermark is the engine's estimate of "we've seen all events with event-time up to T" — it's what triggers a window's result to actually emit, since in event-time processing the engine can't otherwise know a window is complete (more late-arriving events could theoretically still come). Watermark generation strategy is a direct tradeoff: a **tight bound** (watermark close to actual max-event-time-seen) gives low latency results but drops/misroutes more genuinely-late data as "too late"; a **loose bound** reduces lateness drops but delays every window's result by the bound's margin, even when no late data actually occurs on a given run. There's no universally correct value — it should be set from the source's *actual* measured out-of-orderness distribution (e.g. "99% of events arrive within 10s of their event time, but a mobile client can be offline for hours"), not a guessed round number.

## 4. Allowed lateness and side outputs — don't just silently drop late data
Most engines let you configure an **allowed lateness** window past the watermark during which a late event still updates an already-fired window result (re-triggering an updated/corrected output) before truly giving up on it. Decide explicitly what happens to data that's late even beyond that: silently drop it (acceptable only if you've measured the volume and decided it's immaterial), route it to a side output/dead-letter path for separate handling or a periodic batch correction job, or — for data where correctness actually matters — build a reconciliation step that compares streaming results against a later batch recompute and corrects discrepancies. "We'll just drop late data" without measuring how much data that actually is, and whether it's randomly distributed or systematically from one source (e.g. one flaky mobile client population), is the most common unexamined assumption in windowed streaming pipelines.

## 5. Common mistakes
- Using a sliding window for a metric that should be tumbling (gives a smoothed, overlapping-count result when a stakeholder actually wanted discrete, non-double-counted hourly totals — easy to produce numbers that don't sum to the right total across hours).
- Setting watermark bound from a guess rather than measured late-arrival distribution, discovering in production that the "normal" lateness for one source (e.g. mobile devices reconnecting after being offline) regularly exceeds it.
- Forgetting that a session window's result timing is data-dependent — a downstream consumer expecting output on a fixed schedule breaks when sessions legitimately take longer to close than expected.

## Verify
- [ ] The window type matches the actual business question's framing (discrete non-overlapping totals → tumbling; trailing continuous rate → sliding; activity-burst grouping → session).
- [ ] Event time vs processing time was a deliberate choice tied to whether reproducibility/backfill-correctness matters for this metric, not a default.
- [ ] The watermark bound is set from a measured out-of-orderness distribution for the actual source, re-checked periodically as source behavior changes.
- [ ] Data arriving later than the allowed-lateness window has a defined fate (side output, reconciliation, or a measured/accepted drop rate) — not a silent, unmeasured drop.
