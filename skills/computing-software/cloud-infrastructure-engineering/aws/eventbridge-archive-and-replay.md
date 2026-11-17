---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-archive-and-replay
name: eventbridge-archive-and-replay
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, archive-replay, event-replay, event-archive, replay-events, retention-days, replay-name, event-sourcing, disaster-recovery-events, reprocessing, idempotency, event-driven]
level: practitioner
status: docs-checked
description: "Archive EventBridge events with a pattern and retention, and replay a time window to specific rules so a broken consumer can reprocess history without duplicating side effects elsewhere."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-replay-archived-event.html", "https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_CreateArchive.html", "https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_ReplayDestination.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge archive and replay

**Goal:** when a consumer was broken from 09:00 to 11:30, re-deliver exactly those events to
exactly that consumer — nothing to the others — and have the archive cost under control.

## 1. Create an archive
```bash
aws events create-archive --archive-name orders-all --event-source-arn arn:aws:events:<REGION>:<ACCOUNT_ID>:event-bus/orders \
  --retention-days 90 --event-pattern '{"source":["com.example.orders"]}' --description "all order events, 90d"
```
- Each archive receives events from a single source bus that cannot be changed after creation; you can create
  several archives per bus. With no `--event-pattern`, all events are archived except replayed ones (replayed
  events are never archived; EventBridge adds a managed rule on the bus that excludes events with a `replay-name` field).
- `--retention-days 0` (the default) means events are retained indefinitely. EventBridge charges apply to archives
  (see the EventBridge pricing page).
- After creation, allow a short time before events start flowing into the archive.
- Archives are encrypted with an AWS owned key (AES-256) unless you set `KmsKeyIdentifier`; if the source bus uses a
  customer managed key, AWS strongly recommends a customer managed key for its archives too.
- `describe-archive` `EventCount` and `SizeBytes` reconcile only every 24 hours.

## 2. Replay
```bash
aws events start-replay --replay-name orders-fix-2026-10-16 --event-source-arn arn:aws:events:<REGION>:<ACCOUNT_ID>:archive/orders-all \
  --event-start-time 2026-10-16T09:00:00Z --event-end-time 2026-10-16T11:30:00Z \
  --destination '{"Arn":"arn:aws:events:<REGION>:<ACCOUNT_ID>:event-bus/orders","FilterArns":["arn:aws:events:<REGION>:<ACCOUNT_ID>:rule/orders/fulfilment-consumer"]}'
aws events describe-replay --replay-name orders-fix-2026-10-16    # progress: State, EventLastReplayedTime
aws events cancel-replay --replay-name ...
```
- Archived events can only be replayed to the **source event bus** (`Destination.Arn` must be the bus the archive was created from).
- **`FilterArns` is the safety switch**: it lists the rules to replay events to. Without it the replay goes to
  all rules on the bus, so every consumer sees the events again (payments, emails, ...).
- When EventBridge replays an event it adds a `replay-name` field containing the replay's name; consumers can use
  it to recognise replays.
- Replays process events by the time in the event, in one-minute intervals, so order is not guaranteed to match
  the original. Replayed events count against the account's `PutEvents` rate limit.
- Wait about 10 minutes after the event window before replaying, because events can reach the archive with a delay.
- You can have at most 10 active concurrent replays per account per Region; replays can be cancelled while
  Starting or Running; EventBridge deletes replay records after 90 days. Replaying does not remove events from the archive.

## 3. Idempotency is your job
Replayed events reach targets exactly like originals: a Lambda that charged a card will
charge it again. Before replaying, confirm the target consumer dedupes on event `id` (store
processed IDs with a TTL at least as long as the archive retention) or is naturally idempotent (upserts).

## 4. Operational uses
- Rebuild a read model / search index: replay the full archive to a rule targeting the indexer.
- Onboard a new consumer with history: temporary rule → new consumer, replay, delete rule.
- Inspect archived events by replaying a window to a rule whose target is CloudWatch Logs, then query with Logs Insights.

## Gotchas
- Events leave an archive only when they exceed the retention period or the archive is deleted. For long-term
  queryable history, also route events to Firehose and S3.

## Verify
- [ ] `describe-archive` shows `EventCount` growing after publishing test events (allow up to 24 hours for the counts to reconcile).
- [ ] A replay with `FilterArns` of one rule invokes only that rule's target (`Invocations` metric by rule name); other rules show zero.
- [ ] The consumer's logs show `replay-name` on replayed events and skip non-idempotent side effects.

## Checked

Date 2026-10-23. Documentation release: current Amazon EventBridge User Guide and API Reference (archive and replay, CreateArchive, ReplayDestination).
Confirmed: single source bus; multiple archives per bus; no pattern means all except replayed events; `RetentionDays` 0 means indefinite; AWS owned key encryption and customer managed key option; 24-hour reconciliation of `EventCount`/`SizeBytes`; replays go only to the source bus; `FilterArns` lists rules; `replay-name` field and the managed rule that blocks re-archiving; one-minute interval processing; PutEvents rate limit; 10 concurrent replays; 90-day replay record retention; cancel while Starting or Running; 10-minute wait recommendation.
Corrected: the draft said replays into a different bus are allowed, which the docs and API reference forbid; replay ordering is by event time in one-minute steps rather than a plain time-ordered stream.
Removed (not in docs): state list, original `time`/`id` retention remark, throughput estimates, 24-hour splitting, Step Functions remark, archive search remark, `update-archive` and `ResourceNotFoundException` remarks, input-transformer and schedule remarks, delete-with-replay remark.
Sources: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html ; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-replay-archived-event.html ; https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_CreateArchive.html ; https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_ReplayDestination.html

Method: documentation only; no commands were run.
