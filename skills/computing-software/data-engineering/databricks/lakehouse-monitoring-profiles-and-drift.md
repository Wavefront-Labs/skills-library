---
id: computing-software.data-engineering.databricks.lakehouse-monitoring-profiles-and-drift
name: lakehouse-monitoring-profiles-and-drift
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, lakehouse-monitoring, data-profiling, drift-detection, quality-monitors, inference-log, custom-metrics, anomaly-detection, unity-catalog]
level: practitioner
status: docs-checked
description: "Set up Databricks data profiling (Lakehouse Monitoring): snapshot, time-series and inference profiles, metric and drift tables, slicing, custom metrics."
sources:
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling
  - https://docs.databricks.com/aws/en/lakehouse-monitoring/create-monitor-api
  - https://docs.databricks.com/aws/en/lakehouse-monitoring/monitor-output
  - https://docs.databricks.com/aws/en/lakehouse-monitoring/custom-metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lakehouse Monitoring: profiles and drift

**Goal:** automatic statistical profiles and drift metrics for important tables and model inference logs, with alerts when distributions shift. Current docs call the feature data profiling and each monitor a profile.

## 1. Pick a profile type
| Profile | Table shape | Compares |
|---|---|---|
| Snapshot | whole table each refresh | table state at each refresh |
| TimeSeries | has an event timestamp | metrics per time window vs previous window or baseline |
| InferenceLog | model requests: inputs, prediction, (label), model id, timestamp | data drift + model quality per model id |
- A snapshot profile has a maximum table size of 4 TB; use TimeSeries for larger tables.
- Only one profile per table in a Unity Catalog metastore; the table can be a managed or external Delta table registered in Unity Catalog.
- A first TimeSeries or InferenceLog profile analyses only the 30 days before its creation; new data is processed afterwards.
- Enable change data feed on TimeSeries and InferenceLog tables so only newly appended data is processed. Profiles on materialized views do not support incremental processing.

## 2. Create a profile (Python SDK)
Use `databricks-sdk>=0.68.0` and the `w.data_quality` API; the older `quality_monitors` API is deprecated.
```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dataquality import (
    Monitor, DataProfilingConfig, TimeSeriesConfig, AggregationGranularity, Refresh)
w = WorkspaceClient()
schema = w.schemas.get(full_name="prod.monitoring")
table = w.tables.get(full_name="prod.silver.orders")
config = DataProfilingConfig(
    output_schema_id=schema.schema_id,
    assets_dir="/Workspace/Shared/monitors/orders",
    time_series=TimeSeriesConfig(
        timestamp_column="order_ts",
        granularities=[AggregationGranularity.AGGREGATION_GRANULARITY_1_DAY]),
    slicing_exprs=["region", "channel"],
)
w.data_quality.create_monitor(monitor=Monitor(
    object_type="table", object_id=table.table_id, data_profiling_config=config))
w.data_quality.create_refresh(object_type="table", object_id=table.table_id,
    refresh=Refresh(object_type="table", object_id=table.table_id))   # on demand
```
- Granularities run from `AGGREGATION_GRANULARITY_5_MINUTES` through hours, days, weeks, `..._1_MONTH` and `..._1_YEAR`.
- Add a `schedule` (a cron schedule with `quartz_cron_expression` and `timezone_id`) to `DataProfilingConfig` for recurring refreshes, and `notification_settings` for failure emails (maximum 5 addresses per event type).
- `list_refresh` and `get_refresh` show refresh history; `delete_monitor` removes the profile but not the metric tables or dashboard.
- Refreshes run on serverless compute.

## 3. Outputs
- `{output_schema}.{table}_profile_metrics` — per column, per window, per slice: counts, null counts, distinct count, average, 1000 quantiles, top 100 frequent items.
- `{output_schema}.{table}_drift_metrics` — per column: `drift_type` is `CONSECUTIVE` (previous window) or `BASELINE`; includes `chi_squared_test` and `js_distance` for categorical columns, `ks_test` and `wasserstein_distance` for numeric columns, and `population_stability_index`.
- An auto-generated, customisable dashboard in `assets_dir`.
- Metrics are always computed for the whole table; slicing expressions add per-slice rows.
A **baseline table** compares against a known-good dataset (for example training data) instead of the previous window.

## 4. Custom metrics
```python
from databricks.sdk.service.catalog import MonitorMetric, MonitorMetricType
import pyspark.sql.types as T
MonitorMetric(type=MonitorMetricType.CUSTOM_METRIC_TYPE_AGGREGATE, name="refund_rate",
              input_columns=[":table"], definition="avg(CASE WHEN status='REFUNDED' THEN 1 ELSE 0 END)",
              output_data_type=T.StructField("output", T.DoubleType()).json())
```
Types: `CUSTOM_METRIC_TYPE_AGGREGATE` (from table columns), `CUSTOM_METRIC_TYPE_DERIVED` (from other metrics), `CUSTOM_METRIC_TYPE_DRIFT` (comparing windows). Use `:table` in `input_columns` when more than one column is involved. See the custom metrics page for how to attach them to a profile.

## 5. Alerts
Write a SQL alert over the metric tables, for example a Jensen-Shannon distance threshold on a categorical key column (numeric columns carry `ks_test` and `wasserstein_distance` instead):
```sql
SELECT max(js_distance) FROM prod.monitoring.orders_drift_metrics
WHERE column_name = 'channel' AND drift_type = 'CONSECUTIVE' AND window.start >= current_date() - 1;
```

## Verify
- [ ] Profile refresh succeeds on schedule (check refresh history).
- [ ] Profile metrics show expected row counts per window.
- [ ] A drift alert fires when you test with a shifted sample.

## Checked

2026-11-09. Confirmed on the Databricks data profiling overview, create-profile API, metric tables and custom metrics pages: profile types, 4 TB snapshot limit, 30-day initial window, CDF recommendation, w.data_quality create_monitor/create_refresh/list_refresh/delete_monitor, quality_monitors deprecated, granularity names, notification limit of 5 emails, metric table names, drift_type values, drift statistic columns and which apply to categorical vs numeric columns, custom metric types and the :table input. Removed or corrected: the deprecated quality_monitors calls, the Quality-tab UI path, a js_distance example on a numeric column, schema-level anomaly detection claim and the "up to 0.2" threshold (none confirmed). The custom metric snippet is as on the custom metrics page; its attachment parameter was not checked.

Method: documentation only; no commands were run.
