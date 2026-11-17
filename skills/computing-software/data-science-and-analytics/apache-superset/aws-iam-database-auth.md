---
id: computing-software.data-science-and-analytics.apache-superset.aws-iam-database-auth
name: aws-iam-database-auth
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [aws-iam, aurora, redshift, secure-extra, sts]
level: advanced
status: docs-checked
description: "Connect Superset to Aurora and Redshift with AWS IAM auth: feature flag, IAM permissions, Secure Extra aws_iam keys, cross-account roles."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/aws-iam.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate to AWS databases without static passwords.

Prerequisites:
- `AWS_DATABASE_IAM_AUTH` set `True` under `FEATURE_FLAGS`; otherwise `aws_iam` connections fail.
- Install `boto3`.
- Permissions on the Superset role: Aurora `rds-db:connect`; Redshift provisioned `redshift:GetClusterCredentials`; Redshift Serverless `redshift-serverless:GetCredentials` and `redshift-serverless:GetWorkgroup`; cross-account `sts:AssumeRole`.
- SSL enabled on the endpoint.

Put settings in the connection's **Secure Extra** (Advanced > Security) under an `aws_iam` key.

Aurora PostgreSQL or MySQL: `enabled` (required, `true`), `region`, `db_username` (required), optional `role_arn` (cross-account, via STS), optional `external_id`, optional `session_duration` (seconds, default `3600`).

Redshift Serverless: `enabled`, `region`, `role_arn`, `workgroup_name`, `db_name`.

Redshift provisioned: `enabled`, `region`, `role_arn`, `cluster_identifier`, `db_username`, `db_name`.

Cross-account:
1. In the target account create a role with `rds-db:connect` on the DB user's ARN; its trust policy lets the Superset instance role call `sts:AssumeRole` with an `sts:ExternalId` condition.
2. In the Superset account allow the Superset role to `sts:AssumeRole` on that role's ARN.
3. Set `role_arn` and `external_id` in the connection to match.

STS credentials are cached in memory keyed by `(role_arn, region, external_id)` with a 10-minute TTL and refresh before expiry.

## Checked

2026-11-08. Confirmed against the AWS IAM Authentication page (read in full); no content changes needed.
Method: documentation only; no commands were run.
