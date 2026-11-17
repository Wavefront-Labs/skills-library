---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-flow-log-cost-control
name: vpc-flow-log-cost-control
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-flow-logs, flow-log-cost, vended-logs, parquet, cost-optimization]
level: practitioner
status: docs-checked
description: "Cut VPC flow log cost by choosing S3 over CloudWatch, Parquet with hourly partitions, narrower scope and fields, REJECT-only filters and retention lifecycles."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-basics.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-path.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3-create-flow-log.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow log cost control

Flow log charges depend on the destination you publish to (CloudWatch Logs, S3 or Firehose) plus whatever you use to query the data (Athena and, for the Athena integration, a Lambda that loads partitions). Check the current pricing pages; no prices are repeated here.

## 1. Destination
| Destination | Use |
|---|---|
| CloudWatch Logs | Logs Insights queries and metric filters; delivery typically takes about 5 minutes |
| S3 | long-term storage, query with Athena; delivery typically takes about 10 minutes |
| Firehose | streaming to a SIEM or other consumer |
Keep long-term VPC-wide logs in S3; send only targeted, short-lived logs to CloudWatch.

## 2. S3 format options
```bash
aws ec2 create-flow-logs --resource-type VPC --resource-ids vpc-0abc --traffic-type ALL \
  --log-destination-type s3 --log-destination arn:aws:s3:::flowlogs-<ACCOUNT_ID>/ \
  --destination-options FileFormat=parquet,HiveCompatiblePartitions=true,PerHourPartition=true \
  --max-aggregation-interval 600
```
AWS documents Parquet queries as 10 to 100 times faster than plain text and Gzip-compressed Parquet as taking 20 percent less storage (but if there is under 100 KB of data per aggregation period, Parquet can take more space). Hourly partitions give faster results and lower query costs when you target a specific hour; Hive-compatible prefixes need `MSCK REPAIR TABLE` before queries.

## 3. Volume levers
- Scope: subnet-level logs for sensitive tiers instead of every VPC in dev.
- `--traffic-type REJECT` where you only need denied traffic.
- Maximum aggregation interval 600 s (the default, 10 minutes) instead of 60 s; 1-minute logs produce a higher volume of records. Valid values are 60 and 600.
- Custom `--log-format` with only the fields you use (fewer bytes per record).

## 4. Retention
- S3 lifecycle: transition or expire flow log objects per your retention policy.
- CloudWatch: set `aws logs put-retention-policy --log-group-name <GROUP> --retention-in-days 14` (14 is an allowed value) on debug groups rather than keeping them forever.

## 5. Find the spend
Tag flow logs when you create them (`--tag-specifications`) so spend can be attributed, and review the flow log lines in your cost reports.

## Verify
- [ ] Flow log monthly cost per VPC tracked; dev VPCs on REJECT-only or subnet scope.
- [ ] Athena queries over hourly partitions scan only the targeted hour (check the data scanned figure).

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (flow log records and aggregation interval, flow log files, publish to S3, limitations) and the botocore EC2 and CloudWatch Logs models.
- Default 10-minute maximum aggregation interval, 1-minute option with higher record volume, typical delivery times (about 5 minutes to CloudWatch Logs, about 10 minutes to S3), Parquet speed and storage statements, hourly partitions and Hive-compatible prefixes confirmed.
- `create-flow-logs` options (`--destination-options` `FileFormat`, `HiveCompatiblePartitions`, `PerHourPartition`, `--max-aggregation-interval` 60 or 600, `--traffic-type`, `--log-format`, tags) confirmed in the service model; `put-retention-policy` accepts 14 days.
- Removed the destination cost comparisons, the Glacier lifecycle example and the Cost Explorer usage type names: the pricing pages could not be read and no page confirms them.

Method: documentation only; no commands were run.
