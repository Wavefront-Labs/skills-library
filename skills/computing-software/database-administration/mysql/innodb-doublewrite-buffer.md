---
id: computing-software.database-administration.mysql.innodb-doublewrite-buffer
name: innodb-doublewrite-buffer
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, doublewrite-buffer, torn-pages, innodb-doublewrite, innodb-doublewrite-files, crash-safety, mysql-storage]
level: practitioner
status: docs-checked
description: "Understand the InnoDB doublewrite buffer that prevents torn-page corruption, configure doublewrite files in 8.0.20+, and know when disabling it is safe."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-doublewrite-buffer.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_doublewrite
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The doublewrite buffer

InnoDB pages are 16 KB; disks and filesystems often guarantee atomic writes of only 4 KB. A crash mid-write leaves a **torn page** (half old, half new) that redo cannot fix, because redo records are changes applied to a valid page. InnoDB first writes pages to the doublewrite area, fsyncs, then writes them to their real location. On recovery, a torn page is restored from its doublewrite copy.

## Configuration (8.0.20+)
Doublewrite moved out of the system tablespace into separate files:
```ini
[mysqld]
innodb_doublewrite = ON                    # ON | OFF | DETECT_AND_RECOVER (same as ON) | DETECT_ONLY
innodb_doublewrite_dir = /fastdisk/dblwr   # default: innodb_data_home_dir (itself datadir by default)
innodb_doublewrite_files = 2               # default 2: a flush-list file and an LRU-list file per buffer pool instance
innodb_doublewrite_pages = 128             # max doublewrite pages per thread; advanced tuning, default is fine
```
Files appear as `#ib_16384_0.dblwr` etc. (`.bdblwr` with `DETECT_ONLY`). Changing between `ON`, `DETECT_AND_RECOVER` and `DETECT_ONLY` can be done dynamically; changing between any of those and `OFF` cannot.

- `DETECT_ONLY`: writes only metadata, so torn pages are detected but not repaired (less write amplification; you then need a backup/replica to fix).

## When OFF is acceptable
- Filesystem or storage guarantees atomic 16 KB writes (verify the vendor's documented guarantee for your exact stack).
- Disposable instances during initial bulk loads (re-enable afterwards; switching to or from `OFF` needs a restart).
Otherwise keep it ON: torn pages surface later as `Database page corruption` with no clean fix except restore.

## Check it works
```sql
SHOW GLOBAL STATUS LIKE 'Innodb_dblwr%';    -- Innodb_dblwr_pages_written, Innodb_dblwr_writes
SELECT @@innodb_doublewrite, @@innodb_doublewrite_dir;
```

## Gotchas
- Disabling doublewrite and also `innodb_flush_log_at_trx_commit != 1` stacks risks; know which guarantees you are giving up.
- `innodb_doublewrite_dir` is read at startup; plan a restart to change it.

## Checked
Date 2026-11-01. Documentation release: MySQL 8.4 Reference Manual, Doublewrite Buffer.
Confirmed: DETECT_AND_RECOVER equals ON, DETECT_ONLY metadata-only behaviour, dynamic-change rules, innodb_doublewrite_dir default, innodb_doublewrite_files default and file naming, innodb_doublewrite_pages meaning. Corrected the 8.0.30 version note, file naming for DETECT_ONLY and the pages description. Removed unconfirmed claims: named storage examples, the throughput claim and the directory-move procedure.
Method: documentation only; no commands were run.

