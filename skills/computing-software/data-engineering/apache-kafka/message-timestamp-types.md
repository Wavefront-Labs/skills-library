---
id: computing-software.data-engineering.apache-kafka.message-timestamp-types
name: message-timestamp-types
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, message-timestamp-type, createtime, logappendtime, timestamps, retention-ms, kafka-topic-design]
level: practitioner
status: docs-checked
description: "Choose CreateTime vs LogAppendTime for Kafka topics, and handle bad producer clocks that break time-based retention, offset lookups and stream event time."
sources:
  - https://kafka.apache.org/39/implementation/message-format/
  - https://kafka.apache.org/39/getting-started/upgrade/
  - https://kafka.apache.org/40/getting-started/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message timestamp types: CreateTime vs LogAppendTime

Each record carries one timestamp. The topic config `message.timestamp.type` decides its meaning:
| Type | Set by | Use for |
|---|---|---|
| `CreateTime` (default) | the producer (record timestamp or `System.currentTimeMillis()` at send) | event time; the producer can set the real event time explicitly |
| `LogAppendTime` | the broker, overwriting the producer's value when the leader appends | ingestion time; trustworthy for retention and offset lookups |

```bash
kafka-configs.sh --bootstrap-server $BS --alter --entity-type topics --entity-name clicks \
  --add-config message.timestamp.type=LogAppendTime
```

## What timestamps drive
- **Time-based retention** (`retention.ms`): retention is based on the largest timestamp of the messages in a log segment. One record with a timestamp far in the future therefore keeps its whole segment past retention; bad clocks distort retention.
- `offsetsForTimes` / `kafka-consumer-groups --to-datetime` lookups.
- Kafka Streams / Flink / Spark event time when they read the record timestamp.

## Guarding against bad clocks with CreateTime
Kafka 3.6+ (KIP-937):
```properties
message.timestamp.before.max.ms=604800000   # reject records more than 7 days in the past
message.timestamp.after.max.ms=3600000      # reject records more than 1 hour in the future
```
Older versions only have the symmetric `message.timestamp.difference.max.ms` (the broker-level `log.` form is deprecated from 3.6 and removed in 4.0). With `CreateTime`, records outside the limits are rejected, so producers see the problem instead of it silently corrupting retention. The example values above are illustrations, not defaults.

## Choosing
- Producers you control, event time matters (backfills replay old events): `CreateTime`, set the timestamp to the event time, and set the before/after limits generously enough for backfills.
- Many untrusted producers, retention correctness matters, event time is in the payload anyway: `LogAppendTime`.
- A topic set to `LogAppendTime` makes the broker overwrite the timestamp on append, including for mirrored records.

## Verify
- [ ] `kafka-console-consumer.sh --property print.timestamp=true` shows timestamps that match the expected type.
- [ ] No segments much older than retention lingering on disk.

## Checked
2026-10-28. Confirmed in the Kafka 3.9 generated topic and broker config tables, the message-format page and the 3.9/4.0 upgrade notes: `message.timestamp.type`, `message.timestamp.before.max.ms` and `message.timestamp.after.max.ms` (KIP-937, 3.6), rejection under CreateTime, deprecation of `*.timestamp.difference.max.ms` and its removal at broker level in 4.0, retention based on the largest timestamp in a segment, broker overwrite under LogAppendTime, `print.timestamp` formatter property, `kafka-configs.sh --alter --entity-type --entity-name --add-config` (ConfigCommand source). Removed: the `InvalidTimestampException` name, segment rolling claim, the MirrorMaker 2 preservation claim and the `CreateTime:` output prefix.
Method: documentation only; no commands were run.
