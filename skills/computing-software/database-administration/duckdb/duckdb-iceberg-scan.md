---
id: computing-software.database-administration.duckdb.duckdb-iceberg-scan
name: duckdb-iceberg-scan
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, iceberg, iceberg-scan, snapshots, metadata, table-format, lakehouse]
level: practitioner
status: docs-checked
description: "Read Apache Iceberg tables in DuckDB without a catalog: iceberg_scan, iceberg_metadata, iceberg_snapshots, metadata version selection, moved paths, limitations."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/core_extensions/iceberg/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query an Iceberg table by path (local or object store) with the `iceberg` extension.

Setup: auto-installed and loaded on first use; manual `INSTALL iceberg; LOAD iceberg;`. It is updated between DuckDB releases, so run `UPDATE EXTENSIONS;`. For S3/Azure paths it works with `httpfs` or `azure`. For catalogs and writes see duckdb-iceberg-rest-catalogs.

```sql
SELECT count(*) FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
SELECT count(*) FROM iceberg_scan('lineitem_iceberg/metadata/v1.metadata.json');  -- explicit metadata file
SELECT count(*) FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/v1.metadata.json');
SELECT * FROM iceberg_metadata('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
SELECT * FROM iceberg_snapshots('data/iceberg/lineitem_iceberg');
```
`iceberg_metadata` returns the columns manifest_path, manifest_sequence_number, manifest_content, status, content, file_path, file_format and record_count. `iceberg_snapshots` returns sequence_number, snapshot_id, timestamp_ms, manifest_list, and does not accept `allow_moved_paths`, `snapshot_from_id` or `snapshot_from_timestamp`.

Parameters (common): `allow_moved_paths` (default false; allows scanning Iceberg tables that are moved), `metadata_compression_codec` (`'gzip'` only), `snapshot_from_id` (UBIGINT) and `snapshot_from_timestamp` (access a snapshot with a specific id or timestamp), `version`, `version_name_format`.

Choosing the metadata version:
- Default: reads `version-hint.text`. Pass `version = '1'` for an explicit number; it tries `v1.metadata.json` and `1.metadata.json` (with `.gz` variants when gzip is set).
- A text file passed as `version` is used as a hint file; its entire content is the literal version, with no encoding, escaping or trimming, so any whitespace is formatted into file names.
- Odd naming: `version_name_format = 'rev-%s.metadata.json%s'` (comma-separated list, each with two `%s`: version, then compression extension), e.g. with `version = '2'` and `metadata_compression_codec = 'gzip'` for `rev-2.metadata.json.gz`.
- No hint and no version: `version = '?'` guesses the lexicographically largest metadata file name. Off by default because it may violate ACID constraints; enable with `SET unsafe_enable_version_guessing = true;`.

Limitations: no inserts into v3 spec tables, no reads of v3 tables with v2 data types, no geometry type.

## Checked

2026-11-07. Read the Iceberg Extension overview page in full and confirmed auto install and load, UPDATE EXTENSIONS, the common parameter defaults, the iceberg_scan, iceberg_metadata and iceberg_snapshots examples, the snapshots column list and the three unsupported parameters, version-hint behaviour, hint-file content used verbatim, the version_name_format example, version guessing and `unsafe_enable_version_guessing`, and the three limitations. Corrected the iceberg_metadata column list to the page's, reworded `allow_moved_paths`, the snapshot parameters and the hint-file whitespace note to the page's wording, and removed the 'credentials via secrets' aside, the word 'globally' and the Verify step.

Method: documentation only; no commands were run.
