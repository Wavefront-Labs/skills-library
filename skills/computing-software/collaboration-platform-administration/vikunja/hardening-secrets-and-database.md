---
id: computing-software.collaboration-platform-administration.vikunja.hardening-secrets-and-database
name: hardening-secrets-and-database
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, secrets-handling, sslmode-verify-full, vikunja-dump-plaintext, dedicated-db-user, openssl-rand]
level: advanced
status: docs-checked
description: "Protect Vikunja secrets and its database: fixed service.secret, file-based secrets, dedicated DB user, verify-full or TLS connections and the vikunja dump caveat."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/security-hardening.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Secrets:
- Set `service.secret`; if empty, Vikunja generates a new one every start, ending all sessions and making multiple instances reject each other's tokens. Generate with `openssl rand -hex 32`.
- Load secrets from files, for example `VIKUNJA_DATABASE_PASSWORD_FILE=/run/secrets/db_password`. Candidates: `database.password`, `auth.ldap.bindpassword`, OIDC `clientsecret`, `mailer.password`, `redis.password`, `files.s3.secretkey`, `metrics.password`, `outgoingrequests.proxypassword`, `license.key`.
- Make the config file readable only by the Vikunja user.
- `vikunja dump` archives contain the config file and every `VIKUNJA_*` environment variable in plain text, plus the database and files. Encrypt and restrict them. Values loaded from files appear as paths only.

Database:
- Use a dedicated user with access only to Vikunja's database, never a superuser; it must be able to create and alter tables because migrations run at startup.
- PostgreSQL: `database.sslmode: verify-full` with `sslrootcert` (client cert in `sslcert`, `sslkey`).
- MySQL/MariaDB: `database.tls: true` verifies against the system CA store; avoid `skip-verify` and `preferred`.
- Do not expose the database port. With SQLite make the file readable only by the Vikunja user.

## Checked

2026-11-04. Confirmed against the Vikunja Security hardening page (setup/security-hardening): service.secret behaviour, openssl command, file-based secrets and candidate keys, vikunja dump contents, dedicated database user, sslmode and tls options, database port exposure and SQLite file permissions. Nothing removed.

Method: documentation only; no commands were run.
