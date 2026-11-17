---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-vparquet-block-format
name: tempo-vparquet-block-format
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [vparquet, tempo, parquet, block-version, vparquet5, dedicated-columns, storage-format]
level: practitioner
status: docs-checked
description: "Choose Tempo's Parquet block version (vParquet5 default, vParquet4) and configure dedicated attribute columns, arrays and blobs to speed up queries."
sources: ["https://grafana.com/docs/tempo/latest/configuration/parquet/", "https://grafana.com/docs/tempo/latest/operations/dedicated_columns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the block version and move heavy attributes into dedicated columns.

Parquet is the only supported block format in Tempo 3.x (`v2` removed in 3.0). From Tempo 3.1 new blocks are `vParquet5` by default; existing `vParquet4` blocks stay readable with no migration. `vParquet3` was removed in Tempo 3.2: Tempo cannot read those blocks and refuses to start configured to write them, so convert any left with `tempo-cli` from Tempo 3.1 or let them expire.

Set the version (omit it for `vParquet5`; `vParquet4` is the opt-in alternative):
```yaml
storage:
  trace:
    block:
      version: vParquet5
```
Changing the version applies to blocks written afterwards; existing data is left as is.

Dedicated attribute columns need `vParquet4` or later. Limits: vParquet4 allows up to 10 string columns per scope (span, resource); vParquet5 allows up to 20 string and 5 integer columns per scope (span, resource, event).
```yaml
storage:
  trace:
    block:
      parquet_dedicated_columns:
        - {name: http.method, type: string, scope: span}
        - {name: custom.retry.counts, type: int, scope: span, options: ["array"]}
        - {name: db.statement, type: string, scope: span, options: ["blob"]}
        - {name: exception.message, type: string, scope: event}
```
`options` (`array`, `blob`), `int` and `event` scope are vParquet5 only. Blob columns use zstd compression instead of dictionary encoding for high-cardinality or long values (UUIDs, stack traces); mark a column blob when its dictionary size per row group exceeds the threshold (default 4 MiB). Integer columns work best when the attribute is on at least 5% of rows in the scope.

The same list can be set under `overrides.parquet_dedicated_columns` or per tenant in the overrides file (`"*"` wildcard supported). The most specific configuration wins: tenant over global overrides over storage block config.

Pick candidates with `tempo-cli analyse blocks <tenant-id>` (or `analyse block <tenant-id> <block-id>`); it lists top attributes by size, flags integer candidates and takes `--blob-threshold`. The docs say the best candidates are attributes contributing most to block size, even if rarely queried.

Search read tuning (storage block): `read_buffer_size_bytes` (default 10485676) times `read_buffer_count` (default 32) is the total buffering per Parquet block search. `cache_control` booleans `footer`, `column_index`, `offset_index` default to false.

Gotchas
- Lower-version Tempo may not read newer block versions; upgrade all components before switching writers.
- Early-3.x docs vs current docs differ on the default version; check your release.

## Verify
After switching, new blocks report the new version in `tempo-cli` block listings; verify against your release's command help.

## Checked
2026-11-03. Confirmed against the Tempo Parquet block format and Dedicated attribute columns pages. Removed: `vParquet4` default, `{scope,name,type}` flow example with invented attributes, the `storage.parquet_dedicated_columns` override path, the `list block --version` verification output claim, "compaction rewrites to the configured version" and the high-cardinality candidate advice.
Method: documentation only; no commands were run.
