---
id: computing-software.database-administration.postgresql.ssl-tls-connections-and-hostssl
name: ssl-tls-connections-and-hostssl
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, client-authentication, postgres-ssl, sslmode, hostssl, tls, verify-full, certificates, encryption-in-transit]
level: practitioner
status: docs-checked
description: "Enable TLS on a PostgreSQL server, force it with hostssl rules, and make clients actually verify the server with sslmode=verify-full."
sources:
  - https://www.postgresql.org/docs/current/ssl-tcp.html
  - https://www.postgresql.org/docs/current/libpq-ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS for PostgreSQL connections

**Goal:** every remote connection is encrypted and clients refuse to talk to an impostor.

## Server side
```conf
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'          # relative to data dir, or absolute
ssl_key_file  = 'server.key'
ssl_ca_file   = 'root.crt'            # only needed to verify client certs
ssl_min_protocol_version = 'TLSv1.2'
```
With `sslmode=verify-full` the server host name must match the name in the certificate.

Force TLS in pg_hba.conf — first match wins, so put `hostnossl ... reject` first
or only use `hostssl` lines:
```
hostnossl all all 0.0.0.0/0  reject
hostssl   all all 0.0.0.0/0  scram-sha-256
```
`host` matches both TLS and plain; it does not force anything.

## Client side: sslmode
| sslmode | Encrypts | Verifies CA | Verifies hostname |
|---|---|---|---|
| disable/allow/prefer (default) | maybe | no | no |
| require | yes | no (unless root.crt present) | no |
| verify-ca | yes | yes | no |
| verify-full | yes | yes | yes |

`prefer` is the libpq default and, as the docs put it, makes no sense from a security point of view. Use
`sslmode=verify-full sslrootcert=<ca.pem>`. Without verification, TLS stops eavesdropping but not MITM.

## Rotation
Replace the certificate and key files and reload the configuration; check expiry dates and alert before they pass.

## Gotchas
- Managed services ship their own CA bundle; download it for verify-full.
- A pooler terminates TLS separately from the database; configure TLS on both hops.

## Verify
```sql
SELECT pid, ssl, version, cipher FROM pg_stat_ssl JOIN pg_stat_activity USING (pid)
WHERE client_addr IS NOT NULL;   -- ssl = t for every remote row
```
`psql "host=db.example.com sslmode=verify-full ..."` connects; with a wrong
hostname the connection must fail.

## Checked

2026-10-28. Confirmed against PostgreSQL docs (version 18): libpq SSL support (sslmode levels, default prefer, verify-full checks host name, require verifies only if a root certificate is present), pg_hba.conf record types hostssl / hostnossl, ssl_min_protocol_version, pg_stat_ssl. Removed unconfirmed: PG10 reload note, key file ownership and mode, SAN and chain remarks, sslrootcert=system, rotation behaviour of existing sessions, openssl expiry command, the key permission error text, PgBouncer parameter names.

Method: documentation only; no commands were run.
