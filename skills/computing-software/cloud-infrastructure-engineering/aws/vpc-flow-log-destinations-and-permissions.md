---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-flow-log-destinations-and-permissions
name: vpc-flow-log-destinations-and-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-flow-logs, flow-log-destination, flow-logs-s3, flow-logs-firehose, cross-account-logging, parquet]
level: practitioner
status: docs-checked
description: "Publish VPC flow logs to CloudWatch Logs, S3 (Parquet, hive partitions, cross-account) or Firehose with the right IAM role or bucket policy, and pick by cost and use."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-iam-role.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-cwl-create-flow-log.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-permissions.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-cmk-policy.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-path.html", "https://docs.aws.amazon.com/vpc/latest/userguide/firehose-cross-account-delivery.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC flow log destinations and permissions

## 1. Choosing a destination
| Destination | Best for |
|---|---|
| CloudWatch Logs | Live troubleshooting, Logs Insights, metric filters and alarms |
| S3 | Long retention, Athena queries, a central log account |
| Data Firehose | Streaming to SIEM, OpenSearch, Splunk or HTTP endpoints |
Compare current delivery and storage charges for each destination on the VPC and CloudWatch pricing pages; this skill
states no prices. A common pattern is S3 for everything and CloudWatch Logs only for a few VPCs during active debugging.

## 2. CloudWatch Logs
The role must belong to your AWS account, with this permissions policy (Resource `*` in the documented example):
`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`, `logs:DescribeLogGroups`, `logs:DescribeLogStreams`.
Trust policy principal `vpc-flow-logs.amazonaws.com`; AWS recommends confused-deputy conditions:
```json
{"Effect": "Allow", "Principal": {"Service": "vpc-flow-logs.amazonaws.com"},
 "Action": "sts:AssumeRole",
 "Condition": {"StringEquals": {"aws:SourceAccount": "111122223333"},
               "ArnLike": {"aws:SourceArn": "arn:aws:ec2:eu-west-1:111122223333:vpc-flow-log/*"}}}
```
The caller of `create-flow-logs` needs `iam:PassRole` on that role. Set retention on the log group.
```bash
aws ec2 create-flow-logs --resource-type VPC --resource-ids vpc-0abc --traffic-type ALL \
  --log-destination-type cloud-watch-logs --log-group-name /vpc/flow/prod \
  --deliver-logs-permission-arn arn:aws:iam::111122223333:role/FlowLogsToCWL \
  --max-aggregation-interval 60
```

## 3. S3 (including another account)
No IAM role is used: the bucket policy grants the log delivery service. If the flow log creator owns the bucket and has
`PutBucketPolicy` and `GetBucketPolicy`, the policy below is attached automatically and overwrites any existing policy;
otherwise the bucket owner must add it, naming the flow log creator's account, or creation fails.
```json
{"Statement": [
 {"Sid": "AWSLogDeliveryWrite", "Effect": "Allow",
  "Principal": {"Service": "delivery.logs.amazonaws.com"}, "Action": "s3:PutObject",
  "Resource": "arn:aws:s3:::amzn-s3-demo-bucket/*",
  "Condition": {"StringEquals": {"aws:SourceAccount": "123456789012", "s3:x-amz-acl": "bucket-owner-full-control"},
                "ArnLike": {"aws:SourceArn": "arn:aws:logs:us-east-1:123456789012:*"}}},
 {"Sid": "AWSLogDeliveryAclCheck", "Effect": "Allow",
  "Principal": {"Service": "delivery.logs.amazonaws.com"}, "Action": "s3:GetBucketAcl",
  "Resource": "arn:aws:s3:::amzn-s3-demo-bucket",
  "Condition": {"StringEquals": {"aws:SourceAccount": "123456789012"},
                "ArnLike": {"aws:SourceArn": "arn:aws:logs:us-east-1:123456789012:*"}}}]}
```
Restrict the Resource to `.../AWSLogs/<account_id>/*` (or `.../AWSLogs/aws-account-id=<account_id>/*` with Hive-compatible
prefixes) as in the documentation, and grant the delivery service principal rather than individual accounts. The service
calls `HeadBucket` to check the bucket; you need not allow it (CloudTrail shows an AccessDenied for it and delivery continues).
```bash
aws ec2 create-flow-logs --resource-type VPC --resource-ids vpc-0abc --traffic-type ALL \
  --log-destination-type s3 --log-destination arn:aws:s3:::amzn-s3-demo-bucket/vpc/ \
  --log-format '${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${vpc-id} ${subnet-id} ${az-id} ${pkt-srcaddr} ${pkt-dstaddr} ${flow-direction} ${traffic-path}' \
  --destination-options FileFormat=parquet,HiveCompatiblePartitions=true,PerHourPartition=true
```
- Files are published to S3 at 5-minute intervals. Default keys look like
  `<prefix>/AWSLogs/<account_id>/vpcflowlogs/<region>/<year>/<month>/<day>/`; Hive-compatible prefixes use
  `aws-account-id=`, `aws-service=vpcflowlogs`, `aws-region=`, `year=`, `month=`, `day=` and (optionally) `hour=`.
