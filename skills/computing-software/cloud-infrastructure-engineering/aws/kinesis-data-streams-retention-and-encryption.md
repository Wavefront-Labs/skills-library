---
id: computing-software.cloud-infrastructure-engineering.aws.kinesis-data-streams-retention-and-encryption
name: kinesis-data-streams-retention-and-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kinesis, kinesis-data-streams, stream-retention, kds-encryption, sse-kms, extended-retention]
level: practitioner
status: docs-checked
description: "Set Kinesis Data Streams retention (24 hours up to 365 days) for replay and recovery, and turn on server-side encryption with KMS including producer and consumer permissions."
sources: ["https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html", "https://docs.aws.amazon.com/streams/latest/dev/what-is-sse.html", "https://docs.aws.amazon.com/streams/latest/dev/permissions-user-key-KMS.html", "https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis Data Streams retention and encryption

## Retention
- Default 24 hours. Increase up to 8,760 hours (365 days).
```bash
aws kinesis increase-stream-retention-period --stream-name clicks --retention-period-hours 168
aws kinesis decrease-stream-retention-period --stream-name clicks --retention-period-hours 24
aws kinesis describe-stream-summary --stream-name clicks --query 'StreamDescriptionSummary.RetentionPeriodHours'
```
- Additional charges apply to any retention above 24 hours; check the Kinesis Data Streams
  pricing page for the tiers before setting a long period.
- Why longer: replay after a consumer bug (`ShardIteratorType=AT_TIMESTAMP`), onboarding a new
  consumer from history, surviving a consumer outage longer than a day.
- Minimum is 24 hours. Increase and decrease are each limited to 5 calls per second per stream.
- Increasing retention stops making records inaccessible at the old period within several
  minutes. Decreasing it makes records older than the new period inaccessible almost
  immediately, so take care.
- Replay with Lambda: create a new event source mapping with `StartingPosition AT_TIMESTAMP`.

## Server-side encryption
```bash
aws kinesis start-stream-encryption --stream-name clicks \
  --encryption-type KMS --key-id alias/aws/kinesis      # or a customer managed key ARN
aws kinesis describe-stream-summary --stream-name clicks --query 'StreamDescriptionSummary.EncryptionType'
```
- Applies to records written after it is enabled; existing records stay as they were until they age out.
- With a customer managed key, producers need `kms:GenerateDataKey` and consumers `kms:Decrypt`
  on the key (key policy or grants). Firehose and Lambda consumers use their roles for this.
- The default key `alias/aws/kinesis` needs no custom IAM permissions; a customer managed key
  needs producers and consumers listed in the key policy or granted through IAM. Stream
  administrators need `kms:List*` and `kms:DescribeKey*`.
- Kinesis passes the stream ARN as encryption context (`aws:kinesis:arn`), so the
  `kms:EncryptionContext:aws:kinesis:arn` condition key can limit a key to one stream.
- KMS calls can be throttled; `PutRecords` then reports `KMSThrottlingException` per record.
- Cross-account access needs both the key policy and the IAM policy in the other account. A stream
  encrypted with the AWS managed key cannot be shared through a resource policy; switch to a
  customer managed key first.
- Applying a new KMS key succeeds 25 times and disabling encryption succeeds 25 times per stream in
  a rolling 24-hour period.
- Managed Service for Apache Flink and Lambda consume through roles; add `kms:Decrypt` to those roles.

## Gotchas
- `stop-stream-encryption` exists; avoid it unless rotating to a new key.
- A disabled key makes writes fail with `KMSDisabledException`; deleting the key makes the data unreadable.
- Enhanced fan-out consumers also need decrypt permission.

## Verify
- [ ] `RetentionPeriodHours` matches the documented recovery window; cost estimate recorded.
- [ ] `EncryptionType` is `KMS`; a producer without `kms:GenerateDataKey` is denied (negative test).
- [ ] Replay drill from `AT_TIMESTAMP` works in staging.

## Checked

2026-10-27, AWS documentation (current release as read on that date). Kinesis Data Streams Developer Guide pages on retention, server-side encryption, KMS permissions and quotas, plus the botocore kinesis 2013-12-02 model. Confirmed: retention 24 to 8760 hours, almost-immediate effect of a decrease, 25 key changes per 24 hours, kms:GenerateDataKey and kms:Decrypt roles, alias/aws/kinesis, AT_TIMESTAMP iterator and Lambda start position, KMS exception names. Removed the extended and long-term retention billing tiers, which the pages do not state.
Method: documentation only; no commands were run.
