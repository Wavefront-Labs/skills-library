---
id: computing-software.data-engineering.data-quality.snowflake-data-metric-functions
name: snowflake-data-metric-functions
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-metric-functions, snowflake-dmf, data-quality-monitoring, null-count, freshness, custom-dmf, expectations]
level: practitioner
status: docs-checked
description: "Monitor data quality inside Snowflake with data metric functions: system DMFs (NULL_COUNT, DUPLICATE_COUNT, FRESHNESS), custom DMFs, schedules, expectations and result queries."
sources:
  - https://docs.snowflake.com/en/user-guide/data-quality-intro
  - https://docs.snowflake.com/en/user-guide/data-quality-system-dmfs
  - https://docs.snowflake.com/en/user-guide/data-quality-custom-dmfs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake data metric functions (DMFs)

**Goal:** quality metrics computed by Snowflake on a schedule, attached to tables or views, without an external DQ tool. Requires Enterprise Edition.

## Concepts
- **DMF**: measures an attribute (NULL count, update frequency). It returns a value but does not say whether that value is a problem.
- **Expectation**: combined with a DMF it forms a data quality check; the returned value is compared to the expectation to pass or fail, and failures are reported as expectation violations. Snowsight lets you pick the DMF and set the expectation together; SQL can also manage expectations.
- **DMF schedule**: set per table or view; default runs the DMF once every hour.
- **Anomaly detection**: uses history to flag values outside a predicted range; currently for data volume and freshness only. The DMF schedule does not affect how often anomalies are checked.

## System DMFs
More than 185 system DMFs live in the CORE schema of the shared SNOWFLAKE database (so `snowflake.core.<name>`); they cannot be altered. Categories and examples:
- Completeness: NULL_COUNT, NULL_PERCENT, BLANK_COUNT, EMPTY_STRING_COUNT, NOT_NULL_COUNT.
- Uniqueness: DUPLICATE_COUNT (includes NULLs), DUPLICATE_PERCENT, UNIQUE_COUNT, UNIQUE_PERCENT.
- Freshness: FRESHNESS (timestamp column or latest DML), SECONDS_SINCE_ROW_COUNT_CHANGE, SOURCE_TARGET_LAG.
- Volume: ROW_COUNT, ROW_COUNT_DIFFERENCE (vs a reference table), ROWS_IN_PAST_* (0 means no data arrived).
- Validity: ACCEPTED_VALUES (Boolean expression), FUTURE_TIMESTAMP_COUNT, INVALID_EMAIL_COUNT and other format checks.
- Statistics (AVG, MIN, MAX, STDDEV, SUM...) return a measurement only; you define the expectation. Outlier DMFs use built-in thresholds (Tukey fences 1.5x IQR, extreme 3x IQR; Z-score above 3, extreme above 4.5). Schema DMFs count column adds, drops and type changes between evaluations. Machine learning DMFs compare predicted with actual columns (predicted column first).
- Many count and percent DMFs measure undesirable values, so lower is better; NOT_NULL_COUNT measures values that meet an expectation.

## Custom DMF
Use when no system DMF fits. `DATA_METRIC_SCHEDULED_TIME` can be called in the body (for example a custom freshness metric).
```sql
CREATE OR REPLACE DATA METRIC FUNCTION governance.dmfs.count_positive_numbers(
  arg_t TABLE(arg_c1 NUMBER, arg_c2 NUMBER, arg_c3 NUMBER))
RETURNS NUMBER
AS
$$ SELECT COUNT(*) FROM arg_t WHERE arg_c1>0 AND arg_c2>0 AND arg_c3>0 $$;
```
A DMF can take several table arguments, e.g. referential checks. The table you attach it to is the first argument; the second table is given by fully qualified name:
```sql
CREATE OR REPLACE DATA METRIC FUNCTION governance.dmfs.referential_check(
  arg_t1 TABLE (arg_c1 INT), arg_t2 TABLE (arg_c2 INT))
RETURNS NUMBER AS
  'SELECT COUNT(*) FROM arg_t1 WHERE arg_c1 NOT IN (SELECT arg_c2 FROM arg_t2)';

ALTER TABLE salesorders ADD DATA METRIC FUNCTION governance.dmfs.referential_check
  ON (sp_id, TABLE (my_db.sch1.salespeople(sp_id)));
```
A result above 0 means orphaned values. Test a DMF by calling it manually before attaching it. `ALTER FUNCTION ... SET SECURE` makes it secure; a DMF still attached to a table or view cannot be dropped (find attachments with the DATA_METRIC_FUNCTION_REFERENCES function).

## Supported objects
Dynamic, event, external and Iceberg tables, materialized views, regular (incl. temporary and transient) tables, and views. Not hybrid tables or streams.

## Cost and limits
- DMFs run on serverless compute billed under "Data Quality Monitoring"; logging shows as "Logging". You are billed only when a scheduled DMF runs, not for creating one or calling it with SELECT.
- Track with the DATA_QUALITY_MONITORING_USAGE_HISTORY view, or METERING_DAILY_HISTORY (service_type DATA_QUALITY_MONITORING).
- 50,000 DMF associations per account; no DMFs on shared tables or views, on object tags, in reader accounts; not on trial accounts.

## Verify
- [ ] The DMF is attached to the table, with the schedule you intend.
- [ ] A test row that violates the rule produces a changed value (or an expectation violation) after the next scheduled run.

## Checked
Method: docs-only read on 2026-11-09 of data-quality-intro and data-quality-custom-dmfs in full, and the first 120 lines plus a ROW_COUNT search of data-quality-system-dmfs (partial read: category tables). Removed unstated details: exact ALTER TABLE schedule and expectation syntax, TRIGGER_ON_CHANGES, the results view and alert/email example, privilege names and the information_schema verification query, and the claim that custom DMFs referencing other tables arrived only in newer releases.
