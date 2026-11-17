---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-streaming-ingestion-kinesis-msk
name: redshift-streaming-ingestion-kinesis-msk
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, streaming-ingestion, kinesis-data-streams, msk, materialized-views]
level: advanced
status: docs-checked
description: "Ingest Kinesis Data Streams and MSK topics directly into Redshift with streaming ingestion: external schema, streaming materialized view, refresh and retention."
sources: ["https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html", "https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion-getting-started.html", "https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion-getting-started-MSK.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming ingestion from Kinesis and MSK

## 1. Kinesis Data Streams
```sql
CREATE EXTERNAL SCHEMA kds FROM KINESIS IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/redshift-streaming';

CREATE MATERIALIZED VIEW mv_clicks AUTO REFRESH YES AS
SELECT approximate_arrival_timestamp,
       partition_key,
       JSON_PARSE(kinesis_data) AS payload
FROM kds."clickstream"
WHERE CAN_JSON_PARSE(kinesis_data);
```
Role permissions: `kinesis:DescribeStreamSummary`, `GetShardIterator`, `GetRecords`, `ListShards`,
`DescribeStream`, `kinesis:ListStreams` (on `*`), plus `kms:Decrypt` for encrypted streams. The role trusts
Redshift and is associated with the cluster or workgroup. No authentication type is needed for Kinesis;
the role in `CREATE EXTERNAL SCHEMA` signs the requests. Optionally add `REGION '<region>'` to the schema for a
stream in another Region. The default refresh is manual; `AUTO REFRESH YES` turns on auto refresh. Redshift needs a
route to Kinesis (NAT or internet gateway, or a Kinesis interface VPC endpoint). Stream names are case sensitive; set
`enable_case_sensitive_identifier` to true for uppercase names.

## 2. MSK
```sql
CREATE EXTERNAL SCHEMA msk FROM KAFKA IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/redshift-streaming'
AUTHENTICATION iam
URI 'b-1.<cluster>.<id>.<kafka-host>:9098,b-2.<cluster>.<id>.<kafka-host>:9098';
CREATE MATERIALIZED VIEW mv_orders AUTO REFRESH YES AS
SELECT kafka_partition, kafka_offset, kafka_timestamp, JSON_PARSE(kafka_value) AS payload
FROM msk."orders";
```
`AUTHENTICATION` is `none` (unauthenticated MSK access, port 9092), `iam` (MSK only, port 9098) or `mtls`
(port 9094, with `AUTHENTICATION_ARN` for an ACM certificate or `SECRET_ARN` for a Secrets Manager secret).
MSK username and password authentication is not supported. The `URI` lists the bootstrap brokers. Metadata
columns include `kafka_partition`, `kafka_offset`, `kafka_timestamp_type`, `kafka_timestamp`, `kafka_key` and
`kafka_value`. Redshift needs a network path to the brokers (same VPC or routable). Topic names are case
sensitive and at most 128 characters.

## 3. Operating it
- Manual `REFRESH MATERIALIZED VIEW` gives control; auto refresh is opt-in.
- If refresh falls behind longer than stream retention, data is lost; keep retention well above worst-case lag.
- Records larger than the VARBYTE maximum (16 MiB; Kinesis itself caps records at 10 MiB, needing patch 203 or later,
  otherwise older views stay at 1 MiB) are skipped, the refresh still succeeds, and a segment of each is written to
  `SYS_STREAM_SCAN_ERRORS`. Business-logic or type-conversion errors are not skipped and can block ingestion, so keep
  the view definition simple.
- Use `JSON_PARSE` into SUPER rather than `JSON_EXTRACT_PATH_TEXT` per column (each extracted column re-parses the JSON).
- Create one materialized view per stream or topic (each creates a consumer per shard or partition). JOINs are not
  supported on a streaming materialized view; build downstream MVs or scheduled `INSERT INTO ... SELECT` for joins and typed tables.
- KPL-aggregated records are ingested but not parsed (binary protocol buffers); compressed records cannot be queried.

## Verify
- [ ] `SELECT max(approximate_arrival_timestamp) FROM mv_clicks;` stays close to the current time under load (set your own latency target).

## Checked

2026-10-27, AWS documentation (current release as read on that date). Amazon Redshift Database Developer Guide streaming ingestion overview, Kinesis getting-started and MSK getting-started pages. Fixed: the MSK external schema uses FROM KAFKA with AUTHENTICATION and a URI broker list (the skill used FROM MSK and CLUSTER_ARN, which the pages do not show); the VARBYTE record limit is 16 MiB (Kinesis records cap at 10 MiB with patch 203 or later; older views stay at 1 MiB), not 1 MB; JOINs are not supported on streaming views; username and password MSK auth is unsupported. Confirmed: Kinesis IAM actions, metadata column names, manual refresh by default, AUTO REFRESH YES, SYS_STREAM_SCAN_ERRORS, one view per stream guidance. Removed the unsourced seconds-level refresh latency claim.
Method: documentation only; no commands were run.
