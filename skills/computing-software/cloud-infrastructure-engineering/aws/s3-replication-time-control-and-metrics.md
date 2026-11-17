---
id: computing-software.cloud-infrastructure-engineering.aws.s3-replication-time-control-and-metrics
name: s3-replication-time-control-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-replication, replication-time-control, rtc, replication-metrics, cross-region-replication, rpo]
level: practitioner
status: docs-checked
description: "Make S3 replication measurable: Replication Time Control (15-minute SLA), replication metrics and events, latency alarms, and diagnosing FAILED replication."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-time-control.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/repl-metrics.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-metrics-events.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/metrics-dimensions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Replication Time Control and replication metrics

Plain replication is asynchronous: most objects replicate within 15 minutes, large objects can take up
to several hours, and there is no SLA. If DR has an RPO, you need **RTC** and metrics.

## 1. Enable RTC + metrics on a rule
```json
{"Role": "arn:aws:iam::<ACCOUNT_ID>:role/s3-replication",
 "Rules": [{"ID": "to-dr", "Status": "Enabled", "Priority": 1, "Filter": {},
   "DeleteMarkerReplication": {"Status": "Enabled"},
   "Destination": {"Bucket": "arn:aws:s3:::orders-dr-euw1",
     "ReplicationTime": {"Status": "Enabled", "Time": {"Minutes": 15}},
     "Metrics": {"Status": "Enabled", "EventThreshold": {"Minutes": 15}},
     "EncryptionConfiguration": {"ReplicaKmsKeyID": "arn:aws:kms:eu-west-1:<ACCOUNT_ID>:key/..."}},
   "SourceSelectionCriteria": {"SseKmsEncryptedObjects": {"Status": "Enabled"}}}]}
```
```bash
aws s3api put-bucket-replication --bucket orders-use1 --replication-configuration file://repl.json
```
RTC replicates most objects in seconds and a stated percentage within 15 minutes, backed by an SLA
(the RTC page says 99.9 percent; the Multi-Region Access Point page says 99.99 percent: confirm the
current figure on the RTC page and the S3 SLA). The SLA does not apply while request-rate guidelines or
the default 1 Gbps replication transfer-rate quota are exceeded. RTC and replication metrics carry
additional charges. `ReplicationTime.Time.Minutes` and `Metrics.EventThreshold.Minutes` can only be `15`.
Metrics alone (without RTC) can also be enabled.

## 2. Metrics (namespace `AWS/S3`, dimensions SourceBucket, DestinationBucket, RuleId)
`ReplicationLatency` (seconds, Max), `BytesPendingReplication`, `OperationsPendingReplication`,
`OperationsFailedReplication` (Sum). The first three are published in the destination bucket's Region and
`OperationsFailedReplication` in the source Region; create each alarm in the matching Region, with
missing-data treatment set to ignore (`--treat-missing-data ignore`).
```bash
aws cloudwatch put-metric-alarm --alarm-name s3-repl-latency-orders --namespace AWS/S3 \
  --metric-name ReplicationLatency --dimensions Name=SourceBucket,Value=orders-use1 Name=DestinationBucket,Value=orders-dr-euw1 Name=RuleId,Value=to-dr \
  --treat-missing-data ignore --statistic Maximum --period 300 --evaluation-periods 3 --threshold 900 --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:<REGION>:<ACCOUNT_ID>:storage-oncall
```

## 3. Events
S3 event types `s3:Replication:OperationMissedThreshold` and `OperationReplicatedAfterThreshold`
(need RTC), `OperationFailedReplication` (needs metrics only) and `OperationNotTracked` go to
SQS, SNS or Lambda for per-object follow-up.

## 4. Diagnose FAILED
`head-object` on the source shows `ReplicationStatus: FAILED`. Usual causes: replication role
lacks `kms:Decrypt` on the source key or `kms:Encrypt` on the replica key; destination bucket
policy/Object Lock/ownership denies; objects that are themselves replicas made by another rule
(not re-replicated onward). The `failureReason` values are listed in the S3 replication failure reasons table.
Re-drive failed objects with **Batch Replication** after fixing.

## Gotchas
- Versioning must be on for both buckets.
- Replication applies to new objects after the rule exists — existing ones need Batch Replication.
- KMS-heavy replication counts toward KMS request quotas and can be throttled; request an increase through Service Quotas.

## Verify
- [ ] `ReplicationLatency` metric reports and stays well under 900 s at peak.
- [ ] Test object reaches `ReplicationStatus: COMPLETED` on source and `REPLICA` on destination.
- [ ] Alarm fires in a test by temporarily breaking the role's KMS permission (non-prod).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: RTC JSON fields and the 15-minute-only values, RTC SLA caveats (the two AWS pages quote 99.9 and 99.99 percent, so the percentage is left to the live page), metric names, statistics, dimensions and publishing Regions, alarm missing-data guidance, event type names and which need RTC. Removed the SSE-C exclusion and the unconfirmed Bucket Keys claim.

Method: documentation only; no commands were run.
