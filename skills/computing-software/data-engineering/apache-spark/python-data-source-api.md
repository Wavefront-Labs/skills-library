---
id: computing-software.data-engineering.apache-spark.python-data-source-api
name: python-data-source-api
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, python-data-source-api, custom-data-source, datasourcereader, datasourcewriter, spark-4]
level: advanced
status: docs-checked
description: "Build custom Spark readers and writers in pure Python with the Python Data Source API (Spark 4.0): DataSource, partitions, batch and streaming readers, and commit hooks."
sources:
  - https://spark.apache.org/docs/latest/api/python/tutorial/sql/python_data_source.html
  - https://issues.apache.org/jira/browse/SPARK-44076
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python Data Source API (custom readers and writers)

**Use when:** you need `spark.read.format("myapi")` for a REST API, a proprietary file format, or a system with no JVM connector, and want to stay in Python. Available in Spark 4.0.

```python
from pyspark.sql.datasource import DataSource, DataSourceReader, InputPartition

class TicketsSource(DataSource):
    @classmethod
    def name(cls): return "tickets"
    def schema(self): return "id long, status string, updated timestamp"
    def reader(self, schema): return TicketsReader(self.options)

class TicketsReader(DataSourceReader):
    def __init__(self, options): self.base = options["url"]; self.pages = int(options.get("pages", 10))
    def partitions(self):                      # runs on the driver; one task per partition
        return [InputPartition(p) for p in range(self.pages)]
    def read(self, partition):                 # runs on executors; yield tuples matching schema
        import requests
        for r in requests.get(f"{self.base}?page={partition.value}", timeout=30).json():
            yield (r["id"], r["status"], r["updated"])

spark.dataSource.register(TicketsSource)
df = spark.read.format("tickets").option("url", "https://api.example.com/tickets").load()
```

## Writers
Implement `DataSource.writer` returning a `DataSourceWriter` with `write(iterator) -> WriterCommitMessage` (per task) and `commit(messages)` / `abort(messages)` on the driver. Make `write` stage data and `commit` publish it, so a failed job leaves nothing half-written.

## Streaming
`streamReader` (or the simpler `simpleStreamReader`) returns a `DataSourceStreamReader` with `initialOffset()` and `latestOffset()` returning dicts, plus the partition, read and commit methods shown in the tutorial.

## Gotchas
- `read` runs on executors, so create clients (sessions, connections) there rather than at module level.
- Each partition is one Python task; size partitions so tasks take seconds to minutes, and respect API rate limits (fewer partitions).

## Verify
- [ ] `spark.read.format("tickets")...count()` equals the API's total.
- [ ] Kill a write mid-job: `abort` leaves the target clean.

## Checked

2026-10-28. Confirmed against: PySpark Python data source tutorial (DataSource, DataSourceReader, InputPartition, registration with spark.dataSource.register, writer commit/abort and WriterCommitMessage, streamReader/simpleStreamReader, initialOffset/latestOffset). Removed (not confirmable in the fetched pages): Databricks Runtime preview note, writer and stream-reader exact signatures, pickling and options-as-strings gotchas, no-pushdown claim.

Method: documentation only; no commands were run.
