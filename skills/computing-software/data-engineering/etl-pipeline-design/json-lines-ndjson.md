---
id: computing-software.data-engineering.etl-pipeline-design.json-lines-ndjson
name: json-lines-ndjson
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, ndjson, json-lines, semi-structured-data, streaming-files]
level: practitioner
status: gated
description: "Produce and load JSON Lines (NDJSON) files correctly: one object per line, compression and splitting, schema drift, large numbers and timestamps, and warehouse loading."
sources:
  - https://jsonlines.org/
  - https://docs.snowflake.com/en/user-guide/data-load-considerations-prepare#semi-structured-data-files-and-subcolumnarization
  - https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JSON Lines / NDJSON

**Goal:** semi-structured exports and logs that load in parallel, append cheaply and survive partial failures.

## Format rules
- One complete JSON value (usually an object) per line, UTF-8 with no byte-order mark, `\n` separated (jsonlines.org: `\r\n` also works, a final newline is strongly recommended, blank lines are not valid); no outer array, no trailing commas.
- Newlines inside strings must be escaped (`\n`) by the serializer; never pretty-print.
- File extension `.jsonl` / `.ndjson`; jsonlines.org says the media type "may be `application/jsonl`, but this is not yet standardized" (`application/x-ndjson` is the other common label (gated: unconfirmed, source is paywalled or blocked)).

## Why over a JSON array
- Streamable: write and read line by line in constant memory.
- Splittable: engines parallelise by line ranges (when uncompressed or with splittable compression).
- A corrupt line affects one record, not the file.

## Write
```python
import json, gzip
with gzip.open("events-0001.jsonl.gz", "wt", encoding="utf-8") as f:
    for e in events:
        f.write(json.dumps(e, separators=(",", ":"), ensure_ascii=False, default=str) + "\n")
```
Gzip is not splittable (BigQuery docs: gzip JSON cannot be read in parallel and loads slower than uncompressed): write many moderately sized files instead of one huge one (the 100-250 MB figure is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)). The snippet was run and round-trips.

## Load
- Snowflake: `FILE_FORMAT = (TYPE = JSON STRIP_OUTER_ARRAY = FALSE)`; land into a VARIANT column, then flatten; `MATCH_BY_COLUMN_NAME` for typed tables (gated: unconfirmed, source is paywalled or blocked).
- BigQuery: `--source_format=NEWLINE_DELIMITED_JSON` (each object on its own line), explicit schema for production; `--ignore_unknown_values` skips fields not in the schema, so use it cautiously.
- Spark/Databricks: `spark.read.json(path)` reading JSON Lines, or Auto Loader with schema hints and `_rescued_data` (gated: unconfirmed, source is paywalled or blocked).
- DuckDB: `read_json('*.jsonl', format='newline_delimited')` (run on DuckDB 1.5.6; also reads `.jsonl.gz`; a key with mixed string/number values came back as a JSON-typed column, matching the mixed-types trap).

## Traps
- Big integers (> 2^53) lose precision in JavaScript-based producers and some parsers (Python and DuckDB kept 2^60 exactly in a test): send IDs as strings.
- Timestamps: ISO 8601 with offset (`2026-10-18T09:00:00Z`); epoch numbers need documented units.
- Schema drift: new keys appear silently; inference on the first N lines misses rare fields. Prefer explicit schemas or variant landing + contract checks.
- Mixed types for the same key across lines (`"price": "9.99"` vs `9.99`) break typed loads.

## Verify
`jq -c . file.jsonl > /dev/null` (jq not run here; any line-by-line parser works, e.g. `json.loads` per line as re-run this session) validates every line; loaded row count equals line count.
