---
id: computing-software.ai-ml-engineering.mlops.deequ-and-glue-data-quality
name: deequ-and-glue-data-quality
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, deequ, glue-data-quality, pydeequ, dqdl, data-validation]
level: practitioner
status: docs-checked
description: "Validate large datasets on Spark with Deequ/PyDeequ checks, metrics repositories and anomaly detection, or AWS Glue Data Quality DQDL rulesets inside Glue jobs."
sources:
  - https://github.com/awslabs/deequ
  - https://github.com/awslabs/python-deequ
  - https://docs.aws.amazon.com/glue/latest/dg/dqdl.html
  - https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deequ and Glue Data Quality at scale

**Goal:** billion-row training and scoring inputs are checked on Spark before use, with failures stopping the pipeline and metrics tracked over time.

## PyDeequ checks
```python
import os; os.environ["SPARK_VERSION"] = "3.5"
import pydeequ
from pydeequ.checks import Check, CheckLevel
from pydeequ.verification import VerificationSuite, VerificationResult
spark = (SparkSession.builder.config("spark.jars.packages", pydeequ.deequ_maven_coord)
         .config("spark.jars.excludes", pydeequ.f2j_maven_coord).getOrCreate())

check = (Check(spark, CheckLevel.Error, "orders")
         .hasSize(lambda n: n > 1_000_000)
         .isComplete("order_id").isUnique("order_id")
         .isNonNegative("amount")
         .isContainedIn("status", ["open", "shipped", "cancelled"]))
result = VerificationSuite(spark).onData(df).addCheck(check).run()
VerificationResult.checkResultsAsDataFrame(spark, result).show(truncate=False)
```
Fail the pipeline on any failed check result from the checks dataframe; `CheckLevel.Warning` is the lower severity level.

## Metrics over time and anomalies
Deequ supports anomaly detection on data quality metrics over time: store metrics in a metrics repository (`FileSystemMetricsRepository`) and add an anomaly check on dataset size, catching "today's partition is half the usual size" which fixed thresholds miss. See the README for the exact strategy classes. `ConstraintSuggestionRunner` proposes initial constraints from a sample; review them, do not adopt blindly.

## Glue Data Quality (DQDL)
```
Rules = [
  RowCount > 1000000,
  IsComplete "order_id",
  IsUnique "order_id",
  ColumnValues "amount" >= 0,
  ColumnValues "status" in ["open", "shipped", "cancelled"],
  Completeness "email" >= 0.95,
  Freshness "updated_at" <= 24 hours
]
```
- Attach the ruleset to a Data Catalog table, or evaluate inside a Glue ETL job with the `EvaluateDataQuality` transform.
- Results publish to CloudWatch and EventBridge; use them to alert or block downstream jobs.
- Rule recommendations are supported for Data Catalog data quality, not for ETL job data quality.

## Choosing
Deequ: runs on Spark, programmatic control, open source. Glue Data Quality: managed, DQDL readable by data owners, integrated with the catalog. Great Expectations/Pandera fit smaller pandas-scale data.

## Verify
- [ ] An injected bad partition (nulls in keys, duplicates) fails the gate and halts training.
- [ ] Metrics history exists for trend and anomaly checks.

## Checked
2026-11-01. Confirmed against the awslabs/deequ and python-deequ READMEs and the AWS Glue Data Quality and DQDL pages: PyDeequ check methods, SPARK_VERSION and Maven coordinates, ConstraintSuggestionRunner, FileSystemMetricsRepository, anomaly detection over time, EvaluateDataQuality, DQDL rules, CloudWatch and EventBridge integration, recommendations Catalog-only. Removed: hasCompleteness, the named anomaly strategy, scan-count claim, row routing, FAILED status wording.
Method: documentation only; no commands were run.
