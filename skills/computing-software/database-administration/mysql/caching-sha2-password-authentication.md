---
id: computing-software.database-administration.mysql.caching-sha2-password-authentication
name: caching-sha2-password-authentication
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-security, mysql-accounts, caching-sha2-password, mysql-native-password, authentication-plugin, public-key-retrieval, connector-compatibility, mysql-8-4]
level: practitioner
status: verified
description: "Handle MySQL 8 caching_sha2_password: migrate off mysql_native_password (disabled in 8.4), fix 'public key retrieval' errors and old connectors."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/caching-sha2-pluggable-authentication.html
  - https://dev.mysql.com/doc/refman/8.4/en/native-pluggable-authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# caching_sha2_password

**Goal:** all accounts use caching_sha2_password and every client connects,
before an 8.4/9.x upgrade drops the old plugin.

## Background
- 8.0 default plugin: `caching_sha2_password` (SHA-256, with a server-side cache
  of successful logins).
- `mysql_native_password` (SHA-1) is deprecated since 8.0.34, **disabled by default in 8.4**
  (`mysql_native_password=ON` to load it) and removed in 9.0.0 (docs). On 9.7.4 `CREATE USER ... IDENTIFIED WITH mysql_native_password` fails with `ERROR 1524 Plugin 'mysql_native_password' is not loaded` and the plugin is absent from `information_schema.plugins`; there is no way to switch it back on, so on 9.x every account must already be migrated.

## Find old accounts
```sql
SELECT user, host, plugin FROM mysql.user WHERE plugin = 'mysql_native_password';
```
Migrate each (needs the password; hashes are not convertible):
```sql
ALTER USER 'app'@'10.0.%' IDENTIFIED WITH caching_sha2_password BY '<password>';
```

## The first-login rule
On the first login after a restart or `FLUSH PRIVILEGES`, the cache is empty and
the password must be exchanged securely: either over **TLS** or with RSA key
exchange. On an unencrypted connection without RSA, the `mysql` client fails with
`ERROR 2061 (HY000): Authentication plugin 'caching_sha2_password' reported error: Authentication requires secure connection.`
(reproduced on 9.7.4 with `--ssl-mode=DISABLED` after `FLUSH PRIVILEGES`). Other drivers word it differently.
Fixes, best first: use TLS (`--ssl-mode=REQUIRED` or `VERIFY_IDENTITY`); or give the
client the server public key (`--server-public-key-path=<file>`, a copy of the file named by
`caching_sha2_password_public_key_path`, `public_key.pem` in the data dir by default, auto-generated); last resort
`--get-server-public-key` (MITM risk; JDBC equivalent `allowPublicKeyRetrieval=true`, not run here). All three worked on 9.7.4. Once one login has succeeded the cache is warm and
unencrypted logins work without any of them; the cache empties on restart or `FLUSH PRIVILEGES`. Symptom pattern: works after someone else logged in,
fails after restart.

## Client compatibility
Older drivers and proxies may not support the plugin; check each driver's release notes
for `caching_sha2_password` support before migrating (specific minimum versions were not checked here).

## Gotchas
- `default_authentication_plugin` was deprecated in 8.0.27 and removed in 8.4.0 (8.4.0 release notes); on 9.7.4 `SHOW VARIABLES LIKE 'authentication_policy'` is `*,,` by default and
  `SET GLOBAL authentication_policy='caching_sha2_password,,'` is accepted.
- Replication users need the same treatment: `GET_SOURCE_PUBLIC_KEY=1` in
  CHANGE REPLICATION SOURCE TO, or TLS (`SOURCE_SSL=1`).
- If a MySQL 8+ client talks to MariaDB, check MariaDB's own docs for its supported authentication plugins (not run here).

## Verify
The query above returns no rows; after a server restart, each application
reconnects successfully on its first attempt.
