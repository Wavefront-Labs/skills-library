---
id: computing-software.database-administration.mysql.password-policy-and-validate-password
name: password-policy-and-validate-password
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-security, mysql-accounts, validate-password, password-expiration, password-history, failed-login-attempts, dual-password, password-rotation]
level: practitioner
status: verified
description: "Enforce MySQL password policy with the validate_password component, expiry, reuse history, lockout after failed logins, and dual passwords for zero-downtime rotation."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/validate-password.html
  - https://dev.mysql.com/doc/refman/8.4/en/password-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password policy in MySQL

**Goal:** weak passwords are rejected, human passwords rotate, brute force is
throttled, and service passwords rotate without an outage.

## Strength: validate_password component
```sql
INSTALL COMPONENT 'file://component_validate_password';
SET PERSIST validate_password.policy = STRONG;     -- LOW | MEDIUM | STRONG (dictionary file)
SET PERSIST validate_password.length = 14;
SHOW VARIABLES LIKE 'validate_password%';
SELECT VALIDATE_PASSWORD_STRENGTH('Tr0ub4dor&3');   -- 0-100
```
The score depends on the active settings: on 9.7.4, with the defaults (MEDIUM, length 8) that string scores 100, but with STRONG and length 14 it scores 25 (too short); `'abc'` scores 0. A legacy `validate_password` plugin (`INSTALL PLUGIN validate_password SONAME 'validate_password.dll'` on Windows) still installs on 9.7.4, but use the component, which is what the 8.4 manual documents.

## Expiry, reuse and lockout
```sql
SET PERSIST default_password_lifetime = 180;               -- days, global default for humans
ALTER USER 'svc_api'@'10.0.%' PASSWORD EXPIRE NEVER;        -- services rotate via secrets manager
SET PERSIST password_history = 5;  SET PERSIST password_reuse_interval = 365;
ALTER USER 'alice'@'%' FAILED_LOGIN_ATTEMPTS 5 PASSWORD_LOCK_TIME 1;   -- days; UNBOUNDED for manual unlock
ALTER USER 'alice'@'%' PASSWORD REQUIRE CURRENT;           -- must supply old password to change
```
Expired accounts can log in but only run `ALTER USER ... IDENTIFIED BY`
(sandbox mode); other statements fail with error 1820. The non-interactive `mysql -e` refuses to connect to an expired account unless you pass `--connect-expired-password`.
The password in force counts toward `password_history`: re-setting an expired account to its current password fails with error 3638 "contradict the password history policy". An account that inherits the global lifetime has `password_lifetime = NULL` in `mysql.user`.

## Rotation without downtime: dual passwords (8.0.14+)
```sql
ALTER USER 'svc_api'@'10.0.%' IDENTIFIED BY '<new>' RETAIN CURRENT PASSWORD;
-- roll new password out to all app instances; both work meanwhile
ALTER USER 'svc_api'@'10.0.%' DISCARD OLD PASSWORD;
```
Both passwords logged in until `DISCARD OLD PASSWORD`, after which the old one failed with error 1045 (run on 9.7.4). The old password is kept in `User_attributes` under `additional_password`. Requires `APPLICATION_PASSWORD_ADMIN` for your own account; `CREATE USER` covers all accounts (docs).

## Gotchas
- Policy applies when passwords are set; existing weak ones stay until changed.
- Setting STRONG breaks automation that creates users with generated short
  passwords; update generators first.
- Lockout counters are in memory: reset on restart or `FLUSH PRIVILEGES`.
- MariaDB has its own password-validation plugins and settings; check its docs (not run here).

## Verify
```sql
SELECT user, host, password_lifetime, password_last_changed, account_locked,
       JSON_EXTRACT(user_attributes, '$.Password_locking') FROM mysql.user;
```
Attempt `CREATE USER t IDENTIFIED BY 'abc';`: fails with error 1819.
