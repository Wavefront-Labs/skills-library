---
id: computing-software.systems-network-administration.paperless-ngx.sqlite-locked-database
name: sqlite-locked-database
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, sqlite, db-locked, paperless-db-timeout, wal, paperlesstask]
level: practitioner
status: docs-checked
description: "Resolve 'Creating PaperlessTask failed: db locked' on SQLite installs by moving to PostgreSQL or giving SQLite more time and WAL mode."
sources:
  - "https://docs.paperless-ngx.com/troubleshooting/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log says "Creating PaperlessTask failed"

## Symptom
```
[ERROR] [paperless.management.consumer] Creating PaperlessTask failed: db locked
```

## Cause
You are likely using a SQLite installation with an increased number of workers and are running into SQLite's concurrency limitations. Uploading or consuming multiple files at once results in many workers attempting to access the database simultaneously.

## Options
1. Consider changing to PostgreSQL if you will be processing many documents at once often.
2. Otherwise give the database more time to unlock. In v3 `PAPERLESS_DB_TIMEOUT` is removed; the configuration page says to use `PAPERLESS_DB_OPTIONS` instead, with this SQLite example:
```bash
PAPERLESS_DB_OPTIONS="timeout=30"
```
3. The troubleshooting page also suggests SQLite "Write-Ahead Logging". The v3 configuration page says SQLite connections are already pre-configured with WAL journal mode, optimised synchronous and cache settings, and a 5-second busy timeout. To override `init_command`, use `;` between PRAGMAs and `,` between options.
4. `PAPERLESS_TASK_WORKERS` (default 1) sets how many background things Paperless does in parallel, so lowering it reduces simultaneous work. The docs do not tie it to this error directly.

The troubleshooting page says these changes may have minor performance implications but can help prevent database locking issues.

## Low-powered devices
The setup page for less powerful devices advises sticking with SQLite to save resources, and points to this troubleshooting entry if you hit SQLite locking. The same page suggests lowering task workers and threads per worker (example: 2 workers and 1 thread) on a 4-core Raspberry Pi.

## Checked
Date: 2026-11-07
Pages read in full: none of the three in full. I read the relevant sections of troubleshooting (the PaperlessTask section), configuration (PAPERLESS_DB_OPTIONS, PAPERLESS_DB_TIMEOUT, TASK_WORKERS, THREADS_PER_WORKER) and setup (less powerful devices); other sections of those pages were not read for this skill.
Corrections: removed the claim that the old DB_TIMEOUT "maps to" the timeout option (the page says it is removed, use DB_OPTIONS); reworded the options as the page words them rather than "in order of preference"; qualified the worker-count option as not tied to this error by the docs; removed the "duplicate-key warnings are harmless" line (the page says Paperless handles it and the file is still consumed, in the polling case) and added the setup page as a source.
Method: documentation only; no commands were run.
