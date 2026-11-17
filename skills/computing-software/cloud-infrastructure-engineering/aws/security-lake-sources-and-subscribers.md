---
id: computing-software.cloud-infrastructure-engineering.aws.security-lake-sources-and-subscribers
name: security-lake-sources-and-subscribers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-lake, ocsf, security-data-lake, siem-integration, lake-formation, athena]
level: advanced
status: docs-checked
description: "Stand up Amazon Security Lake: org-wide AWS log sources, rollup regions, retention, custom OCSF sources, and data-access vs query-access subscribers for SIEMs."
sources: ["https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html", "https://docs.aws.amazon.com/security-lake/latest/userguide/internal-sources.html", "https://docs.aws.amazon.com/security-lake/latest/userguide/custom-sources.html", "https://docs.aws.amazon.com/security-lake/latest/userguide/subscriber-management.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon Security Lake

**What it is:** a fully managed security data lake in your own account, backed by S3 buckets you own. It collects
security logs and events from AWS services, SaaS, on-premises and third-party sources, converts them to Apache Parquet
and the Open Cybersecurity Schema Framework (OCSF), manages lifecycle (retention, replication, storage tiering) and lets
subscribers consume the data. It creates a Lake Formation table for each source and uses Glue crawlers to populate the
Glue Data Catalog. Security Lake does not support Amazon S3 Select.

## 1. Enable
1. Designate a delegated administrator from the management account:
   `aws securitylake register-data-lake-delegated-administrator --account-id <ACCOUNT_ID>`
2. Create the lake in chosen Regions with a KMS key, lifecycle and replication (field names from the API model):
```bash
aws securitylake create-data-lake --meta-store-manager-role-arn \
  arn:aws:iam::<ACCOUNT_ID>:role/<META_STORE_MANAGER_ROLE> \
  --configurations '[{"region":"eu-west-1","encryptionConfiguration":{"kmsKeyId":"<key-arn>"},
     "lifecycleConfiguration":{"transitions":[{"days":30,"storageClass":"STANDARD_IA"}],
                               "expiration":{"days":400}}},
   {"region":"eu-central-1","replicationConfiguration":{"regions":["eu-west-1"],
     "roleArn":"arn:aws:iam::<ACCOUNT_ID>:role/<REPLICATION_ROLE>"}}]'
```
   A **rollup Region** (here eu-west-1) consolidates data from contributing Regions; this helps with data residency
   requirements.
3. Enable for new organization accounts with `create-data-lake-organization-configuration`.

## 2. AWS sources
Natively supported: CloudTrail management and data events (S3, Lambda), EKS audit logs, Route 53 resolver query logs,
Security Hub CSPM findings, VPC Flow Logs and WAFv2 logs. API `sourceName` values: `ROUTE53`, `VPC_FLOW`,
`SH_FINDINGS`, `CLOUD_TRAIL_MGMT`, `LAMBDA_EXECUTION`, `S3_DATA`, `EKS_AUDIT`, `WAF`.
```bash
aws securitylake create-aws-log-source --sources sourceName=VPC_FLOW,accounts='["<ACCOUNT_ID>"]',regions='["eu-west-1"]',sourceVersion="2.0"
aws securitylake get-data-lake-sources --accounts "<ACCOUNT_ID>"
```
- `sourceName` and `regions` are required; if you omit `accounts` the command applies to every account in the
  organization. Applying to a Region where Security Lake is not enabled returns an error.
- Except for CloudTrail management events, you do not need to configure logging in these services separately, and
  existing logging is unaffected: Security Lake pulls from an independent, duplicated stream of events.
- Adding a source needs permissions such as `glue:CreateDatabase`, `glue:CreateTable`, `iam:CreateServiceLinkedRole`,
  `s3:GetObject`, `s3:PutObject` (and `kms:DescribeKey` if a KMS key is used).
- Removing a source stops collection; subscribers can still read data collected before removal.
- Choosing a newer source version requires updating subscriber settings so subscribers ingest that version.

## 3. Custom sources
A custom source must convert data to OCSF before sending. Requirements from the docs:
- Format: Apache Parquet objects; the same OCSF event class for every record in an object; deliver each OCSF event
  class as a separate source. Zstandard compression preferred; data page size at most 1 MB uncompressed; row group at
  most 256 MB compressed. Records ordered by time.
- Partitioning: `.../ext/<custom-source-name>/region=<region>/accountId=<ACCOUNT_ID>/eventDay=YYYYMMDD/`. `eventDay` is
  the UTC date of the record. For accounts outside AWS use a string such as `external` or `external_<id>`.
- Object rate: send files at intervals between 5 minutes and 1 event day (more often only if files exceed 256 MB).
- Up to 50 custom log sources per account; custom sources support OCSF 1.3 and earlier.
- Security Lake provides a unique S3 prefix, an IAM role for the source to write, a Lake Formation table and a Glue
  crawler. The role is named `AmazonSecurityLake-Provider-<custom source name>-<region>`.
- Via API or CLI you also create an IAM role for the Glue crawler (with `AWSGlueServiceRole` attached); the console
  does this for you.

## 4. Subscribers
- **Data access:** notified of new objects as they are written; by default through an HTTPS endpoint you provide, or
  alternatively by polling an SQS queue.
- **Query access:** query the Lake Formation tables directly with services such as Athena.
- Access is per source and per Region chosen at creation; use a rollup Region to give access to several Regions.
  A subscriber can have at most 10 sources (AWS and custom combined).
```bash
aws securitylake create-subscriber --subscriber-name <NAME> \
  --sources '[{"awsLogSource":{"sourceName":"CLOUD_TRAIL_MGMT","sourceVersion":"2.0"}}]' \
  --subscriber-identity principal=<SUBSCRIBER_ACCOUNT_ID>,externalId=<EXTERNAL_ID> \
  --access-types S3
```
`--access-types` takes `S3` (data access) or `LAKEFORMATION` (query access).

## Verify
- [ ] `aws securitylake get-data-lake-sources` shows the planned sources enabled for the accounts in each Region.
- [ ] A data access subscriber receives notifications for new objects.
- [ ] Custom source objects follow the partition path and Parquet requirements above.
- [ ] Lifecycle and retention match the logging policy.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the four cited Security Lake User Guide pages (overview, AWS sources, custom sources, subscriber
management) and the botocore securitylake model (command and field names, `sourceName` enum, access types).
Removed claims the pages do not give: the Athena table names and SQL example, partition column names for querying,
the Resource Access Manager sharing step, cost statements, named SIEM products, and the statement that S3 access alone
shows files rather than tables. Account IDs replaced with placeholders.
