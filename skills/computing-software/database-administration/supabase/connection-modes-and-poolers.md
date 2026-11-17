---
id: computing-software.database-administration.supabase.connection-modes-and-poolers
name: connection-modes-and-poolers
category: computing-software
field: database-administration
product: supabase
tags: [connections, pooler, transaction-mode, ipv4, prepared-statements]
level: practitioner
status: docs-checked
description: "Pick the right Supabase Postgres connection: direct, shared pooler session or transaction, dedicated pooler, with ports, usernames and driver flags."
sources:
  - https://supabase.com/docs/guides/database/connecting-to-postgres
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose a connection mode that fits the workload.

- Direct: `db.[PROJECT-REF].supabase.co:5432`. IPv6 (IPv4 with the add-on). For persistent backends, migrations, `pg_dump`, backup/restore and replication.
- Shared pooler, session: `aws-[INDEX]-[REGION].pooler.supabase.com:5432`. IPv4. For IPv4-only backends and third-party tools.
- Shared pooler, transaction: same host, port `6543`. For serverless and edge functions.
- Dedicated pooler, transaction: `db.[PROJECT-REF].supabase.co:6543`. Pro and above, for high-load apps; transaction mode only, prepared statements supported on PgBouncer 1.21 and later.

Usernames: `postgres` for direct and dedicated pooler; `postgres.[PROJECT-REF]` for the shared pooler; `[ROLE].[PROJECT-REF]` for a custom role through it. Copy the pooler host from the Connect dialog, since `[INDEX]` cannot be derived from the region. The IPv4 add-on is not dual-stack; it replaces the IPv6 record.

Transaction mode loses session state between transactions: `set`/`reset`, session advisory locks, `LISTEN`/`NOTIFY` and temporary tables. Cursors work only inside one transaction, and pipelining is unsupported.

Disable prepared statements for the shared pooler in transaction mode (the dedicated pooler supports them): Postgres.js and Drizzle `prepare: false`; Prisma `pgbouncer=true`; asyncpg `statement_cache_size=0`; JDBC `prepareThreshold=0`.

Serverless: create the client at module scope, pool size 1, SSL `require`. Postgres.js defaults to 10 connections per instance. For verified TLS use `sslmode=verify-full` with `sslrootcert` from Database settings. Percent-encode reserved password characters.

## Checked

2026-11-04: Read the Connect to your database guide in full. Confirmed hosts, ports, usernames, plan and IPv4 notes, transaction-mode limitations, the driver settings table, serverless client settings and the SSL advice. Narrowed the prepared-statement advice to transaction mode, as the page words it.
Method: documentation only; no commands were run.
