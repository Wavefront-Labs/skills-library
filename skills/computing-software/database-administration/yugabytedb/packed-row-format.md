---
id: computing-software.database-administration.yugabytedb.packed-row-format
name: packed-row-format
category: computing-software
field: database-administration
product: yugabytedb
tags: [packed-rows, docdb, ysql-enable-packed-row, upgrade, storage-format]
level: practitioner
status: docs-checked
description: "What packed rows change in DocDB storage, when they are enabled by default, and how updates and compactions treat packed and unpacked fragments of a row."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb/packed-rows.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Packed row format

Without packing, a row with primary key K and n non-key columns is stored as n separate key-value pairs. With packed rows it is stored as one pair, `<K, packed {C1..Cn}>`.

Benefits: lower storage footprint, cheaper INSERTs on wide tables, and faster multi-column reads because fewer pairs are fetched. Point lookups are as fast as before since they still seek one pair.

Behaviour to know:
- **Insert:** the whole row is written as one packed pair.
- **Update:** changing some columns writes each changed column as its own pair, as before. Updating all non-key columns rewrites the row in packed form.
- **Select:** scans reassemble the row from the packed insert plus any unpacked column updates.
- **Compaction:** produces a compact version, merging unpacked fragments back into the row.

Once a row is packed it cannot be unpacked; reads understand both formats and writes may still produce the non-packed format. Sequential scans and bulk ingestion of 1 million rows were about 2x faster in the page's tests. The YSQL form is GA as of v2.20.0; the YCQL form (`--ycql_enable_packed_row`) is tech preview. Related flags: `--ysql_enable_packed_row_for_colocated_table` (default true) and `--ysql_packed_row_size_limit` and `--ycql_packed_row_size_limit` (default 0, which uses the block size as the limit; larger rows pack as many columns as fit).

Enablement: YSQL packed row is on by default for new universes from v2.20.0 (`--ysql_enable_packed_row` defaults to true). The yb-tserver reference instead says the flag default became true for new clusters starting from 2.19, so the two pages disagree by one release; check the release notes for your version. A universe that did not have it and is upgraded to a release before v2025.1 does not get it automatically. Upgrading such a universe to v2025.1 or later enables it automatically, so plan for the storage-format change in that upgrade window. The pre-v2025.1 restriction exists because of a known xCluster limitation: a target universe might not be able to interpret packed rows unless it is upgraded first.

## Checked

2026-11-04. Confirmed against the Packed rows in DocDB page (one pair versus n pairs, benefits, insert/update/select/point lookup/compaction behaviour, enablement and upgrade rules, xCluster limitation) and the yb-tserver reference (packed row flags and defaults). Page conflict recorded in the skill: the architecture page says packed row is on by default for new universes from v2.20.0, the yb-tserver reference says the flag default is true for new clusters from 2.19.

Method: documentation only; no commands were run.
