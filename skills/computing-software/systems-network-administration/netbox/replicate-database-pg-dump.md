---
id: computing-software.systems-network-administration.netbox.replicate-database-pg-dump
name: replicate-database-pg-dump
category: computing-software
field: systems-network-administration
product: netbox
tags: [pg-dump, database-replication, on-error-stop]
level: practitioner
status: docs-checked
description: "Dump, exclude changelog data and restore with ON_ERROR_STOP."
sources: ["https://netboxlabs.com/docs/netbox/administration/replicating-netbox/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replicating the database

Goal: copy production data to a dev or test instance.

NetBox uses PostgreSQL, so standard practice applies. The examples assume a database named `netbox`.

**Export**

```
pg_dump --username netbox --password --host localhost netbox > netbox.sql
```

Adjust user, host and database to your install. For development copies you can exclude the change log, which often makes up most of the size:

```
pg_dump ... --exclude-table-data=core_objectchange netbox > netbox.sql
```

**Restore.** Delete the existing database first to avoid conflicts. This destroys and replaces it:

```
psql -c 'drop database netbox'
psql -c 'create database netbox'
psql -v ON_ERROR_STOP=1 netbox < netbox.sql
```

**Always use ON_ERROR_STOP.** By default `psql` continues after an error and exits with status 0, so a restore missing an index, function or trigger can appear to succeed. With the flag the restore aborts on the first error, including unrelated ones such as an existing role. For non-plain dump formats use `pg_restore --exit-on-error`.

**Checklist**

1. Exclude `core_objectchange` for dev copies.
2. Drop and recreate before restoring.
3. Restore with `ON_ERROR_STOP=1`.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Replicating page: pg_dump with --exclude-table-data=core_objectchange, drop/create database restore, ON_ERROR_STOP explanation, pg_restore --exit-on-error. Removed: Nothing.

Method: documentation only; no commands were run.
