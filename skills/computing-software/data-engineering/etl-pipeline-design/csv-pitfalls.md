---
id: computing-software.data-engineering.etl-pipeline-design.csv-pitfalls
name: csv-pitfalls
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, file-formats, csv-pitfalls, rfc-4180, quoting, embedded-newlines, bom, delimiters, encoding]
level: practitioner
status: gated
description: "Parse and produce CSV files that survive real data: RFC 4180 quoting, embedded newlines, BOMs, delimiters, encodings, nulls vs empty strings, leading zeros and Excel damage."
sources:
  - https://www.rfc-editor.org/rfc/rfc4180
  - https://docs.python.org/3/library/csv.html
  - https://docs.snowflake.com/en/sql-reference/sql/create-file-format
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSV pitfalls

**Goal:** CSV ingestion that does not silently shift columns, lose rows, or corrupt values.

## The usual failures
| Problem | Symptom | Handling |
|---|---|---|
| Embedded delimiter/newline in a field | column count varies per line; rows split | require RFC 4180 quoting (`"a,b"`), parse with a real CSV parser, enable multiline (`multiLine=true` in Spark) |
| Quotes inside quoted fields | `"He said ""hi"""` vs backslash escapes | set escape char correctly: RFC uses doubled quotes; many exports use `\"` (Spark's CSV `escape` option defaults to `\`, Python's csv module defaults to doubled quotes; both checked in the docs/run) |
| UTF-8 BOM at file start | first column name `﻿id` | strip BOM (`encoding='utf-8-sig'` in Python; most loaders have an option) |
| Wrong encoding | mojibake (`Ã©`) or load errors | ask for UTF-8; detect (`chardet`), convert with `iconv -f WINDOWS-1252 -t UTF-8` |
| Delimiter ambiguity | `;` in European Excel exports | configure per source; validate header column count |
| Null vs empty string | `,,` vs `,"",` | define: empty unquoted = NULL, `""` = empty string (Snowflake `EMPTY_FIELD_AS_NULL`, Spark `nullValue`/`emptyValue`) |
| Leading zeros / IDs | `00123` becomes `123`; long IDs become `1.23E+15` | read everything as string at landing; cast deliberately |
| Excel round-trips | dates reformatted, trailing zeros lost | never accept Excel-edited CSV for machine pipelines; use XLSX or a proper export |
| Trailing delimiter / ragged rows | extra empty column | `skip_header`, `ERROR_ON_COLUMN_COUNT_MISMATCH` decisions (Snowflake default `TRUE`, which errors; Spark PERMISSIVE does not treat short or long rows as corrupt: it pads with null or drops extra tokens, so check column counts yourself) |
| Line endings | `\r\n` vs `\n`, stray `\r` in values | normalise or configure record delimiter |

## Ingest defensively
1. Land the file untouched; record checksum and byte size.
2. Validate header (names and order) against the expected contract; fail on mismatch.
3. Parse all columns as strings into a raw table, with file name and line number.
4. Cast in staging with explicit formats; route rows failing casts to a quarantine table.
5. Reconcile row count with trailer record or provider manifest.

Spark (options `multiLine`, `escape`, `mode`, `columnNameOfCorruptRecord` checked in the Spark CSV docs; the corrupt-record column must be a string field in the schema; the snippet itself was not run, no Spark here):
```python
spark.read.option("header", True).option("multiLine", True).option("escape", '"') \
  .option("mode", "PERMISSIVE").option("columnNameOfCorruptRecord", "_corrupt") \
  .schema(all_string_schema_with_corrupt).csv(path)
```
Snowflake file format (option names and defaults checked in the CREATE FILE FORMAT docs; `EMPTY_FIELD_AS_NULL` already defaults to TRUE): `type=csv field_optionally_enclosed_by='"' skip_header=1 encoding='UTF8' empty_field_as_null=true error_on_column_count_mismatch=true`.

## Producing CSV for others
Quote all text fields (`csv.QUOTE_NONNUMERIC` or `QUOTE_ALL`), UTF-8 without BOM unless the consumer is Excel (then a BOM often helps (gated: unconfirmed, source is paywalled or blocked)), ISO-8601 dates, `.` decimal separator, header row, consistent `\n`. Document the dialect. Better: offer Parquet.

## Verify
- [ ] Test fixture with commas, quotes, newlines, unicode and empty vs null loads correctly.
- [ ] Column count and header checks fail loudly on a malformed file.
