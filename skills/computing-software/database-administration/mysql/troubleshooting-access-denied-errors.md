---
id: computing-software.database-administration.mysql.troubleshooting-access-denied-errors
name: troubleshooting-access-denied-errors
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-security, mysql-accounts, access-denied-1045, account-host-matching, troubleshooting, authentication]
level: practitioner
status: docs-checked
description: "Resolve MySQL 'Access denied for user' (1045, 1044, 1142): account host matching, anonymous users, auth plugin mismatch, TLS requirements and missing privileges."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/problems-connecting.html
  - https://dev.mysql.com/doc/refman/8.4/en/connection-access.html
  - https://dev.mysql.com/doc/refman/8.4/en/account-names.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting "Access denied"

## Which error
| Error | Stage | Meaning |
|---|---|---|
| `1045 Access denied for user 'app'@'10.1.2.3' (using password: YES)` | connect | no account matches user+host with that password |
| other access-denied errors | connect or statement | logged in but missing a database, table or global privilege: check `SHOW GRANTS`; look the code up in the server error reference |

## Account matching (the common 1045 cause)
An account is `'user'@'host'`. The server sorts accounts by **most specific host first**
and picks the first match for the client's host, then checks the password for that one only.
```sql
SELECT user, host, plugin, account_locked FROM mysql.user
WHERE user IN ('app', '') ORDER BY user, host;
SELECT USER(), CURRENT_USER();      -- USER() = what you asked for, CURRENT_USER() = account matched
```
Classic traps:
- An **anonymous user** `''@'localhost'` (old installs) matches before `'app'@'%'` for local
  connections. Drop anonymous users (`mysql_secure_installation` does).
- `'app'@'localhost'` (socket) and `'app'@'127.0.0.1'` (TCP) are different accounts.
- Client IP seen by the server is the proxy's or NAT's address; check
  `SELECT host FROM information_schema.processlist` for a working session.
- `skip_name_resolve = ON` means host names in accounts never match; use IPs/CIDR (`'app'@'10.1.%'`
  or `'app'@'10.1.0.0/255.255.0.0'`).

## Plugin and password state
- Account `plugin` = `mysql_native_password` on 8.4 where it is disabled by default ->
  `ALTER USER 'app'@'%' IDENTIFIED WITH caching_sha2_password BY '...';`
- `caching_sha2_password` over non-TLS needs the server RSA key: client option
  `--get-server-public-key` (or `allowPublicKeyRetrieval=true` in JDBC), or use TLS.
- `account_locked = Y`, an expired password, or a temporary lock from FAILED_LOGIN_ATTEMPTS / PASSWORD_LOCK_TIME.

## Privileges
```sql
SHOW GRANTS FOR 'app'@'%';
SHOW GRANTS FOR 'app'@'%' USING 'app_rw';   -- include role privileges
SELECT CURRENT_ROLE();                       -- roles active? need SET DEFAULT ROLE or activate_all_roles_on_login
```
Granted roles are **inactive** at login unless default roles are set:
`SET DEFAULT ROLE ALL TO 'app'@'%';`

## Log detail
The general log shows connect attempts; enable it only briefly, it is heavy.

## Checked

2026-11-01. Confirmed against the MySQL 8.4 manual pages connection-access (host sorting, anonymous match), problems-connecting, native-pluggable-authentication (disabled by default in 8.4), caching-sha2-pluggable-authentication (`--get-server-public-key`), roles (activate_all_roles_on_login, SET DEFAULT ROLE), password-management. Removed unconfirmed error numbers and messages other than 1045, and the log_error_verbosity claim.

Method: documentation only; no commands were run.

## Verify
`mysql -h <host> -u app -p -e 'SELECT CURRENT_USER(), CURRENT_ROLE()'` from the client host
returns the intended account and roles.