- Parquet queries are documented as 10 to 100 times faster than plain text; below about 100 KB per aggregation period
  Parquet with Gzip can take more space than plain text with Gzip.
- With Hive-compatible prefixes run `MSCK REPAIR TABLE` before queries to load partitions.
- SSE-S3 needs no extra setup. For SSE-KMS use a customer managed key **ARN** (a key ID can produce a
  `LogDestination undeliverable` error) and update the key policy so the log delivery account can write; see the CloudWatch
  Logs User Guide page on S3 bucket server-side encryption for the policy.

## 4. Data Firehose
`--log-destination-type kinesis-data-firehose --log-destination <stream-arn>`. For a stream in another account, create a
role in the source account (trusted by `delivery.logs.amazonaws.com`, allowing `iam:PassRole` to that service,
`logs:CreateLogDelivery`/`DeleteLogDelivery`/`ListLogDeliveries`/`GetLogDelivery`, and `sts:AssumeRole` on the destination
role) and a destination-account role named `AWSLogDeliveryFirehoseCrossAccountRole...` (allowing
`iam:CreateServiceLinkedRole` and `firehose:TagDeliveryStream`, trusting the source role); pass the source role with
`--deliver-cross-account-role`.

## 5. Scope
`--resource-type` accepts `VPC`, `Subnet`, `NetworkInterface`, `TransitGateway`, `TransitGatewayAttachment` and
`RegionalNatGateway`. `--traffic-type ACCEPT|REJECT|ALL`. A REJECT-only flow log is a smaller security baseline;
ALL suits troubleshooting.

## Gotchas
- You cannot change a flow log's configuration or record format after creation; delete it and create a new one.
- You see no data until there is traffic; some records can be skipped during an aggregation interval (`log-status`
  values `OK`, `NODATA`, `SKIPDATA`).
- Not logged: traffic to the Amazon DNS server (queries to your own DNS server are logged), Windows license activation,
  `169.254.169.254` (IMDS), `169.254.169.123` (Time Sync), DHCP, the default VPC router reserved address, mirrored source
  traffic, ARP, and traffic between an endpoint network interface and a Network Load Balancer network interface.
- When a network interface is on a Nitro-based instance the aggregation interval is always 1 minute or less.

## Verify
- [ ] `aws ec2 describe-flow-logs` shows `DeliverLogsStatus: SUCCESS` for each flow log.
- [ ] Objects appear under the expected `AWSLogs/` prefix in S3 (files are published every 5 minutes; delivery to S3 takes about 10 minutes).
- [ ] An Athena query over the Parquet table returns recent records from each account.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "IAM role for publishing flow logs to CloudWatch Logs", "Create a flow log that publishes to CloudWatch Logs", "Amazon S3 bucket permissions for flow logs", "Required key policy for use with SSE-KMS", "Flow log files" (S3 path and format), "IAM roles for cross account delivery", "Flow log limitations" and "Flow log records"; botocore EC2 model (CreateFlowLogs members, DestinationOptionsRequest, FlowLogsResourceType and LogDestinationType enums).
Corrected: bucket policy now follows the documented form (SourceArn condition, scoped Resource, no ListBucket); delivery timing is stated as 5-minute publication and about 10 minutes to S3; SSE-KMS needs a key ARN; added RegionalNatGateway as a resource type; the unlogged-traffic list now matches the documented list.
Removed: all cost comparisons (prices are not checkable from documentation), the aws:SourceOrgID tip, the "one log stream per ENI" statement, and the partition-projection remark.

Method: documentation only; no commands were run.
