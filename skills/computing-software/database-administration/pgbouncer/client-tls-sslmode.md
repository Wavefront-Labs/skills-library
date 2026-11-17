---
id: computing-software.database-administration.pgbouncer.client-tls-sslmode
name: client-tls-sslmode
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, tls, client-tls, sslmode, certificates]
level: practitioner
status: docs-checked
description: "client_tls_sslmode values and the key, cert and CA files for accepting TLS connections from clients."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enable TLS for client connections to PgBouncer.

TLS from clients is disabled by default. When enabled, `client_tls_key_file` and `client_tls_cert_file` must also be set. PEM is the most common file format.

`client_tls_sslmode`:

- `disable` (default): plain TCP; a TLS request from the client is ignored.
- `allow`: use TLS if the client requests it, otherwise plain TCP. A client certificate, if presented, is not validated.
- `prefer`: same as allow.
- `require`: client must use TLS or is rejected. A presented client certificate is not validated.
- `verify-ca`: client must use TLS with a valid client certificate.
- `verify-full`: same as verify-ca.

File settings (all default not set):

- `client_tls_key_file`: private key PgBouncer uses to accept client connections.
- `client_tls_cert_file`: certificate for that key; clients can validate it.
- `client_tls_ca_file`: root certificate used to validate client certificates.

```
client_tls_sslmode = verify-ca
client_tls_key_file = /path/to/server.key
client_tls_cert_file = /path/to/server.crt
client_tls_ca_file = /path/to/root.crt
```

Pair verify-ca with `auth_type = cert` to take the user name from the certificate CommonName. If the content of a cert or key file changes without changing the filename setting, RELOAD makes new connections use it; existing connections stay open, so run RECONNECT after RELOAD if everything must move to the new files. Changing any TLS setting triggers a RECONNECT automatically.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
