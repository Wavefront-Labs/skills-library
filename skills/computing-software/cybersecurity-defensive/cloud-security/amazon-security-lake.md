---
id: computing-software.cybersecurity-defensive.cloud-security.amazon-security-lake
name: amazon-security-lake
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-detection, amazon-security-lake, ocsf, security-data-lake, subscriber-access, athena-queries, log-centralisation]
level: practitioner
status: docs-checked
description: "Deploy Amazon Security Lake across an AWS organisation: delegated admin, sources, rollup Regions, OCSF Parquet data and data or query access subscribers."
sources: ["https://docs.aws.amazon.com/security-lake/latest/userguide/internal-sources.html", "https://docs.aws.amazon.com/security-lake/latest/userguide/add-rollup-region.html", "https://docs.aws.amazon.com/security-lake/latest/userguide/subscriber-data-access.html", "https://docs.aws.amazon.com/security-lake/latest/userguide/subscriber-query-access.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon Security Lake

**Goal:** a central, OCSF-normalised security data lake in your Log Archive/security account that SIEMs and analysts query without each team copying logs.

## Setup
1. Designate a delegated administrator (typically the Log Archive or security tooling account) from the management account: `aws securitylake register-data-lake-delegated-administrator --account-id <id>`.
2. Create the data lake in the Regions you need, and optionally add a **rollup Region**: it consolidates data from one or more contributing Regions (useful for Regional compliance). Before adding one you must create two IAM roles, one for data replication and one so a Lambda function can register AWS Glue partitions for replicated objects (without it subscribers cannot query those objects). The replication role name must start with `SecurityLake`, and `AmazonSecurityLakeMetaStoreManager` must be granted as a Lake Formation data lake administrator.
3. Enable AWS sources per account and Region: CloudTrail management and data events (S3, Lambda), EKS audit logs, Route 53 resolver query logs, Security Hub CSPM findings, VPC Flow Logs and WAFv2 logs. Security Lake pulls from an independent, duplicated stream of events, so you do not change existing logging, except that CloudTrail management events must be configured. You can ingest only the latest source version and disable earlier ones.
4. Custom sources can add third-party data (see the custom sources page in the user guide).

## Data format
Security Lake transforms source data into the Open Cybersecurity Schema Framework (OCSF) in Apache Parquet format, registered in AWS Glue and Lake Formation.

## Subscribers
- **Data access subscribers** (`S3` in the `accessTypes` parameter of `CreateSubscriber`) read S3 objects directly and are notified of new objects through an HTTPS endpoint they provide (default) or by polling an SQS queue. Use for SIEMs.
- **Query access subscribers** (`LAKEFORMATION` access type) query Lake Formation tables in your S3 bucket with Athena (the primary engine) or other Glue Data Catalog engines such as Redshift Spectrum and Spark SQL.

## Gotchas
- Lake Formation permissions are needed in addition to S3/IAM for querying; data-access errors are often Lake Formation grants.
- Costs scale with ingested volume (data events, flow logs); enable sources selectively and see the Security Lake pricing page.
- Filter Athena queries on partition columns to control scan cost.

## Verify
- [ ] All org accounts and Regions show sources enabled in the Security Lake console.
- [ ] A subscriber (SIEM) receives new objects within the expected delay.
- [ ] An Athena query on a CloudTrail table returns today's events.

## Checked
Checked 2026-11-09 against the Security Lake User Guide pages in `sources` (sources list, OCSF/Parquet transformation, rollup Regions and required roles, data and query access subscriber types); the CLI command name was verified with the command checker. Removed unconfirmed claims: Glue database and table naming, the sample SQL query, OCSF 1.1 for source version 2, lifecycle and KMS options, and the CloudTrail service-linked channel remark.
Method: documentation only; no commands were run.
