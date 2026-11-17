---
id: computing-software.database-administration.pgbouncer.cert-authentication
name: cert-authentication
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, cert, client-certificate, tls, auth-type]
level: advanced
status: docs-checked
description: "auth_type cert: authenticate clients by TLS client certificate CommonName, with the required TLS settings."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use client certificates instead of passwords.

`auth_type = cert`: the client must connect over TLS with a valid client certificate, and the user name is taken from the certificate's CommonName field.

Required TLS configuration for client connections:

```
auth_type = cert
client_tls_sslmode = verify-ca
client_tls_key_file = /path/to/server.key
client_tls_cert_file = /path/to/server.crt
client_tls_ca_file = /path/to/root.crt
```

`client_tls_sslmode` values `verify-ca` and `verify-full` (equivalent) require TLS with a valid client certificate; `allow`, `prefer` and `require` do not validate a presented certificate, so they are not enough to validate identities. The CA file validates the certificates.

Under `auth_type = hba` you can set cert per access path, and the user name map (`map=`) parameter is supported for cert and peer methods; the map comes from `auth_ident_file`, with lines `map-name system-username database-username`.

Backend login still needs a password source if the PostgreSQL server requires one: the auth_file entry, a `password=` in the database definition, or auth_user.

Changing any TLS setting triggers an automatic RECONNECT. If only the contents of certificate files change, run RELOAD for new connections and RECONNECT to push existing ones onto the new files.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
