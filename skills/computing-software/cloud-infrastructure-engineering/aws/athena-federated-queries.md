---
id: computing-software.cloud-infrastructure-engineering.aws.athena-federated-queries
name: athena-federated-queries
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, athena, federated-query, athena-connectors, lambda-connector, data-source-connector, glue-connections, passthrough-query, spill-bucket, query-federation-sdk, cross-source-join, dynamodb-query, rds-query]
level: advanced
status: docs-checked
description: "Query DynamoDB, PostgreSQL, Redshift and other sources from Athena via federated connectors: register catalogs, passthrough queries, VPC and Secrets Manager, case modes."
sources: ["https://docs.aws.amazon.com/athena/latest/ug/connect-to-a-data-source.html", "https://docs.aws.amazon.com/athena/latest/ug/connectors-available.html", "https://docs.aws.amazon.com/athena/latest/ug/federated-query-passthrough.html", "https://docs.aws.amazon.com/athena/latest/ug/connect-to-a-data-source-lambda.html", "https://github.com/awslabs/aws-athena-query-federation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Athena federated queries

**Goal:** analysts join S3 data-lake tables with live operational data (a DynamoDB table, a
PostgreSQL database, CloudWatch Logs) in one SQL statement, without building an ETL job
for every ad-hoc question — and know when that is the wrong tool.

## 1. How it works
A **data source connector** is built with the Athena Query Federation SDK and registered in
Athena as a **data catalog**. Prebuilt connectors exist for DynamoDB, MySQL, PostgreSQL, SQL Server,
Oracle, Redshift, OpenSearch, CloudWatch and CloudWatch metrics, DocumentDB, HBase, Snowflake,
Google BigQuery, SAP HANA and more (see the available-connectors page).

## 2. Deploy a connector
Configure and deploy the connector in your account (see "Use Amazon Athena Federated Query"),
then register the Lambda function as a catalog:
```bash
aws athena create-data-catalog --name pg_orders --type LAMBDA \
  --parameters function=arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:athena-pg-orders
```
Connector prerequisites:
- Some prebuilt connectors need a VPC and a security group before you can use them.
- To use federated queries with Secrets Manager you must configure an Amazon VPC private
  endpoint for Secrets Manager.
- Catalog types accepted by `create-data-catalog` are `LAMBDA`, `GLUE`, `HIVE` and `FEDERATED`.

## 3. Query
```sql
SELECT o.order_id, o.status, c.segment
FROM pg_orders.public.orders o
JOIN awsdatacatalog.lake.customers c ON c.customer_id = o.customer_id
WHERE o.created_at > current_date - interval '1' day;

-- DynamoDB via its connector
SELECT * FROM "ddb"."default"."sessions" WHERE pk = 'user#42';

-- passthrough: send native SQL to the source, avoid pulling whole tables
SELECT * FROM TABLE(pg_orders.system.query(
  query => 'SELECT customer_id, count(*) n FROM orders WHERE created_at > now() - interval ''1 day'' GROUP BY 1'));
```
Predicate pushdown is connector-dependent: for connectors that do not support it, queries with a
predicate take longer and can time out on large datasets. Passthrough queries (below) send the full
query to the source; they use `TABLE(catalog.system.query(query => '...'))`, and the supported
connectors include DynamoDB, MySQL, Oracle, PostgreSQL and Redshift.

## 4. Permissions
See the Athena federated query documentation for the IAM permissions of users and of the connector's
Lambda role; grant the connector only read access to the source.

## Gotchas
- A careless `SELECT *` on a production DB hits the primary; point connectors at **read
  replicas**. Long-running heavy joins belong in an ETL into S3.
- Identifier case: the Federation SDK has case resolver modes `NONE`, `LOWER`, `UPPER`,
  `ANNOTATION` (existing Snowflake and SAP HANA connectors only) and `CASE_INSENSITIVE_SEARCH`.
  In `LOWER` mode the schema and all its tables must be lowercase; Glue integration works only with
  `NONE` or `LOWER`.
- Connectors are updated periodically; data sources at end-of-life are not supported.

## Verify
- [ ] `SHOW DATABASES IN pg_orders` lists schemas; a small query returns rows.
- [ ] Query with a filter shows reduced "data scanned" vs unfiltered (pushdown working).
- [ ] Source DB CPU during a test query stays within budget (read replica used).

## Checked
2026-10-31. Confirmed in the Athena available-connectors page, the passthrough-queries page and the botocore athena model: connector names, VPC/security group and Secrets Manager private endpoint prerequisites, pushdown behaviour, case resolver modes and limits, passthrough syntax and supported connectors, `create-data-catalog` types. Removed as unconfirmed (the Lambda connector page was a stub): spill bucket settings, the connection string format, Glue-connection flow, IAM permissions, Lake Formation behaviour, the 15-minute Lambda limit, cost formula and SAR version drift.
Method: documentation only; no commands were run.
