---
id: computing-software.cloud-infrastructure-engineering.cortex.parquet-mode
name: parquet-mode
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [parquet, converter, queryable, experimental, store-gateway]
level: advanced
status: docs-checked
description: "Understand experimental Parquet mode: why it exists, the converter and queryable components, and how it falls back to TSDB blocks."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/parquet-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Parquet mode is experimental. It converts TSDB blocks to Apache Parquet to improve query performance and storage efficiency for older data.

Why: TSDB indexes rely on random reads, each a separate object-store request, and merging nearby reads causes overfetching; high-cardinality postings become a bottleneck. Store-gateways need local disk for index headers and lots of memory, have complex sharding with long startups, and process blocks single-threaded. Parquet is columnar (fetch only needed columns), co-locates series likely queried together, carries rich metadata so no local state is needed, compresses well, and row groups enable parallel processing.

Two components:

- Parquet Converter: runs periodically, finds TSDB blocks to convert, and writes Parquet files alongside the blocks in object storage. Conversion status is tracked with marker files to avoid duplicate work.
- Parquet Queryable: queries Parquet files first and falls back to TSDB blocks when necessary.

Enabling:

- Converter: add `parquet-converter` to the target list (`target: parquet-converter`, or `all,parquet-converter`), set the `parquet_converter` block (`data_dir`, `conversion_interval`, `max_rows_per_row_group`, a ring) and enable conversion per tenant with the limits `parquet_converter_enabled`, `parquet_converter_tenant_shard_size` and `parquet_converter_sort_columns`.
- Queryable: set `enable_parquet_queryable: true` in the `querier` block. `parquet_queryable_fallback_disabled` defaults to false; set to true only when every needed block is converted, because queries then fail with a consistency check error if a block lacks Parquet files.
- Limits `parquet_max_fetched_row_count`, `parquet_max_fetched_chunk_bytes` and `parquet_max_fetched_data_bytes` cap per-query fetching. Chunk and labels caches are configured under `blocks_storage.bucket_store` (backends: none, inmemory, memcached, redis, or a comma-separated multi-level list).

Which blocks convert: only blocks whose time range is larger than the base TSDB block duration (typically 2h), once each, and only for tenants with conversion enabled.

Limitations: experimental; Parquet files are stored in addition to TSDB blocks; there is a delay between block creation and Parquet availability; only shuffle sharding is supported as the sharding strategy; the bucket index must be enabled because it carries the Parquet metadata used for query routing. Roll out per tenant first and keep TSDB blocks as the fallback.

## Checked

Method: docs-checked 2026-11-09 against the Cortex Parquet mode guide (raw markdown, read in full).
