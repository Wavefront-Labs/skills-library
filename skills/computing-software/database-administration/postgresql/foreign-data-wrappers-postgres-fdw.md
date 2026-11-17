---
id: computing-software.database-administration.postgresql.foreign-data-wrappers-postgres-fdw
name: foreign-data-wrappers-postgres-fdw
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres-extensions, postgres-fdw, foreign-data-wrapper, file-fdw, import-foreign-schema, data-migration]
level: practitioner
status: docs-checked
description: "Query remote PostgreSQL tables and files with postgres_fdw and file_fdw: server, user mapping, IMPORT FOREIGN SCHEMA, pushdown checks, batching and security."
sources:
  - https://www.postgresql.org/docs/current/postgres-fdw.html
  - https://www.postgresql.org/docs/current/file-fdw.html
  - https://www.postgresql.org/docs/current/sql-importforeignschema.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Foreign data wrappers (postgres_fdw / file_fdw)

## postgres_fdw setup
```sql
CREATE EXTENSION postgres_fdw;
CREATE SERVER billing_srv FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'billing-db', port '5432', dbname 'billing',
           fetch_size '10000', use_remote_estimate 'true', sslmode 'verify-full');
CREATE USER MAPPING FOR app_reporting SERVER billing_srv
  OPTIONS (user 'reporting_ro', password '...');
CREATE SCHEMA billing_remote;
IMPORT FOREIGN SCHEMA public LIMIT TO (invoices, customers)
  FROM SERVER billing_srv INTO billing_remote;
GRANT USAGE ON FOREIGN SERVER billing_srv TO app_reporting;
```

## Check pushdown
```sql
EXPLAIN (VERBOSE) SELECT customer_id, sum(amount) FROM billing_remote.invoices
WHERE issued_at >= '2026-01-01' GROUP BY 1;
```
EXPLAIN VERBOSE shows the query actually sent to the remote server. A join between foreign tables on the **same foreign server** is sent as one join unless the planner thinks fetching rows separately is cheaper or the tables use different user mappings. Only immutable functions and operators that are built in, or that belong to an extension listed in the server's `extensions` option, can be shipped to the remote side.

## Performance options
- `fetch_size` (default 100) is the number of rows per fetch: raise for large scans.
- `use_remote_estimate 'true'`: planner asks the remote side for row estimates (extra
  round trip per plan); otherwise `ANALYZE` the foreign table locally.
- `batch_size` sets how many rows are inserted per insert operation; `async_capable` lets
  scans of several foreign tables run asynchronously (see the options list).

## file_fdw for CSV and logs
```sql
CREATE EXTENSION file_fdw;
CREATE SERVER files FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE import_users (id int, email text)
  SERVER files OPTIONS (filename '/data/import/users.csv', format 'csv', header 'true');
-- or OPTIONS (program 'gunzip -c /data/import/users.csv.gz', format 'csv')
```
Reading files needs superuser or `pg_read_server_files`; `program` needs `pg_execute_server_program`.

## Security
- Non-superusers must supply a password in the user mapping (`password_required`), which
  stops them borrowing the local server's identity via peer/trust on the remote.
- Use a dedicated read-only remote role for the mapping.
- The `use_scram_passthrough` option (foreign server or user mapping) lets postgres_fdw use SCRAM
  pass-through authentication instead of a stored password; see the postgres_fdw options.

## Uses
Migrations between databases (`INSERT INTO local SELECT * FROM remote`), cross-database
reporting, archiving old partitions to another server as foreign partitions.

## Verify
`SELECT count(*) FROM billing_remote.invoices;` works as the intended role, and EXPLAIN
VERBOSE shows filters inside `Remote SQL`.

## Checked

2026-10-28. Confirmed against PostgreSQL docs (version 18) postgres_fdw and file_fdw pages and IMPORT FOREIGN SCHEMA: fetch_size default 100, use_remote_estimate, batch_size, async_capable, extensions option and shippability, same-server join pushdown, EXPLAIN VERBOSE shows the remote query, password_required, pg_read_server_files / pg_execute_server_program. Fixed: the option is use_scram_passthrough, not scram_client_key. Removed unconfirmed: PG14+ version tags, pg_user_mappings visibility note, local-table join advice, the `Remote SQL:` label.

Method: documentation only; no commands were run.
