---
id: computing-software.devops-ci-cd.gitea.database-tls
name: database-tls
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-database-tls, gitea, postgresql-ssl, mysql-ssl, clientcert-verify-full, sslmode-verify-full, two-way-tls]
level: advanced
status: docs-checked
description: "Encrypt the Gitea to database link: PostgreSQL two-way TLS with client certs and pg_hba clientcert, MySQL/MariaDB one-way TLS with REQUIRE SSL."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/database-preparation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database connection over TLS

Only needed when the DB is on a public network; same-host or private-network setups can skip it. Prerequisites: a server cert and a client cert signed by a trusted CA. The server cert needs `TLS Web Server Authentication` in Extended Key Usage and its SAN/CN must be the DB FQDN. The client cert needs `TLS Web Client Authentication` and a SAN/CN containing the DB username Gitea uses. Connect by domain name (DNS or hosts-file entries), not IP.

## PostgreSQL (two-way TLS)
Server `postgresql.conf`:
```ini
ssl = on
ssl_ca_file = '/path/to/root.crt'
ssl_cert_file = '/path/to/postgresql.crt'
ssl_key_file = '/path/to/postgresql.key'
ssl_min_protocol_version = 'TLSv1.2'
```
Files must be owned by `postgres` and `chmod 0600`. Restrict the user to SSL and require a verified client cert in `pg_hba.conf`:
```ini
hostssl    giteadb    gitea    192.0.2.10/32    scram-sha-256    clientcert=verify-full
```
(`clientcert=1` is the form for PostgreSQL 11 and earlier.) On the Gitea host, put `postgresql.crt`, `postgresql.key` and `root.crt` in `~/.postgresql/` of the account running Gitea. These filenames are hardcoded by PostgreSQL and cannot be changed. Test with `psql "postgres://gitea@example.db/giteadb?sslmode=verify-full"`.

## MySQL/MariaDB (one-way TLS only)
Gitea currently supports only one-way TLS (the client verifies the server; no client cert check, see upstream issue 10828). In `my.cnf` under `[mysqld]` set `ssl-ca`, `ssl-cert`, `ssl-key` and `tls-version = TLSv1.2,TLSv1.3`; certs owned by `mysql`, mode 0600; restart. Recreate the DB user against the Gitea domain and force TLS:
```sql
CREATE USER 'gitea'@'example.gitea' IDENTIFIED BY '<password>' REQUIRE SSL;
GRANT ALL PRIVILEGES ON giteadb.* TO 'gitea'@'example.gitea';
FLUSH PRIVILEGES;
```
The CA chain must be in the system certificate store on both servers. Test with `mysql -u gitea -h example.db -p --ssl`.

## Gotcha
The documented client-side command for fixing key permissions reads `chown 0600`; the intent is `chmod 0600`.

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page database-preparation.md (raw markdown, gitea/docs main branch), including the `chown 0600` wording in the source. Nothing removed.
Method: documentation only; no commands were run.
