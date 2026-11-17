---
id: computing-software.cloud-infrastructure-engineering.aws.sns-fifo-message-archiving-and-replay
name: sns-fifo-message-archiving-and-replay
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, message-archiving, sns-replay, sns-fifo, archive-policy, replay-policy]
level: practitioner
status: docs-checked
description: "Archive messages on an SNS FIFO topic and replay them to a subscription: ArchivePolicy retention, ReplayPolicy time windows, filter behaviour and replay monitoring."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/message-archiving-and-replay-topic-owner.html", "https://docs.aws.amazon.com/sns/latest/dg/message-archiving-and-replay-subscriber.html", "https://docs.aws.amazon.com/sns/latest/dg/fifo-message-archiving-replay.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS FIFO message archiving and replay

**Goal:** keep an in-service copy of published messages on a FIFO topic and redeliver a time
range to one subscriber after a bug, outage or new consumer onboarding.

Available on **FIFO topics only**. For standard topics use EventBridge archive/replay or a
Firehose-to-S3 subscription.

## Enable archiving (topic owner)
```bash
aws sns set-topic-attributes --topic-arn "$TOPIC" \
  --attribute-name ArchivePolicy --attribute-value '{"MessageRetentionPeriod":"30"}'
```
- `MessageRetentionPeriod` is a number of days, 1 to 365 (any integer above zero activates archiving; `ArchivePolicy` can
  be set with `CreateTopic` or `SetTopicAttributes`). Available only on application-to-application (A2A) FIFO topics.
- `GetTopicAttributes` returns `BeginningArchiveTime`, the oldest timestamp from which a replay can start.
- Disable by unsetting the policy (`{}`): deactivating **deletes all archived messages**, and a topic with an
  active archive policy cannot be deleted until the policy is deactivated.
- Additional charges apply for archiving (see SNS pricing).
- If the topic is KMS-encrypted, the key policy must allow the `sns.amazonaws.com` principal `kms:Decrypt` and
  `kms:GenerateDataKey` or replays fail.

## Replay to a subscription (subscription owner)
```bash
aws sns set-subscription-attributes --subscription-arn "$SUB" \
  --attribute-name ReplayPolicy --attribute-value \
  '{"PointType":"Timestamp","StartingPoint":"2026-10-17T08:00:00Z","EndingPoint":"2026-10-17T09:30:00Z"}'
```
`ReplayPolicy` fields: `PointType` (required, currently only `Timestamp`), `StartingPoint` (required),
`EndingPoint` (optional). The policy can be passed to `Subscribe` or `SetSubscriptionAttributes`; starting a
new replay replaces the existing one. The console shows a replay status of Pending (default while it starts),
In progress, Completed or Failed.
- Omit `EndingPoint` to replay until caught up and then continue with live traffic.
- **If you set an `EndingPoint`, the subscription is effectively paused after the replay**: new messages are not
  delivered until you apply a new `ReplayPolicy` without `EndingPoint` (for example starting at the previous
  `EndingPoint`).
- Replay goes only to that subscription.
- SNS retrieves each archived message and then applies the subscription's `FilterPolicy`, so a corrected
  filter can pick up messages the old one dropped.
- A replayed message keeps the same content, `MessageId` and `Timestamp`, and carries a boolean `Replayed`
  attribute; consumers must be idempotent.
- CloudWatch metrics: `NumberOfReplayedNotificationsDelivered` and `NumberOfReplayedNotificationsFailed`
  (subscriber side); `ApproximateNumberOfMessagesArchived`, `ApproximateNumberOfBytesArchived`,
  `NumberOfMessagesArchiveProcessing`, `NumberOfBytesArchiveProcessing` (topic owner).

## Gotchas
- FIFO topics deliver to SQS FIFO or standard queues; the queue's limits apply to the replay burst.
- Deleting a topic requires deactivating the archive policy first, which deletes the archive: it is not a backup.

## Verify
- [ ] `ArchivePolicy` and `BeginningArchiveTime` present on the topic.
- [ ] Test replay of a 5-minute window to a scratch FIFO queue: message count matches publishes in that window.
- [ ] Runbook covers who may set ReplayPolicy (IAM `sns:SetSubscriptionAttributes`), the pause behaviour of `EndingPoint`, and the replay metrics.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (FIFO message archiving for topic owners and replay for subscribers).
Confirmed: A2A FIFO only; `ArchivePolicy` `MessageRetentionPeriod` 1 to 365 days; unsetting deletes the archive; `BeginningArchiveTime`; `ReplayPolicy` fields and `Timestamp` point type; filter policy applied to replays; `Replayed` attribute and unchanged `MessageId`; KMS decrypt grant; metrics; archive costs extra.
Corrected: an `EndingPoint` pauses the subscription (the draft implied live traffic continues); the deletion rules; "archived storage billed per GB-month" and `ReplayStatus` value "Replaying" were not in the docs (console shows In progress).
Removed (not in docs): `get-subscription-attributes --query` ReplayStatus attribute path, group-ordering and 5-minute dedup remarks, billing detail.
Sources: https://docs.aws.amazon.com/sns/latest/dg/message-archiving-and-replay-topic-owner.html ; https://docs.aws.amazon.com/sns/latest/dg/message-archiving-and-replay-subscriber.html ; https://docs.aws.amazon.com/sns/latest/dg/fifo-message-archiving-replay.html

Method: documentation only; no commands were run.
