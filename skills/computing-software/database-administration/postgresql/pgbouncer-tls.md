---
id: computing-software.database-administration.postgresql.pgbouncer-tls
name: pgbouncer-tls
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pgbouncer-tls, pgbouncer, client-tls, server-tls, sslmode, encryption-in-transit]
level: practitioner
status: docs-checked
description: "Configure PgBouncer TLS on both legs: client_tls_* for apps to PgBouncer and server_tls_* for PgBouncer to PostgreSQL, with verification and checks."
sources:
  - https://www.pgbouncer.org/config.html#tls-settings
  - https://www.postgresql.org/docs/current/libpq-ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PgBouncer TLS (client_tls / server_tls)

PgBouncer terminates TLS: client connections and server connections are configured independently. Encrypting one leg says nothing about the other.

## Client side (apps -> PgBouncer)
```ini
[pgbouncer]
client_tls_sslmode = require            # disable | allow | prefer | require | verify-ca | verify-full
client_tls_key_file = /etc/pgbouncer/server.key
client_tls_cert_file = /etc/pgbouncer/server.crt
client_tls_ca_file = /etc/pgbouncer/ca.crt   # needed for verify-ca/verify-full (client certificates)
client_tls_protocols = tlsv1.2,tlsv1.3
```
- `require` here means PgBouncer refuses non-TLS clients. Clients still need `sslmode=verify-full` and the CA to authenticate PgBouncer.
- Client certificate auth: `client_tls_sslmode = verify-full` + `auth_type = cert`; the cert CN must match the user name.
- Key file must be readable only by the pgbouncer user (`chmod 600`).

## Server side (PgBouncer -> PostgreSQL)
```ini
server_tls_sslmode = verify-full
server_tls_ca_file = /etc/pgbouncer/pg-ca.crt
# optional client cert for PgBouncer itself:
server_tls_key_file = /etc/pgbouncer/pgbouncer-client.key
server_tls_cert_file = /etc/pgbouncer/pgbouncer-client.crt
```
`verify-full` checks the hostname in `[databases]` entries against the server certificate; use the DNS name there, not an IP, unless the cert has an IP SAN.

## Apply and check
```bash
kill -HUP $(pidof pgbouncer)       # or RELOAD in the admin console; since 1.24.0 connections are recycled only if the TLS settings changed
psql "host=pgb1 port=6432 dbname=app sslmode=verify-full sslrootcert=ca.crt" -c "SHOW ssl;"
```
Admin console:
```
SHOW CLIENTS;   -- tls column per client
SHOW SERVERS;   -- tls column for server connections
```
On PostgreSQL: `SELECT ssl, version FROM pg_stat_ssl JOIN pg_stat_activity USING (pid) WHERE application_name LIKE '%pgbouncer%' OR client_addr = '<PGB_IP>';`

## Gotchas
- With `server_tls_sslmode = prefer` PgBouncer falls back to plaintext if the server has no TLS (libpq documents `prefer` as not recommended for secure deployments).
- TLS handshakes on the client side cost CPU in PgBouncer's single thread; with many short-lived client connections this can cap throughput (see running multiple PgBouncer processes).

## Checked

2026-10-28. Confirmed against the PgBouncer config TLS settings section (client_tls_* and server_tls_* settings), changelog (1.24.0: connections not recycled on RELOAD if TLS config is unchanged) and the libpq SSL page (sslmode semantics, prefer not recommended). Corrected: the claim that TLS file changes only affect new connections (the changelog describes recycling when settings change). Removed: default value claim for server_tls_sslmode, example cipher string and the channel-binding note.

Method: documentation only; no commands were run.
