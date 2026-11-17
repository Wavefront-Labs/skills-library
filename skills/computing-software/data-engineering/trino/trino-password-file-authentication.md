---
id: computing-software.data-engineering.trino.trino-password-file-authentication
name: trino-password-file-authentication
category: computing-software
field: data-engineering
product: trino
tags: [password-file, password-authenticator, bcrypt, htpasswd, http-server-authentication-type]
level: practitioner
status: docs-checked
description: "Set up Trino password file authentication with bcrypt or PBKDF2 hashes, htpasswd cost 10, refresh period and verification via Web UI and CLI."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/password-file.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino password file authentication

Password file authentication gives HTTPS clients (CLI, JDBC, ODBC) username and password checks against a file. It is similar to LDAP setup and requires both TLS and the configured shared secret.

In `etc/config.properties` set `http-server.authentication.type=PASSWORD`. On the coordinator create `etc/password-authenticator.properties`:

```text
password-authenticator.name=file
file.password-file=/path/to/password.db
```

Options: `file.refresh-period` (default `5s`), `file.auth-token-cache.max-size` (default `1000`).

File format: one `username:hash` per line. Hashes must be bcrypt or PBKDF2. bcrypt starts with `$2y$` and needs a minimum cost of `8`. PBKDF2 is `iterations:hex-salt:hex-hash`, for example `test:1000:5b42...:f38d...`.

Create with Apache `htpasswd`, which must be given an explicit cost because Trino enforces a higher minimum than the tool's default:

```text
touch password.db
htpasswd -B -C 10 password.db test
```

Verify: browse to the Web UI over HTTPS (for example `https://trino.example.com:8443`), log in, and confirm a wrong password fails; the username shows at the top right on success. Then use the CLI:

```text
./trino --server https://trino.example.com:8443 --user test --password
```

and run `SELECT 'rocks' AS trino;`.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
