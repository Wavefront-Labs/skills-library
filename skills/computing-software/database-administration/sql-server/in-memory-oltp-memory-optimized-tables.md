---
id: computing-software.database-administration.sql-server.in-memory-oltp-memory-optimized-tables
name: in-memory-oltp-memory-optimized-tables
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, in-memory-oltp, memory-optimized-tables, natively-compiled-procedures, hash-index, memory-optimized-tempdb-metadata, resource-pool]
level: advanced
status: docs-checked
description: "Adopt SQL Server In-Memory OLTP: memory-optimized filegroup, durable and non-durable tables, hash vs range indexes, native procedures, memory sizing and monitoring."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/overview-and-usage-scenarios
  - https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/estimate-memory-requirements-for-memory-optimized-tables
  - https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/bind-a-database-with-memory-optimized-tables-to-a-resource-pool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-Memory OLTP (memory-optimized tables)

Memory-optimized tables held in memory. The gain depends on the workload; non-durable
tables (`SCHEMA_ONLY`) avoid log IO where durability is not needed.

## Enable
```sql
ALTER DATABASE appdb ADD FILEGROUP appdb_mod CONTAINS MEMORY_OPTIMIZED_DATA;
ALTER DATABASE appdb ADD FILE (NAME = 'appdb_mod1', FILENAME = '<DATA_DIR>/appdb_mod1') TO FILEGROUP appdb_mod;
ALTER DATABASE appdb SET MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = ON;
```

## Tables
```sql
CREATE TABLE dbo.SessionState (
  SessionId uniqueidentifier NOT NULL PRIMARY KEY NONCLUSTERED HASH WITH (BUCKET_COUNT = 2000000),
  UserId int NOT NULL INDEX ix_user NONCLUSTERED,
  Payload varbinary(8000), ExpiresAt datetime2 NOT NULL)
WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA);  -- SCHEMA_ONLY = lost on restart, no log
```
- Hash index: sized with `BUCKET_COUNT`; size it for your expected number of distinct keys.
- Nonclustered index: for range scans and ordering.
- Table types for TVPs/temp data: `CREATE TYPE dbo.IdList AS TABLE (Id int PRIMARY KEY NONCLUSTERED) WITH (MEMORY_OPTIMIZED = ON);`

## Natively compiled procedures
```sql
CREATE PROCEDURE dbo.usp_TouchSession @SessionId uniqueidentifier
WITH NATIVE_COMPILATION, SCHEMABINDING AS
BEGIN ATOMIC WITH (TRANSACTION ISOLATION LEVEL = SNAPSHOT, LANGUAGE = N'us_english')
  UPDATE dbo.SessionState SET ExpiresAt = DATEADD(minute, 20, SYSUTCDATETIME()) WHERE SessionId = @SessionId;
END;
```
Supported T-SQL surface is restricted; interop (normal T-SQL against memory-optimized tables) works for most code.

## Memory
Start with two times the expected size of the memory-optimized tables and indexes, then observe
actual consumption. Bind the database to a resource pool so a
runaway table cannot starve the buffer pool:
```sql
CREATE RESOURCE POOL Pool_IMOLTP WITH (MIN_MEMORY_PERCENT = 30, MAX_MEMORY_PERCENT = 30);
ALTER RESOURCE GOVERNOR RECONFIGURE;
EXEC sp_xtp_bind_db_resource_pool 'appdb', 'Pool_IMOLTP';
```

## Verify
Memory use stays within the resource pool limit under a realistic load test.

## Checked
2026-10-28. Confirmed against the In-Memory OLTP overview and memory-optimized table pages: MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT recommendation, hash index with BUCKET_COUNT, DURABILITY = SCHEMA_ONLY avoids IO, NATIVE_COMPILATION with SCHEMABINDING, start with two times the expected size of memory-optimized tables and indexes, sp_xtp_bind_db_resource_pool taking a database name and a pool name.
Removed unconfirmed claims: use-case list, "filegroup cannot be removed", bucket-count ratio, Bw-tree detail, error 41805, the monitoring DMV queries, tempdb metadata section, conflict error numbers and recovery/ALTER gotchas.
Method: documentation only; no commands were run.
