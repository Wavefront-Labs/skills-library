---
id: computing-software.data-engineering.snowflake.stages-and-storage-integrations
name: stages-and-storage-integrations
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-stages, storage-integration, external-stage, internal-stage, put-command, list-stage, s3-iam-role, directory-table, copy-into]
level: practitioner
status: docs-checked
description: "Set up Snowflake stages: storage integrations with an IAM role (no keys), external stages on S3/GCS/Azure, internal stages with PUT, LIST and directory tables."
sources:
  - https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration
  - https://docs.snowflake.com/en/sql-reference/sql/create-stage
  - https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stages and storage integrations

**Goal:** Snowflake can read/write your cloud storage securely (no access keys in SQL), and loads reference stages by name.

## Storage integration (S3 example)
```sql
create storage integration s3_landing
  type = external_stage
  storage_provider = 'S3'
  enabled = true
  storage_aws_role_arn = 'arn:aws:iam::<acct>:role/snowflake-landing-read'
  storage_allowed_locations = ('s3://<BUCKET>/landing/');

desc integration s3_landing;   -- note STORAGE_AWS_IAM_USER_ARN and STORAGE_AWS_EXTERNAL_ID
```
In AWS, set the role's trust policy to allow that IAM user ARN and external ID, and grant the role `s3:GetBucketLocation`, `s3:GetObject`, `s3:GetObjectVersion` and `s3:ListBucket` (the docs list extra permissions for unload and purge).
Only ACCOUNTADMIN (or a role with CREATE INTEGRATION) creates integrations; grant `usage` on it to the loader role.

## External stage
```sql
create stage raw.landing.orders_stage
  url = 's3://<BUCKET>/landing/orders/'
  storage_integration = s3_landing
  file_format = (type = parquet)
  directory = (enable = true auto_refresh = true);   -- optional directory table
list @raw.landing.orders_stage pattern = '.*2026-10-15.*';
select * from directory(@raw.landing.orders_stage);    -- file metadata as a table
```

## Internal stages
- User stage `@~`, table stage `@%orders`, named internal stage `create stage raw.landing.uploads;`.
- Upload from a client with `PUT file:///data/orders_*.csv @raw.landing.uploads;`; download with `GET`, clean up with `REMOVE`.

## Permissions
- Grant stage privileges to loader roles, not users.
- Restrict `storage_allowed_locations`/`storage_blocked_locations` to exact prefixes; one integration per trust boundary.

## Verify
- [ ] `list @stage` works for the loader role and fails for others.

## Checked
2026-10-28. Confirmed against the Snowflake S3 storage integration and stage pages (CREATE STORAGE INTEGRATION TYPE = EXTERNAL_STAGE, STORAGE_ALLOWED_LOCATIONS and STORAGE_BLOCKED_LOCATIONS, STORAGE_AWS_IAM_USER_ARN and external ID in DESC output, S3 permissions, CREATE INTEGRATION privilege, DIRECTORY = (ENABLE, AUTO_REFRESH) parameters). Removed: sts:ExternalId wording, GCS/Azure remark, PUT options and the web UI limitation, the stage privilege list and the three gotchas (credentials in query history, trailing slash, cross-region egress).
Method: documentation only; no commands were run.
