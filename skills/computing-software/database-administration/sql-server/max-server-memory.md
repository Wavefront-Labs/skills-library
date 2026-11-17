---
id: computing-software.database-administration.sql-server.max-server-memory
name: max-server-memory
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, max-server-memory, min-server-memory, sp-configure, sql-server-configuration, buffer-pool, memory-pressure, resource-semaphore, page-life-expectancy]
level: practitioner
status: docs-checked
description: "Size SQL Server max server memory so the OS, other services and non-buffer-pool allocations keep headroom, and confirm it with memory DMVs and counters."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/server-memory-server-configuration-options
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-sys-memory-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# max server memory

**Goal:** stop SQL Server taking every byte of RAM (the default 2,147,483,647 MB) and
starving the OS into paging, without leaving memory idle.

## Starting value
Since SQL Server 2019, Windows Setup recommends a value; for older or upgraded instances compute it.
Microsoft's generic approach for a single instance with no monitoring history:
- from total OS memory subtract thread memory outside the cap: thread stack size x calculated max worker threads
  (stack size per architecture is in the memory management architecture guide);
- then subtract 25% for other allocations outside the cap (backup buffers, extended-procedure DLLs, `sp_OA` objects, linked-server providers),
  a generic approximation;
- subtract memory for other instances and applications on the host.
The documented table lists 75% of available memory not used by other processes as the recommended value.
The default is 2,147,483,647 MB and the minimum is 128 MB (the minimum can stop SQL Server starting; recover by starting with `-f`).
Do not set min and max equal or close.

```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'max server memory (MB)', 112640; RECONFIGURE;   -- example value; takes effect immediately, no restart
EXEC sp_configure 'min server memory (MB)', 0;      RECONFIGURE;   -- default 0; Microsoft calls a min value essential on VMs
```

## What it covers
The documentation note says the option limits the size of the buffer pool and does not limit the remaining unreserved area used by
extended stored procedures, COM objects, non-shared DLLs and EXEs (thread stacks and similar also sit outside, per the formula above).
Columnstore and In-Memory OLTP objects have their own memory clerks (`sys.dm_os_memory_clerks`).

## Several instances on one host
Give each instance an explicit max that together leave OS headroom. Without caps,
instances compete; Microsoft notes the first instances presented with a workload tend to take all memory.

## Verify headroom
```sql
SELECT total_physical_memory_kb/1024 AS total_mb,
       available_physical_memory_kb/1024 AS avail_mb,
       system_memory_state_desc
FROM sys.dm_os_sys_memory;          -- states: high / low / steady / transitioning ("Available physical memory is low" = pressure)
SELECT physical_memory_in_use_kb/1024 AS sql_mb, memory_utilization_percentage
FROM sys.dm_os_process_memory;
```

## Gotchas
- On VMs, set `min server memory` so host pressure cannot deallocate more of the buffer pool than acceptable (Microsoft's guidance).
- Lock pages in memory changes how trimming works: see
  `computing-software.database-administration.sql-server.instant-file-initialization-and-lock-pages-in-memory`.

## Verify
- [ ] `max server memory (MB)` is not the default on every instance.
- [ ] `sys.dm_os_sys_memory` does not report low memory under peak load; no hard paging.
- [ ] Sum of caps across instances plus other services is below physical RAM.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 Server Memory Configuration Options and sys.dm_os_sys_memory pages (2017-2025).
Confirmed: default 2,147,483,647 MB and minimum 128 MB, setup recommendation from 2019, the stack-size plus 25% sizing method and 75% table value, dynamic change without restart, buffer-pool scope note, `sys.dm_os_sys_memory` columns and state values. Removed the unconfirmed 1 GB per 4/8 GB community rule, the Perfmon thresholds, dbatools commands and the wait-type advice.
Method: documentation only; no commands were run.
