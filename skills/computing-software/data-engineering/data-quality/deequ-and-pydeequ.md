---
id: computing-software.data-engineering.data-quality.deequ-and-pydeequ
name: deequ-and-pydeequ
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, deequ, pydeequ, spark-data-quality, verification-suite, metrics-repository, constraint-suggestion, anomaly-detection]
level: practitioner
status: docs-checked
description: "Validate Spark DataFrames at scale with Deequ/PyDeequ: VerificationSuite checks, a metrics repository for history, anomaly checks and constraint suggestion."
sources:
  - https://github.com/awslabs/deequ
  - https://github.com/awslabs/python-deequ
  - https://aws.amazon.com/blogs/big-data/test-data-quality-at-scale-with-deequ/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deequ and PyDeequ

**Goal:** declarative data quality checks computed in one pass over large Spark datasets, with metric history for trend/anomaly checks.

## Setup
Deequ is a Scala library; PyDeequ wraps it. Set `SPARK_VERSION` to match your Spark runtime before importing PyDeequ (the README names 3.5 and 4.1; PyDeequ 1.6.0 is the last release supporting Spark 3.1-3.4):
```python
import os; os.environ["SPARK_VERSION"] = "3.5"
import pydeequ
spark = (SparkSession.builder
         .config("spark.jars.packages", pydeequ.deequ_maven_coord)
         .config("spark.jars.excludes", pydeequ.f2j_maven_coord).getOrCreate())
```

## Checks
```python
from pydeequ.checks import Check, CheckLevel
from pydeequ.verification import VerificationSuite, VerificationResult

check = (Check(spark, CheckLevel.Error, "orders")
  .hasSize(lambda n: n > 100_000)
  .isComplete("order_id").isUnique("order_id")
  .isComplete("customer_id")
  .isNonNegative("amount")
  .isContainedIn("status", ["NEW", "PAID", "SHIPPED", "CANCELLED"])
  .hasCompleteness("email", lambda c: c >= 0.95)
  .satisfies("shipped_at IS NULL OR shipped_at >= ordered_at", "ship after order", lambda r: r == 1.0))

result = VerificationSuite(spark).onData(df).addCheck(check).run()
VerificationResult.checkResultsAsDataFrame(spark, result).show(truncate=False)
if result.status != "Success":
    raise ValueError("DQ failed")
```
All constraints compile to aggregations computed in a minimal number of scans.

## Metrics repository and anomaly detection
Deequ can store metrics in a metrics repository (PyDeequ: `FileSystemMetricsRepository`) and run anomaly checks on metrics that change over time; see the PyDeequ README for the repository and anomaly-detection API.

## Constraint suggestion (bootstrap)
```python
from pydeequ.suggestions import ConstraintSuggestionRunner, DEFAULT
s = ConstraintSuggestionRunner(spark).onData(df).addConstraintRule(DEFAULT()).run()
```
Review suggestions; do not adopt blindly (they encode today's data, including today's bugs).

## Gotchas
- PyDeequ lags Spark releases; check compatibility before upgrading Spark.
- `isUnique` on huge high-cardinality columns is a full shuffle; schedule accordingly.
- Persist results (check results DataFrame) to a table for dashboards, not just logs.

## Verify
- [ ] Pipeline step fails on Error-level check failures and stores results per run.
- [ ] Metrics history populated; an anomaly check on a synthetic load fires.

## Checked

2026-10-28. Confirmed in the PyDeequ README and the AWS Deequ blog: `SPARK_VERSION` handling and the supported Spark versions, `FileSystemMetricsRepository`, `ConstraintSuggestionRunner`, check methods `hasCompleteness`, `isContainedIn`, `isNonNegative`; the blog also states that anomaly detection runs on metrics that change over time. Removed: the PyDeequ anomaly-detection code (`RelativeRateOfChangeStrategy`, `addAnomalyCheck`; not found in the pages) and the AWS Glue Data Quality and EMR claims.

Method: documentation only; no commands were run.
