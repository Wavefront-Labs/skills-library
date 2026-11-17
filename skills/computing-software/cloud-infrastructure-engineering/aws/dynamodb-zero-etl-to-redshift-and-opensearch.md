---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-zero-etl-to-redshift-and-opensearch
name: dynamodb-zero-etl-to-redshift-and-opensearch
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, dynamodb-zero-etl, zero-etl, redshift, opensearch-ingestion]
level: advanced
status: docs-checked
description: "Replicate DynamoDB tables to Redshift with zero-ETL integrations and to OpenSearch with OpenSearch Ingestion pipelines, including PITR, policies and data shape."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/RedshiftforDynamoDB-zero-etl.html", "https://github.com/opensearch-project/documentation-website/blob/main/_data-prepper/pipelines/configuration/sources/dynamo-db.md", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json", "https://github.com/boto/botocore/blob/develop/botocore/data/redshift/2012-12-01/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamoDB zero-ETL to Redshift and OpenSearch

## 1. Redshift
Behaviour: on activation the integration exports the full table, then replicates updates incrementally every
15-30 minutes using DynamoDB incremental exports. The table and the Redshift cluster or serverless namespace must
be in the same Region, and the source table must be encrypted with an Amazon-owned or customer managed KMS key
(the AWS managed key is not supported).
Prerequisites:
- Point-in-time recovery enabled on the table.
- A resource-based policy attached to the table that lets `redshift.amazonaws.com` call
  `dynamodb:ExportTableToPointInTime` and `dynamodb:DescribeTable` (and `dynamodb:DescribeExport` on
  `table/<name>/export/*`), conditioned on `aws:SourceAccount` and an `aws:SourceArn` of
  `arn:aws:redshift:<REGION>:<ACCOUNT_ID>:integration:*`. Within one account the console option "Fix it for
  me" applies the policies; across accounts you attach this policy yourself.
- The creating identity needs `dynamodb:GetResourcePolicy`, `dynamodb:PutResourcePolicy`,
  `dynamodb:UpdateContinuousBackups`, `redshift:CreateIntegration` and related Redshift permissions; whoever
  configures the target namespace needs `redshift:PutResourcePolicy`, `DeleteResourcePolicy` and
  `GetResourcePolicy`.
- If the table uses a customer managed KMS key, the key policy must allow `redshift.amazonaws.com` to
  `kms:Decrypt` with the same source conditions.
```bash
aws redshift create-integration --integration-name orders-zetl \
  --source-arn arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/orders \
  --target-arn arn:aws:redshift-serverless:<REGION>:<ACCOUNT_ID>:namespace/<NAMESPACE_ID>
```
`CreateIntegration` takes `SourceArn`, `TargetArn` and `IntegrationName`. After the integration is active,
create the destination database in Redshift from the integration ID as described in the Redshift zero-ETL guide
and query the replicated table there; the Redshift guide documents the target schema and the Redshift settings
required (for example the case-sensitivity setting), so follow it rather than a hand-written query.

## 2. OpenSearch
OpenSearch Ingestion (Data Prepper) pipeline with a `dynamodb` source: an initial export to S3 using
point-in-time recovery, then DynamoDB Streams, then a sink into an index:
```yaml
version: "2"
ddb-pipeline:
  source:
    dynamodb:
      tables:
        - table_arn: "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/orders"
          stream: {start_position: "LATEST"}
          export: {s3_bucket: "osis-exports-<ACCOUNT_ID>", s3_region: "<REGION>"}
      aws: {sts_role_arn: "arn:aws:iam::<ACCOUNT_ID>:role/osis-ddb", region: "<REGION>"}
  sink:
    - opensearch:
        hosts: ["https://search-orders-xxxx.<REGION>.es.amazonaws.com"]
        index: "orders"
        document_id: '${getMetadata("primary_key")}'
        action: '${getMetadata("opensearch_action")}'
        aws: {sts_role_arn: "arn:aws:iam::<ACCOUNT_ID>:role/osis-ddb", region: "<REGION>"}
```
- The export option needs point-in-time recovery; the stream option needs DynamoDB Streams enabled on the
  table. The role needs `dynamodb:DescribeTable`, `DescribeContinuousBackups`, `ExportTableToPointInTime`,
  `DescribeExport`, stream read actions and S3 access to the export bucket; when reading streams only, the export
  and S3 statements are not required.
- Metadata exposed by the source includes `primary_key` (partition key, or `partition|sort`), `opensearch_action`
  (`index` for export items; for stream events `INSERT`/`MODIFY` or `delete` for `REMOVE`), `document_version`
  and `ttl_delete` (true for TTL-based removals).
- `view_on_remove` (`NEW_IMAGE` or `OLD_IMAGE`, default `NEW_IMAGE`) selects the stream view used for REMOVE events.
- One Data Prepper instance processes up to 150 stream shards in parallel.

## Verify
- [ ] Row/doc counts match the table item count after initial load; allow the documented replication interval
  for Redshift (15-30 minutes) before checking a test update there.

## Checked
Checked 2026-10-24 against the DynamoDB guide page "DynamoDB zero-ETL integration with Amazon Redshift", the
OpenSearch Data Prepper `dynamodb` source documentation and the botocore models. Corrected: the old text said
changes arrive "within minutes"; the page says incremental replication every 15-30 minutes. Confirmed: PITR
requirement, resource policy principal, actions and conditions, same-Region and KMS limitations, identity
permissions, `CreateIntegration` parameters, and the Data Prepper option names (`tables`, `table_arn`, `export`,
`s3_bucket`, `s3_region`, `stream`, `start_position`, `view_on_remove`, `aws.sts_role_arn`, `aws.region`) and
metadata attributes. Removed unchecked details: the `value` SUPER column layout and sample SQL, the
Redshift RA3-only wording, the `enable_case_sensitive_identifier` instruction (deferred to the Redshift guide),
and the specific stream view requirement for the pipeline.
Method: documentation only; no commands were run.
