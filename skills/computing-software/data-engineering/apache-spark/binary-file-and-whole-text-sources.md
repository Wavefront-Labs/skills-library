---
id: computing-software.data-engineering.apache-spark.binary-file-and-whole-text-sources
name: binary-file-and-whole-text-sources
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, binaryfile-source, wholetext, binary-files, image-ingestion, pdf-ingestion, data-sources]
level: practitioner
status: docs-checked
description: "Load whole files into Spark with the binaryFile source and wholetext text reader: path filters, recursive lookup, size limits, and processing images or PDFs per row."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-binaryFile.html
  - https://spark.apache.org/docs/latest/sql-data-sources-text.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary file and whole-text sources

## binaryFile: one row per file
```python
df = (spark.read.format("binaryFile")
      .option("pathGlobFilter", "*.png")
      .option("recursiveFileLookup", "true")
      .load("s3a://raw/images/"))
# schema: path string, modificationTime timestamp, length long, content binary
```
- `content` is one binary value per file, so filter on `length` before selecting it for large files.
- `recursiveFileLookup` disables partition inference; `modifiedAfter`/`modifiedBefore` filter by modification time (format `YYYY-MM-DDTHH:mm:ss`).

Process per file with a pandas UDF (Arrow batches keep it fast):
```python
import pandas as pd
from pyspark.sql.functions import pandas_udf
@pandas_udf("int")
def width(content: pd.Series) -> pd.Series:
    from PIL import Image; import io
    return content.map(lambda b: Image.open(io.BytesIO(b)).width)
df.select("path", width("content").alias("w"))
```
Lower `spark.sql.execution.arrow.maxRecordsPerBatch` (default 10000) for large files, or the Python worker runs out of memory.

## Text with wholetext
```python
docs = spark.read.option("wholetext", True).text("s3a://raw/contracts/*.txt")   # one row per file, column "value"
```
Without `wholetext`, `text` gives one row per line. `lineSep` sets a custom delimiter.

## Many small files
Listing millions of objects is slow: on cloud storage, keep a manifest table. `spark.sql.sources.parallelPartitionDiscovery.threshold` is the related listing setting (see its description in the configuration page).

## Verify
- [ ] Row count equals object count for the prefix.
- [ ] No task failures from oversized files; executor memory steady.

## Checked

2026-10-28. Confirmed against: Spark binaryFile and text data source pages (schema columns, pathGlobFilter, recursiveFileLookup disables partition inference, modifiedBefore/modifiedAfter format, wholetext, lineSep), configuration page (spark.sql.execution.arrow.maxRecordsPerBatch default 10000, parallelPartitionDiscovery.threshold). Removed (not confirmable in the fetched pages): 2 GB limit, cheap-inventory claim, write-support claim, 3.1+ and 3.3+ gates, _metadata/input_file_name, Auto Loader, parallelism setting name (does not exist; threshold does).

Method: documentation only; no commands were run.
