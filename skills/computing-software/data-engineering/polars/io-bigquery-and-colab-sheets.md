---
id: computing-software.data-engineering.polars.io-bigquery-and-colab-sheets
name: io-bigquery-and-colab-sheets
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, bigquery, google-sheets, colab, interactive-sheet, from-arrow, polars-io-bigquery, write-parquet]
level: practitioner
status: docs-checked
description: "Move Polars data to and from Google BigQuery (from_arrow, parquet load job) and Google Sheets in Colab via sheets.InteractiveSheet."
sources:
  - https://docs.pola.rs/user-guide/io/bigquery/
  - https://docs.pola.rs/user-guide/io/sheets_colab/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: exchange Polars data with BigQuery and, in Colab, Google Sheets.

BigQuery (needs `pip install google-cloud-bigquery`)
Read: run the query, convert the result to Arrow, then `pl.from_arrow`.
```python
from google.cloud import bigquery
client = bigquery.Client()
query_job = client.query(QUERY)       # API request
rows = query_job.result()             # waits for query to finish
df = pl.from_arrow(rows.to_arrow())
```
Write: stream the frame as Parquet into a load job; it does not hit disk.
```python
with io.BytesIO() as stream:
    df.write_parquet(stream)
    stream.seek(0)
    parquet_options = bigquery.ParquetOptions()
    parquet_options.enable_list_inference = True
    job = client.load_table_from_file(
        stream, destination='tablename', project='projectname',
        job_config=bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            parquet_options=parquet_options,
        ),
    )
job.result()  # waits for the job to complete
```

Google Sheets in Colab (`from google.colab import sheets`)
- Open: `sheets.InteractiveSheet(url=url, backend="polars", display=False)` or `sheet_id=...`; `sheet.as_df()` returns the data. The left-most worksheet is used unless you pass `worksheet_id` or `worksheet_name`. Each session, Colab asks permission to edit your Drive assets on first use.
- Create: omit the source, e.g. `InteractiveSheet(title="Colab <3 Polars", backend="polars")`; pass `df=df` to write data immediately.
- Write: `sheet.update(df)` clears the worksheet and writes at the top left. `sheet.update(df, clear=False)` keeps contents; `sheet.update(df, location="D3")` or `location=(3, 4)` moves the target.
- Loop pattern: clear on the first iteration only (`clear=i == 0`); the page says dataframes land next to each other, one every five columns. Its snippet passes `loc=(1, i * 3)` while the text names `location`, so prefer the documented `location` parameter.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
