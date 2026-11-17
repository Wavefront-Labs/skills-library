---
id: computing-software.database-administration.mysql.encrypted-connections-tls
name: encrypted-connections-tls
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-security, mysql-tls, require-secure-transport, ssl-mode, verify-identity, require-ssl, certificate-rotation, encryption-in-transit]
level: practitioner
status: docs-checked
description: "Enforce TLS for MySQL connections: server certs, require_secure_transport or per-account REQUIRE SSL, client ssl-mode VERIFY_IDENTITY, and rotating certs without restart."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/using-encrypted-connections.html
  - https://dev.mysql.com/doc/refman/8.4/en/connection-options.html#option_general_ssl-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS for MySQL connections

**Goal:** no plaintext connections, and clients verify they talk to the real server.

## Server
Without ssl options the server may enable encrypted connections itself with an
automatically created self-signed certificate (it logs a warning); VERIFY_IDENTITY
does not work with those. Use CA-issued certs:
```ini
[mysqld]
ssl_ca   = /etc/mysql/tls/ca.pem
ssl_cert = /etc/mysql/tls/server-cert.pem
ssl_key  = /etc/mysql/tls/server-key.pem
tls_version = TLSv1.2,TLSv1.3
require_secure_transport = ON      # reject any non-TLS TCP connection (unix socket still allowed)
```
Per account instead of global:
```sql
ALTER USER 'app'@'%' REQUIRE SSL;                      -- any TLS
ALTER USER 'svc'@'%' REQUIRE X509;                     -- client cert required
ALTER USER 'svc'@'%' REQUIRE SUBJECT '/CN=svc';        -- specific client cert
```

## Client ssl-mode
| `--ssl-mode` | Encrypt | Verify CA | Verify hostname |
|---|---|---|---|
| PREFERRED (default) | if possible | no | no |
| REQUIRED | yes | no | no |
| VERIFY_CA | yes | yes | no |
| VERIFY_IDENTITY | yes | yes | yes |
```bash
mysql --host db.example.com --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem -u app -p
```

## Rotate certs without restart
Replace the files at the configured paths (needs `CONNECTION_ADMIN`), then:
```sql
ALTER INSTANCE RELOAD TLS;
```
Existing connections are unaffected; new ones use the new context. If the new context cannot be created the statement rolls back by default and the old one stays in use.

## Gotchas
- Only VERIFY_CA and VERIFY_IDENTITY verify the server certificate; the latter also checks the host name.
- `REQUIRE X509` accounts need at least `--ssl-cert` and `--ssl-key` on the client, plus `--ssl-ca` to verify the server.
- `tls_version` tightening locks out clients that only speak the removed protocols.

## Verify
```sql
SHOW SESSION STATUS LIKE 'Ssl_version';     -- TLS version in use
```

## Checked
2026-11-01. Confirmed against MySQL 8.4 "Using Encrypted Connections": require_secure_transport (TCP must use SSL, socket allowed), ALTER INSTANCE RELOAD TLS behaviour, ssl-mode PREFERRED default and VERIFY_CA / VERIFY_IDENTITY behaviour, REQUIRE X509/SUBJECT client needs, self-signed auto certificates. Removed: Connector/J string, replication SOURCE_SSL options, MariaDB note, the 8.0.16 version tag, the status_by_thread query.
Method: documentation only; no commands were run.
