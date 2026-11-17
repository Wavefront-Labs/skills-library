---
id: computing-software.cloud-infrastructure-engineering.aws.s3-server-access-logging-and-data-events
name: s3-server-access-logging-and-data-events
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, server-access-logging, s3-access-logs, cloudtrail, data-events, athena, audit]
level: practitioner
status: docs-checked
description: "Log S3 object access: server access logs (target bucket, partitioned prefixes, Athena) vs CloudTrail data events (selectors, cost), what each records, and which to use when."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-server-access-logging.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 server access logs vs CloudTrail data events

| | Server access logs | CloudTrail data events |
|---|---|---|
| Delivery | best effort, most records within a few hours, completeness and timeliness not guaranteed | delivery timing per the CloudTrail user guide |
| Cost | no charge for delivery (pay storage) | billed per event (see CloudTrail pricing); can be large on busy buckets |
| Format | space-delimited text | JSON, with full IAM identity, session context |
| Extra detail | HTTP status, bytes, turn-around time, referrer, lifecycle actions | request parameters, `vpcEndpointId`, organisation-level trails, EventBridge |
Use access logs for **traffic/usage analysis** and cheap broad coverage; CloudTrail data
events for **security audit** on sensitive buckets (scoped with selectors).

## 1. Server access logs
```bash
aws s3api put-bucket-logging --bucket app-data --bucket-logging-status '{"LoggingEnabled":{
  "TargetBucket":"org-s3-access-logs","TargetPrefix":"app-data/",
  "TargetObjectKeyFormat":{"PartitionedPrefix":{"PartitionDateSource":"EventTime"}}}}'
```
Target bucket: same Region and account, **not the source bucket** (AWS says logging into the same bucket causes an infinite loop of logs), bucket policy
allowing principal `logging.s3.amazonaws.com` with `aws:SourceAccount`/`aws:SourceArn`
conditions. Partitioned prefixes (`.../<ACCOUNT_ID>/<REGION>/<BUCKET>/YYYY/MM/DD/`) make
Athena partition projection simple.

Athena (after creating the table from the documented DDL):
```sql
SELECT requester, operation, count(*) n, sum(bytessent)/1e9 gb
FROM s3_access_logs WHERE bucket_name = 'app-data' AND timestamp LIKE '16/Oct/2026%'
GROUP BY 1,2 ORDER BY n DESC LIMIT 20;
```

## 2. CloudTrail data events (targeted)
```bash
aws cloudtrail put-event-selectors --trail-name org-trail --advanced-event-selectors '[{
 "Name":"S3 writes and deletes on sensitive buckets",
 "FieldSelectors":[{"Field":"eventCategory","Equals":["Data"]},
  {"Field":"resources.type","Equals":["AWS::S3::Object"]},
  {"Field":"readOnly","Equals":["false"]},
  {"Field":"resources.ARN","StartsWith":["arn:aws:s3:::payroll/","arn:aws:s3:::pii-exports/"]}]}]'
```
Scoping by bucket and by read/write keeps costs sane; logging all reads on a busy data lake
can cost more than the storage.

## Gotchas
- Access log delivery can lag hours and occasionally drop records — never rely on it for
  billing-grade accounting or legal audit.
- S3 Lifecycle actions appear in access logs with operations of the form `S3.action.resource_type`.
- Server access logs can instead be delivered to CloudWatch Logs (log group, S3 as JSON or Parquet, or
  Firehose), which supports cross-Region and cross-account delivery and KMS; the plain S3 destination
  must be in the same Region and account and uses SSE-S3 only.
- Requests via access points log the access point ARN.

## Verify
- [ ] After a test `GetObject`, a log record appears under the partitioned prefix (within hours) and in CloudTrail (if selected).
- [ ] Target bucket has a lifecycle rule for log retention.
- [ ] CloudTrail cost for S3 data events reviewed after one week.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Logging requests with server access logging, Enabling server access logging, Server access log format, CloudTrail data events for S3, the CloudTrail record contents page and the botocore s3 model.
Confirmed: no charge for server access log delivery beyond storage; best-effort delivery within a few hours, not guaranteed complete; destination bucket in the same Region and account; logging.s3.amazonaws.com principal in the target bucket policy; same-bucket delivery causes an infinite loop; PartitionedPrefix with PartitionDateSource EventTime and the [SourceAccountId]/[SourceRegion]/[SourceBucket]/[YYYY]/[MM]/[DD] layout; lifecycle operations are logged as S3.action.resource_type; access point ARN field; CloudTrail advanced selector fields eventCategory, resources.type AWS::S3::Object, readOnly and resources.ARN with StartsWith, set through put-event-selectors; CloudTrail events are available to EventBridge. The CloudTrail delivery-time figure was removed because it could not be confirmed.

Method: documentation only; no commands were run.
