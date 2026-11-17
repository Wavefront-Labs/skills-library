---
id: computing-software.database-administration.sql-server.interpreting-checkdb-output
name: interpreting-checkdb-output
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, dbcc-checkdb, checkdb-errors, minimum-repair-level, corruption, nonclustered-index-corruption, incident-response]
level: advanced
status: docs-checked
description: "Read DBCC CHECKDB errors to judge scope: which object and index ids, the minimum repair level, and when rebuilding a nonclustered index beats restoring."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/errors-events/database-engine-events-and-errors
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-pages-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreting DBCC CHECKDB output

## Run for a readable result
```sql
DBCC CHECKDB (Sales) WITH NO_INFOMSGS, ALL_ERRORMSGS;
```
Without `NO_INFOMSGS` the real errors are buried in row counts.

## The summary lines matter most
```
CHECKDB found 0 allocation errors and 3 consistency errors in table 'Orders' (object ID 245575913).
CHECKDB found 0 allocation errors and 3 consistency errors in database 'Sales'.
repair_rebuild is the minimum repair level for the errors found by DBCC CHECKDB (Sales).
```
| Minimum repair level | Meaning |
|---|---|
| `repair_rebuild` | repairs with no possibility of data loss (for example missing rows in nonclustered indexes, or rebuilding an index) |
| `repair_allow_data_loss` | some errors can only be fixed by deallocating a row, page or pages; that data is lost |

The repair option to use is named at the end of the reported errors. Microsoft recommends restoring from a known good backup instead of any `REPAIR_*` option.

## Identify the damaged structure
Each error names object and index ids:
`Msg 8951 ... Table error: table 'Orders' (ID 245575913). Data row does not have a matching index row in the index 'IX_Orders_Customer' (ID 7).`
- **index_id 0** = heap, **1** = clustered index (the table data itself), **> 1** = nonclustered index.
- If every error is on index_id > 1: the base data is fine. Fix by disabling/dropping and
  recreating that nonclustered index (an `ALTER INDEX ... REBUILD` may read the bad index;
  `DROP` + `CREATE` or `REBUILD` after `DISABLE` reads the base table instead).
  ```sql
  ALTER INDEX IX_Orders_Customer ON dbo.Orders DISABLE;
  ALTER INDEX IX_Orders_Customer ON dbo.Orders REBUILD WITH (ONLINE = ON);
  ```
- Errors on index_id 0/1, or allocation errors (8905, 8906), mean the base data may be damaged: plan a restore.

## Common error numbers
| Msg | Meaning |
|---|---|
| 8928 | page could not be processed (see the other errors) |
| 8939 / 8946 | a page test failed / invalid allocation page header values |
| 8951 / 8952 / 8956 | index row and data row mismatch (often nonclustered only) |
| 8976 | page not seen in the scan although its parent and previous page refer to it |

## Decision order
1. Find root cause: storage errors (system event log, `msdb.dbo.suspect_pages`).
2. Nonclustered only -> rebuild those indexes.
3. Data pages, few -> **page restore** from backups plus log backups (online page restore needs Enterprise edition; other editions restore offline).
4. Widespread -> full restore + log chain to point of failure (tail-log backup first).
5. No backups -> `REPAIR_ALLOW_DATA_LOSS` as the last resort, on a copy first.

## Verify
Re-run `DBCC CHECKDB WITH NO_INFOMSGS` after the fix: `CHECKDB found 0 allocation errors and 0 consistency errors`.

## Checked
2026-11-01. Confirmed from the sql-docs GitHub markdown: DBCC CHECKDB page (`NO_INFOMSGS`, `ALL_ERRORMSGS`, `REPAIR_REBUILD` vs `REPAIR_ALLOW_DATA_LOSS`, restore-first advice, summary line text), the database engine error list (8905, 8906, 8928, 8939, 8946, 8951, 8952, 8956, 8976) and the restore-pages page (suspect_pages, online page restore on Enterprise edition, tail-log backup). Removed: `TABLERESULTS`, errors 2533 and 824, the object id < 100 rule and 823/824/825.
Method: documentation only; no commands were run.
