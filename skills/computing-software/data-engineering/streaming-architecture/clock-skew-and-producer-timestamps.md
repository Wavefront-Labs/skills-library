---
id: computing-software.data-engineering.streaming-architecture.clock-skew-and-producer-timestamps
name: clock-skew-and-producer-timestamps
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, clock-skew, event-time, producer-timestamps, ntp, watermark, data-quality]
level: advanced
status: draft
description: "Handle clock skew in event-time pipelines: detecting bad producer clocks, clamping or quarantining future/past timestamps, server-side ingestion time and watermark safety."
sources:
  - https://www.oreilly.com/library/view/streaming-systems/9781491983867/
  - https://kafka.apache.org/documentation/#topicconfigs_message.timestamp.after.max.ms
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clock skew and producer timestamps

Event time is only as good as the clock that stamped it. Mobile devices, IoT boards without RTC batteries and misconfigured servers produce timestamps minutes to years off.

## Why it is dangerous
- **Future timestamps** push the watermark (max timestamp minus bound) forward: one event dated next week makes every correct event "late", and windows close prematurely and drop data.
- **Past timestamps** create late data that is dropped or reopens old windows; with Kafka CreateTime they also distort retention and time-index lookups.
- Skew between producers makes ordering by event time across sources wrong (a "logout" before its "login").

## Detect
- Emit `ingest_time - event_time` per source/device as a metric (histogram). Normal: small positive lag. Negative values = clocks ahead. Large positive = buffering devices or clocks behind.
- Track per-device offset over time; consistent offsets mean a skewed clock, not network delay.

## Mitigate
1. **Fix at the source**: NTP/chrony on servers (alert on offset > 100 ms); devices sync from server time on connect.
2. **Capture both times**: event time from the device plus server receive time (and Kafka LogAppendTime). Keep raw values for audits.
3. **Correct**: for devices, compute offset = server_time - device_time at handshake and adjust event times (classic NTP-style correction for offline-buffered events).
4. **Clamp or quarantine at ingestion**:
```sql
-- Flink SQL: never let a future timestamp exceed processing time + tolerance
CREATE TABLE events (..., device_ts TIMESTAMP_LTZ(3),
  ts AS CASE WHEN device_ts > CURRENT_TIMESTAMP + INTERVAL '5' MINUTE THEN CURRENT_TIMESTAMP ELSE device_ts END,
  WATERMARK FOR ts AS ts - INTERVAL '30' SECOND) WITH (...);
```
   Or route out-of-range events to a side output/quarantine topic for inspection rather than silently rewriting.
5. **Broker-side guard**: Kafka 3.6+ `message.timestamp.after.max.ms` / `before.max.ms` reject records with absurd CreateTime.
6. **Watermark robustness**: per-partition watermarks (so one skewed partition affects less), and generators that ignore outliers (e.g. use a percentile of recent timestamps instead of the max) in custom WatermarkGenerators.

## Ordering across sources
Do not rely on cross-source event-time ordering at sub-second precision. Use causal markers (sequence numbers per entity, version vectors) for correctness-critical ordering; event time for analytics.

## Verify
- [ ] Skew metric dashboards per source; alert when negative lag exceeds tolerance.
- [ ] Inject a far-future event in staging: watermark does not jump; event lands in quarantine or is clamped.
