---
id: computing-software.database-administration.oracle-database.memory-management-sga-and-pga
name: memory-management-sga-and-pga
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-instance, sga-target, pga-aggregate-target, pga-aggregate-limit, memory-target, hugepages, ora-04031, ora-04036, memory-advisor, use-large-pages]
level: advanced
status: docs-checked
description: "Size Oracle SGA and PGA with ASMM, cap PGA with PGA_AGGREGATE_LIMIT, set USE_LARGE_PAGES instead of MEMORY_TARGET on Linux, and read the memory advisors."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-memory.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/tuning-program-global-area.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/USE_LARGE_PAGES.html
  - https://docs.oracle.com/en/error-help/db/ora-04036/
  - https://docs.oracle.com/en/error-help/db/ora-04031/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory management: SGA and PGA

## Pick the model
- **ASMM**: `SGA_TARGET` + `PGA_AGGREGATE_TARGET`. Oracle moves memory among buffer cache,
  shared pool, large pool and the other automatically sized SGA components.
- **AMM** (`MEMORY_TARGET`): one number for SGA+PGA. With `MEMORY_TARGET` set, `SGA_TARGET` and
  `PGA_AGGREGATE_TARGET` become minimums (set both to 0 for no minimums). With
  `USE_LARGE_PAGES = ONLY` you must not set `MEMORY_TARGET` or `MEMORY_MAX_TARGET` explicitly,
  or the instance will not start.
- Manual: individual pool sizes; only for special cases.
Setting an automatically sized component (e.g. `SHARED_POOL_SIZE`) under ASMM sets its **minimum**.

## Typical settings
```sql
ALTER SYSTEM SET memory_target = 0 SCOPE=SPFILE;
ALTER SYSTEM SET sga_max_size = 64G SCOPE=SPFILE;
ALTER SYSTEM SET sga_target   = 64G SCOPE=SPFILE;
ALTER SYSTEM SET pga_aggregate_target = 16G SCOPE=BOTH;
ALTER SYSTEM SET pga_aggregate_limit  = 32G SCOPE=BOTH;
ALTER SYSTEM SET use_large_pages = ONLY SCOPE=SPFILE;      -- instance fails to start if large pages cannot cover the whole SGA
```
The sizes are examples. Leave headroom for the OS and per-connection process memory.

## PGA_AGGREGATE_LIMIT
`PGA_AGGREGATE_TARGET` is a target, not a cap. `PGA_AGGREGATE_LIMIT` defaults to the greater of
2 GB, 200% of `PGA_AGGREGATE_TARGET`, or 3 MB x `PROCESSES`, and does not exceed 120% of physical
memory minus the total SGA; the default is printed in the alert log. When the limit is exceeded,
Oracle interrupts the largest sessions using PGA and raises `ORA-04036`
(action: raise the limit or reduce memory use). A per-consumer-group cap is also available
with `SESSION_PGA_LIMIT` in Resource Manager plan directives (`ORA-10260`).

## Large pages on Linux
`USE_LARGE_PAGES` applies only on Linux and is not modifiable on a running instance.
Values: `TRUE` (default on most systems), `FALSE` (not recommended: can severely degrade
performance), `AUTO`, `ONLY` (Oracle recommends it for consistent performance), `AUTO_ONLY`
(19c and later). Configure the operating system's huge pages for the SGA size using the
Oracle Database Installation Guide for Linux.

## Advisors and diagnosis
```sql
SELECT sga_size, sga_size_factor, estd_db_time_factor, estd_physical_reads FROM v$sga_target_advice;
SELECT pga_target_for_estimate/1048576 mb, estd_pga_cache_hit_percentage, estd_overalloc_count
FROM v$pga_target_advice;                -- want estd_overalloc_count = 0
SELECT component, current_size/1048576 mb, min_size/1048576 FROM v$sga_dynamic_components;
SELECT name, value/1048576 mb FROM v$pgastat WHERE name IN ('total PGA allocated','maximum PGA allocated','over allocation count');
SELECT * FROM v$memory_resize_ops ORDER BY start_time DESC;
```
- `ORA-04031` (unable to allocate shared memory): read the Cause and Action on the error page
  for the failing pool, and check `V$SGASTAT`.
- Frequent shrink/grow of components in `v$memory_resize_ops` suggests setting minimums
  for the affected components.

## Verify
- [ ] `memory_target = 0` on Linux when using `USE_LARGE_PAGES = ONLY`.
- [ ] `pga_aggregate_limit` set explicitly; `over allocation count` not growing.
- [ ] Advisors show little benefit from more memory at current sizes.

## Checked
2026-10-31. Confirmed in the Oracle Database 19c Administrator's Guide (Managing Memory), Performance
Tuning Guide (PGA), Database Reference (`USE_LARGE_PAGES`) and the ORA-04036 / ORA-04031 error
pages: ASMM/AMM minimum behaviour, the `PGA_AGGREGATE_LIMIT` default and 120% bound,
`USE_LARGE_PAGES` values, Linux-only scope and the `ONLY` / `MEMORY_TARGET` restriction,
`SESSION_PGA_LIMIT` and `ORA-10260`. Removed unconfirmed claims: ASMM "recommended on Linux",
`/dev/shm` and HugePages incompatibility wording, 60-70% RAM split, "12c+" note, sysctl/limits/
Transparent HugePages recipe, alert-log nr_hugepages hint, ORA-04031 cause guess, per-PDB
parameter note.
Method: documentation only; no commands were run.
