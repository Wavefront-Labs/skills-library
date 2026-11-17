---
id: computing-software.cloud-infrastructure-engineering.aws.glue-data-quality-and-schema-registry
name: glue-data-quality-and-schema-registry
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, glue, glue-data-quality, dqdl, data-quality-rules, evaluate-data-quality, glue-schema-registry, schema-evolution, avro, compatibility-mode, kafka-serde, kinesis-schema, data-contracts]
level: advanced
status: docs-checked
description: "Enforce data contracts in AWS Glue: DQDL rulesets on catalog tables and in ETL jobs with quarantine and alerts, and Schema Registry compatibility for Kafka/Kinesis producers."
sources: ["https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html", "https://docs.aws.amazon.com/glue/latest/dg/dqdl.html", "https://docs.aws.amazon.com/glue/latest/dg/data-quality-gs-studio-notebooks.html", "https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html", "https://docs.aws.amazon.com/glue/latest/dg/schema-registry-integrations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Glue Data Quality and Schema Registry

**Goal:** bad data is caught at the boundary — producers cannot publish an incompatible
schema to a stream, and batch pipelines stop or quarantine rows that break the contract
before they reach consumers.

## 1. Data Quality Definition Language (DQDL)
```
Rules = [
  RowCount > 1000,
  IsComplete "order_id",
  IsUnique "order_id",
  ColumnValues "status" in ["NEW","PAID","SHIPPED","CANCELLED"],
  ColumnValues "amount" between 0 and 100000,
  Completeness "customer_id" >= 0.99,
  ColumnLength "country" = 2
]
```
Rule recommendations: `aws glue start-data-quality-rule-recommendation-run --data-source GlueTable={DatabaseName=sales,TableName=orders} --role <ROLE>`
profiles the table and proposes rules — review, do not accept blindly.

## 2. Rulesets on catalog tables
```bash
aws glue create-data-quality-ruleset --name orders-contract --ruleset file://orders.dqdl \
  --target-table TableName=orders,DatabaseName=sales
aws glue start-data-quality-ruleset-evaluation-run --role <ROLE> \
  --data-source GlueTable={DatabaseName=sales,TableName=orders} --ruleset-names orders-contract \
  --additional-run-options CloudWatchMetricsEnabled=true,ResultsS3Prefix=s3://dq-results/orders/
aws glue get-data-quality-result --result-id <ID>   # score, per-rule PASS/FAIL with evaluation message
```
Schedule runs (console or EventBridge Scheduler) after each load.

## 3. In ETL jobs (stop or quarantine)
```python
from awsgluedq.transforms import EvaluateDataQuality
results = EvaluateDataQuality().process_rows(frame=orders_dyf, ruleset=RULES,
    publishing_options={"dataQualityEvaluationContext": "orders", "enableDataQualityCloudWatchMetrics": True,
                        "enableDataQualityResultsPublishing": True},
    additional_options={"observations.scope": "ALL", "performanceTuning.caching": "CACHE_NOTHING"})
rows = SelectFromCollection.apply(dfc=results, key="rowLevelOutcomes")
good = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Passed")
bad  = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Failed")   # write to s3://quarantine/
```
Fail the job on rule-level failures for hard contracts, quarantine row-level failures
for soft ones. Alert from the CloudWatch metrics that `enableDataQualityCloudWatchMetrics` /
`CloudWatchMetricsEnabled` publish.

## 4. Schema Registry
```bash
aws glue create-registry --registry-name streaming
aws glue create-schema --registry-id RegistryName=streaming --schema-name orders-value \
  --data-format AVRO --compatibility BACKWARD --schema-definition file://orders-v1.avsc
aws glue register-schema-version --schema-id RegistryName=streaming,SchemaName=orders-value \
  --schema-definition file://orders-v2.avsc     # rejected if incompatible
aws glue check-schema-version-validity --data-format AVRO --schema-definition file://orders-v2.avsc
```
- Formats: Avro, JSON Schema, Protobuf. The 8 compatibility modes are `NONE`, `DISABLED`,
  `BACKWARD`, `BACKWARD_ALL`, `FORWARD`, `FORWARD_ALL`, `FULL`, `FULL_ALL`.
- Producers/consumers use the Glue Schema Registry serde libraries; the integration page
  shows `schemaAutoRegistrationEnabled` as a converter setting (set it false where only CI
  should register schemas).
- Documented integrations: MSK/Apache Kafka, Kinesis Data Streams (KPL/KCL in Java),
  Managed Service for Apache Flink, and Lambda.

## Gotchas
- DQDL `between x and y` is exclusive of both bounds, numeric and date types only.
- Row-level DQDL labels are disabled by default in row-level results; enable them through
  `additional_options` in `EvaluateDataQuality`.

## Verify
- [ ] Evaluation run on a known-bad sample fails the expected rules with clear messages.
- [ ] ETL job writes quarantined rows to S3 and the EventBridge alert fires.
- [ ] Registering an incompatible schema version (adding a field without a default under BACKWARD) is rejected.
- [ ] Consumer deserialises messages produced with both v1 and v2.

## Checked

2026-10-28. Confirmed against AWS documentation: DQDL rule types and syntax, EvaluateDataQuality options and rowLevelOutcomes, schema registry formats and eight compatibility modes, documented integrations; CLI flags via botocore.
Removed: CustomSql/primary and DataFreshness examples, EventBridge event name, serde class names, DPU cost/sampling advice, default-compatibility advice, wrong inclusive reading of between (it is exclusive).
Method: documentation only; no commands were run.
