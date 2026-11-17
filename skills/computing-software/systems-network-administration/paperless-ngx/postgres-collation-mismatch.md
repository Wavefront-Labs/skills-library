---
id: computing-software.systems-network-administration.paperless-ngx.postgres-collation-mismatch
name: postgres-collation-mismatch
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, postgresql, collation-version-mismatch, glibc, reindex, docker]
level: advanced
status: docs-checked
description: "Handle the PostgreSQL 'collation version mismatch' warning: why it appears after image updates and how to reindex and refresh it."
sources:
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL collation version mismatch

## The warning
The PostgreSQL log shows a warning like:
```
WARNING:  database "paperless" has a collation version mismatch
DETAIL:  The database was created using collation version 2.36, but the operating system provides version 2.41.
HINT:  Rebuild all objects in this database that use the default collation and run ALTER DATABASE paperless REFRESH COLLATION VERSION, or build PostgreSQL with the right library version.
```

## What it means
This comes from PostgreSQL, not Paperless-ngx. The `glibc` version that PostgreSQL runs against changed, and the existing database was created with an older one. With Docker, `glibc` comes from the PostgreSQL image's Debian base, not the host, so this commonly happens when a new image is pulled after its base Debian release changed. If PostgreSQL is installed directly on a host, it uses the host's `glibc` instead.

The warning is not an error and Paperless-ngx keeps working, but the database's text indexes may be built with outdated sorting rules.

## Resolve
Back up your database, then connect to it (for example with `psql -U paperless -d paperless` inside the database container) and run:
```sql
REINDEX DATABASE paperless;
ALTER DATABASE paperless REFRESH COLLATION VERSION;
```

## Prevent
Pin your PostgreSQL image to a specific Debian release, for example `postgres:18-trixie`, rather than `postgres:18`.

## Checked
Date: 2026-11-07
Pages read in full: troubleshooting section "PostgreSQL warns about a collation version mismatch" read in full; the rest of the troubleshooting page was not read for this skill.
Corrections: added the HINT line of the warning; removed "so base image changes happen when you choose" and the closing note about major PostgreSQL upgrades (neither is in that section); the rest matched the page.
Method: documentation only; no commands were run.
