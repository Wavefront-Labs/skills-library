---
id: computing-software.data-engineering.apache-spark.csv-json-readers-and-corrupt-records
name: csv-json-readers-and-corrupt-records
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-data-sources, csv-json-reader, corrupt-record, permissive-mode, dropmalformed, failfast, badrecordspath, multiline-json, csv-options, schema-inference]
level: practitioner
status: docs-checked
description: "Ingest CSV and JSON with Spark safely: explicit schemas, PERMISSIVE/DROPMALFORMED/FAILFAST, _corrupt_record capture, multiLine, quoting/escape options and encoding."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-csv.html
  - https://spark.apache.org/docs/latest/sql-data-sources-json.html
  - https://spark.apache.org/docs/latest/sql-migration-guide.html#upgrading-from-spark-sql-22-to-23
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSV and JSON readers: schemas and corrupt records

**Goal:** load text files without silently dropping or mangling bad rows, and keep the bad rows for inspection.

## Always supply a schema
`inferSchema=true` (CSV, default false) needs one extra pass over the data, and inferred types follow whatever the data contains, so they can change between runs. Pin a DDL schema:
```python
schema = "order_id STRING, amount DECIMAL(12,2), order_ts TIMESTAMP, _corrupt_record STRING"
df = (spark.read.format("csv")
      .schema(schema)
      .option("header", True)
      .option("mode", "PERMISSIVE")
      .option("columnNameOfCorruptRecord", "_corrupt_record")
      .load("s3://landing/orders/2026-10-15/"))
df.cache()   # since Spark 2.3, queries on raw JSON/CSV files that reference only the corrupt-record column are disallowed; cache or save the parsed result first
bad = df.filter("_corrupt_record IS NOT NULL")
good = df.filter("_corrupt_record IS NULL").drop("_corrupt_record")
```

## Modes
| mode | Behaviour |
|---|---|
| `PERMISSIVE` (default) | Sets malformed fields to null and puts the malformed string in the field named by `columnNameOfCorruptRecord` if the schema declares it (otherwise the record is still retained with null fields) |
| `DROPMALFORMED` | Ignores the whole corrupted record |
| `FAILFAST` | Throws an exception on a corrupted record |
CSV parses only the required columns under column pruning (`spark.sql.csv.parser.columnPruning.enabled`, default true), so which records count as corrupt can depend on the columns selected.

## CSV options that matter
- `sep`, `quote`, `escape` (default backslash; sets the character escaping quotes inside an already quoted value), `multiLine=true` for quoted values containing line separators (when it is disabled, a quoted value containing a line separator splits one source record into two before `mode` is applied).
- `nullValue`, `emptyValue`, `nanValue`; `ignoreLeadingWhiteSpace`; `encoding`.
- `enforceSchema=true` (default) forcibly applies the specified or inferred schema and ignores CSV headers. Set `enforceSchema=false` to validate the schema against the headers when `header` is true.

## JSON options
- The default expects one JSON object per line; a pretty-printed or array file needs `multiLine=true`.
- `primitivesAsString`, `allowComments`, `dropFieldIfAllNull` (all default false).
- Fields absent from your pinned schema are not read: compare a sample's inferred schema to the pinned one to spot drift.

## Gotchas
- In PERMISSIVE mode malformed fields become null, so also check null rates on required columns.

## Verify
- [ ] Row counts: good plus bad rows match the source record count (excluding headers).
- [ ] Bad rows are persisted for inspection.
- [ ] Ingest fails or alerts when bad-row ratio exceeds a threshold.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/, SQLConf.scala and python/pyspark/sql/readwriter.py on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in sql-data-sources-csv.md and sql-data-sources-json.md: mode values and semantics, columnNameOfCorruptRecord behaviour, inferSchema default false with an extra pass, enforceSchema semantics, escape meaning, multiLine behaviour for quoted line separators, column pruning, primitivesAsString / allowComments / dropFieldIfAllNull defaults; migration guide 2.2 to 2.3 for the corrupt-record-only query restriction and the cache workaround. Removed the Databricks badRecordsPath note, gzip splittability, version-dependent null claims and the file-name helper.

Method: documentation only; no commands were run.
