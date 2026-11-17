---
id: computing-software.data-engineering.apache-kafka.reset-offsets-and-replay
name: reset-offsets-and-replay
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-consumer, consumer-groups, reset-offsets, auto-offset-reset, replay, kafka-consumer-groups, to-datetime, shift-by, offsets-for-times, reprocessing]
level: practitioner
status: docs-checked
description: "Replay or skip Kafka data by resetting consumer group offsets: kafka-consumer-groups --reset-offsets (to-datetime, shift-by, to-offset), dry-run vs execute, and auto.offset.reset."
sources:
  - https://kafka.apache.org/40/operations/basic-kafka-operations/
  - https://kafka.apache.org/40/configuration/consumer-configs/
  - https://kafka.apache.org/39/streams/developer-guide/app-reset-tool/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resetting consumer offsets and replaying

**Goal:** reprocess a time range after a bug fix, or skip poison data, in a controlled, auditable way.

## Preconditions
- The group must be **inactive** (all consumer instances stopped); the tool resets one group at a time.
- The data must still be retained (`retention.ms`).
- The downstream sink must tolerate replays (idempotent upserts) or you will double-count.

## Commands
```bash
B=<BROKER>:9092; G=billing-projector; T=orders.checkout.order-placed.v1
# 1. record current position (for rollback)
kafka-consumer-groups.sh --bootstrap-server $B --describe --group $G > offsets-before.txt
# 2. plan (default is --dry-run)
kafka-consumer-groups.sh --bootstrap-server $B --group $G --topic $T \
  --reset-offsets --to-datetime 2026-10-15T00:00:00.000+00:00 --dry-run
# 3. apply
kafka-consumer-groups.sh --bootstrap-server $B --group $G --topic $T \
  --reset-offsets --to-datetime 2026-10-15T00:00:00.000+00:00 --execute
```
Other targets: `--to-earliest`, `--to-latest`, `--to-offset N`, `--shift-by -1000`, `--by-duration PT6H`, `--from-file offsets.csv` (topic,partition,offset rows; also how you roll back using the saved CSV from `--export`).
Scope: `--topic T` (all partitions), `--topic T:0,3` (specific partitions), `--all-topics`.

`--to-datetime` goes by record timestamps, so producers with wrong clocks make it imprecise (see message-timestamp-types).

## Skip a poison message
```bash
kafka-consumer-groups.sh --bootstrap-server $B --group $G --topic $T:7 --reset-offsets --to-offset 551234 --execute
```
Prefer handling it in code (DLQ) so it never blocks again.

## auto.offset.reset
Applies only when the group has **no committed offset** (new group, or offsets expired after `offsets.retention.minutes`; the upgrade notes give 7 days as the default since 2.0): `latest` (default) skips history, `earliest` reads all retained data, `none` throws. For a backfill consumer, a fresh group with `earliest` is often cleaner than resetting the production group.

## Programmatic
`offsetsForTimes` then `seek()` in the app. Kafka Streams: `kafka-streams-application-reset` (resets input topics, deletes internal topics; you must also delete local state with `KafkaStreams#cleanUp()` or by removing the state directory; run it once with `--dry-run` first).

## Verify
- [ ] Dry-run output reviewed and saved before `--execute`.
- [ ] After restart, `--describe` shows lag equal to the expected replay volume and draining.
- [ ] Downstream row counts for the replayed window match expectations (no doubles).

## Checked
2026-10-28. Confirmed in ConsumerGroupCommandOptions source (Kafka 3.9), the 3.9/4.0 basic operations page, the Streams application reset tool page, the consumer config tables and the upgrade notes: options `--reset-offsets`, `--dry-run` (default) and `--execute`, `--export`, `--to-datetime`, `--by-duration` (PnDTnHnMnS), `--to-earliest`, `--to-latest`, `--to-offset`, `--shift-by`, `--from-file` (CSV), `--all-topics`, `topic:0,1,2` partition syntax, inactive-group requirement, `auto.offset.reset` values and semantics, `offsets.retention.minutes` (7 days since 2.0), Streams reset tool behaviour. Removed: the exact error text, the log-start-offset claim, the timestamp-index remark and the `alterConsumerGroupOffsets` name.
Method: documentation only; no commands were run.
