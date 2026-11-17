---
id: computing-software.cloud-infrastructure-engineering.aws.timestream-for-influxdb
name: timestream-for-influxdb
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, timestream, timestream-influxdb, influxdb, time-series, telegraf]
level: advanced
status: docs-checked
description: "Run managed InfluxDB with Amazon Timestream for InfluxDB: create instances, Multi-AZ standby, credentials and tokens, Telegraf ingestion and choosing it over LiveAnalytics."
sources: ["https://docs.aws.amazon.com/timestream/latest/developerguide/timestream-for-influxdb.html", "https://docs.aws.amazon.com/timestream/latest/developerguide/timestream-for-influx-getting-started-creating-db-instance.html", "https://docs.aws.amazon.com/cli/latest/reference/timestream-influxdb/create-db-instance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestream for InfluxDB

## 1. When
Managed InfluxDB: it runs InfluxDB databases using the open-source APIs, so existing InfluxDB workloads, Telegraf and
Grafana setups can move over. Compare it with Timestream for LiveAnalytics in the Timestream developer guide before choosing.

## 2. Create
```bash
aws timestream-influxdb create-db-instance --name metrics-prod \
  --db-instance-type db.influx.large --db-storage-type InfluxIOIncludedT1 --allocated-storage 400 \
  --deployment-type WITH_MULTIAZ_STANDBY \
  --vpc-subnet-ids subnet-a subnet-b --vpc-security-group-ids sg-influx --no-publicly-accessible \
  --username admin --password '<PASSWORD>' --organization acme --bucket telemetry
aws timestream-influxdb get-db-instance --identifier <ID> --query '{status:status,endpoint:endpoint}'
```
- The initial admin credentials (organization, bucket, username, password) are stored in a Secrets Manager secret
  (`influxAuthParametersSecretArn`); use the password to reach the InfluxDB UI and create an operator token.
- `--db-storage-type` is one of three Influx IO Included tiers (3000, 12000 or 16000 IOPS); `--deployment-type` is
  `SINGLE_AZ` or `WITH_MULTIAZ_STANDBY`, which creates a standby in another AZ for failover (give at least two subnets
  in different AZs).
- The default InfluxDB port is 8086.
- A DB parameter group (`--db-parameter-group-identifier`) sets configuration such as the query concurrency limit.

## 3. Tokens and ingestion
Create scoped write tokens per writer with the InfluxDB UI or CLI using the operator token, and keep the operator
token in Secrets Manager. Point Telegraf's InfluxDB v2 output at `https://<ENDPOINT>:8086` with your organization,
bucket and token.

## 4. Operations
Retention is set per bucket (a bucket combines a database and a retention period).

## Verify
- [ ] Writes from Telegraf appear in the bucket (query it from the InfluxDB UI).

## Checked

2026-10-28. Confirmed against the Timestream developer guide pages timestream-for-influxdb and the creating-a-DB-instance guide, and the CLI reference for `aws timestream-influxdb create-db-instance`: flag names, instance types, the three Influx IO Included storage tiers, deployment types, Multi-AZ standby for failover, the Secrets Manager secret, parameter groups, default port 8086, and per-bucket retention.
Removed: the "single-digit millisecond" and LiveAnalytics-suits-serverless comparison, the price-trade-off wording, the `influx auth create`, `influx backup/restore` and Telegraf config snippets, and downsampling-task advice (InfluxDB product docs, not fetched).
Method: documentation only; no commands were run.
