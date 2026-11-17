---
id: computing-software.data-engineering.polars.lazy-sinks-partitioned-output
name: lazy-sinks-partitioned-output
category: computing-software
field: data-engineering
product: polars
tags: [polars, lazy, sink-parquet, partitionby, streaming-sink, polars-lazy-sources-sinks, cloud-storage, multipart]
level: practitioner
status: docs-checked
description: "Stream a Polars query result to disk or cloud with sink_parquet and PartitionBy, and clean up correctly when a sink fails mid-query."
sources:
  - https://docs.pola.rs/user-guide/lazy/sources_sinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write query results to storage in batches without holding everything in RAM.

Sinks execute a query and stream the results to storage (disk or cloud). Example from the page, converting many CSVs to Parquet while dropping missing data, limiting rows per file:

```python
lf = pl.scan_csv("my_dataset/*.csv").filter(pl.all().is_not_null())
lf.sink_parquet(
    pl.PartitionBy(
        "output_folder/",
        max_rows_per_file=512_000,
    )
)
```
This writes numbered files: `output_folder/00000000.parquet`, `00000001.parquet`, ... `0000000f.parquet`, `00000010.parquet`.

The page's snippet omits the `pl.` prefix on `scan_csv` and a comma after the path; the version above is corrected.

Multiplexing sinks
Several sinks in one query: create each with `lazy=True` and run them together.
```python
q1 = lf.sink_parquet(.., lazy=True)
q2 = lf.sink_ipc(.., lazy=True)
pl.collect_all([q1, q2])
```

Failure behaviour (page statements)
- If the query fails before the sink received all input, the sink does not finish its output.
- With several sinks in one `collect_all`, a sink whose input was already complete does finish.
- Cloud storage: no object is created.
- A local file already opened stays unfinished; writes in progress may still reach it shortly after the error. For plain CSV and NDJSON it is a readable prefix of the output, so delete it after a failure.
- With `PartitionBy`, files closed before the failure (by `max_rows_per_file` or the open-file limit) are completed and stay.
- Parts of a multipart upload that the sink started are not aborted; add a bucket lifecycle rule that aborts incomplete multipart uploads.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
