---
id: computing-software.database-administration.pgbouncer.server-tls-sslmode
name: server-tls-sslmode
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, tls, server-tls, sslmode, verify-full]
level: practitioner
status: docs-checked
description: "server_tls_sslmode values and the CA, key and cert files for TLS from PgBouncer to PostgreSQL."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: secure the PgBouncer-to-PostgreSQL leg with TLS.

`server_tls_sslmode` (default `prefer`):

- `disable`: plain TCP; TLS is not even requested.
- `allow`: the docs mark its behaviour as FIXME (whether a rejected plain connection retries with TLS).
- `prefer` (default): TLS is requested first from PostgreSQL; if refused, plain TCP is used. The server certificate is not validated.
- `require`: must use TLS; if the server rejects it, plain TCP is not attempted. The server certificate is not validated.
- `verify-ca`: TLS, and the server certificate must be valid according to server_tls_ca_file. The host name is not checked.
- `verify-full`: as verify-ca, and the server host name must match the certificate.

Files (default not set):

- `server_tls_ca_file`: root certificate that validates PostgreSQL server certificates.
- `server_tls_key_file`: private key PgBouncer uses to authenticate to PostgreSQL.
- `server_tls_cert_file`: certificate for that key; the server can validate it.

```
server_tls_sslmode = verify-full
server_tls_ca_file = /path/to/root.crt
server_tls_key_file = /path/to/client.key
server_tls_cert_file = /path/to/client.crt
```

Also `server_tls_protocols` (default `secure`; shortcuts all, secure, legacy where legacy means all), `server_tls_ciphers` (default `default`, TLS 1.2 and lower) and `server_tls13_ciphers` (default empty, falls back to server_tls_ciphers). Changing a TLS setting triggers an automatic RECONNECT; changed file contents behind an unchanged filename are used by new connections after RELOAD.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
