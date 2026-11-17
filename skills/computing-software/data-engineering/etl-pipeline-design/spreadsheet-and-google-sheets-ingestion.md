---
id: computing-software.data-engineering.etl-pipeline-design.spreadsheet-and-google-sheets-ingestion
name: spreadsheet-and-google-sheets-ingestion
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, spreadsheet-ingestion, google-sheets, excel, manual-data]
level: practitioner
status: gated
description: "Ingest spreadsheets and Google Sheets reliably: service account access, typed reads, header and type drift checks, locking down the source, and when to replace it."
sources:
  - https://developers.google.com/sheets/api/guides/values
  - https://docs.gspread.org/en/latest/
  - https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spreadsheet and Google Sheets sources

**Goal:** business-maintained mapping tables, targets and manual adjustments flow into the warehouse without breaking every time someone edits the sheet.

Checked here: gspread 6.2.1 has `service_account(filename=...)`, `open_by_key`, `worksheet`, and `Worksheet.get_all_records(head, expected_headers, value_render_option, ...)`; `pd.to_datetime(serial, unit="D", origin="1899-12-30")` turned 45000 into 2023-03-15; with openpyxl, `pd.read_excel(..., dtype={"region": "string"}, skiprows=2)` kept `"007"` while the same read without `dtype` returned integer 7 (so leading zeros are lost without dtype); a merged cell raised no error and simply read as NaN, so merged-cell checks must be written explicitly. Calls to the live Google Sheets API, `UNFORMATTED_VALUE` rendering and the native warehouse connectors were not run (no account) (gated: unconfirmed, source is paywalled or blocked).

## Google Sheets via API
```python
import gspread, pandas as pd
gc = gspread.service_account(filename="sa.json")          # share the sheet with the service account email
ws = gc.open_by_key("1AbC...").worksheet("targets")
rows = ws.get_all_records(expected_headers=["region", "month", "target_eur"], value_render_option="UNFORMATTED_VALUE")
df = pd.DataFrame(rows)
```
- `UNFORMATTED_VALUE` returns numbers as numbers (not "1,234.00"); dates come as serial numbers: convert with `pd.to_datetime(df.month, unit="D", origin="1899-12-30")`.
- Alternatives: Snowflake/BigQuery native connectors (BigQuery external tables over Sheets), Fivetran/Airbyte Sheets connectors.

## Excel files
```python
df = pd.read_excel(path, sheet_name="targets", dtype={"region": "string"}, engine="openpyxl", skiprows=2)
```
Read with explicit dtypes; leading zeros and IDs as strings.

## Validate before loading
- Exact header set (fail if a column is renamed/added) and row count bounds.
- Types per column, allowed values (regions in a reference list), uniqueness of keys.
- Reject merged cells/blank header rows with a clear message to the sheet owner.
Load into staging only after validation; keep the last good version if validation fails.

## Protect the source
- Protected ranges for headers and formula columns; data validation dropdowns for categorical columns.
- One tab per dataset; no free-form notes in the data range.
- Named owner; changes notified via a pipeline alert to them, not to data engineers.

## When to replace it
If the sheet has more than a few editors, needs history/audit, or drives money decisions, move it to a small app, a dbt seed under review, or a governed input table with a form.

## Verify
Rename a header in a copy of the sheet: the pipeline fails validation with an actionable message and the warehouse keeps the previous load.
