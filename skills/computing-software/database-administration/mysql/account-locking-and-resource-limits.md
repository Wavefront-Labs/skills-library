---
id: computing-software.database-administration.mysql.account-locking-and-resource-limits
name: account-locking-and-resource-limits
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, account-locking, max-user-connections, resource-limits, failed-login-attempts, password-lock-time, mysql-accounts]
level: practitioner
status: verified
description: "Lock and unlock MySQL accounts, auto-lock after failed logins, and cap per-account connections and query rates with MAX_USER_CONNECTIONS and friends."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/account-locking.html
  - https://dev.mysql.com/doc/refman/8.4/en/user-resources.html
  - https://dev.mysql.com/doc/refman/8.4/en/password-management.html#failed-login-tracking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Account locking and resource limits

## Manual locking
```sql
ALTER USER 'legacy_app'@'%' ACCOUNT LOCK;     -- existing sessions continue; new logins fail
ALTER USER 'legacy_app'@'%' ACCOUNT UNLOCK;
CREATE USER 'svc_definer'@'localhost' ACCOUNT LOCK;   -- definer-only account nobody can log in as
SELECT user, host, account_locked FROM mysql.user;
```
Login attempt error (correct password supplied): `ERROR 3118 (HY000): Access denied for user ... Account is locked.` and `Locked_connects` status increments. With a wrong password on a locked account you still get plain `ERROR 1045` (checked on 9.7.4). Kill existing sessions separately (`KILL <id>` from the processlist). The `mysql.*` system accounts (`mysql.sys`, `mysql.session`, `mysql.infoschema`) and every role created with `CREATE ROLE` show `account_locked = Y` by default.

## Automatic lock after failed logins (8.0.19+)
```sql
ALTER USER 'alice'@'%' FAILED_LOGIN_ATTEMPTS 5 PASSWORD_LOCK_TIME 1;        -- days; UNBOUNDED = until unlocked
ALTER USER 'alice'@'%' ACCOUNT UNLOCK;                                       -- resets the counter and lock
```
While blocked, a login (even with the right password) fails with `ERROR 3955 (HY000): ... Account is blocked for 1 day(s) (1 day(s) remaining) due to 3 consecutive failed logins.` and `account_locked` in `mysql.user` stays `N`: the temporary block is tracked in memory, and `User_attributes` only holds the settings, e.g. `{"Password_locking": {"failed_login_attempts": 3, "password_lock_time_days": 1}}`. Counters are in memory: global reset on server restart or `FLUSH PRIVILEGES`; per-account reset on a successful login or when the lock time passes (documented; the successful-login, `FLUSH PRIVILEGES` and server-restart resets were all run on 9.7.4: an account blocked after 2 failures could log in after a restart). Beware with service accounts: a misconfigured app retrying a wrong password locks the account for every instance.

## Resource limits
```sql
ALTER USER 'report'@'%' WITH MAX_USER_CONNECTIONS 10 MAX_QUERIES_PER_HOUR 50000 MAX_UPDATES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0;
```
- `MAX_USER_CONNECTIONS`: simultaneous connections for that account (0 = use global `max_user_connections`, 0 globally = unlimited). Error 1226 `has exceeded the 'max_user_connections' resource`.
- Hourly counters apply per account (user@host). Reset them for all accounts with `FLUSH USER_RESOURCES` (also reset by `FLUSH PRIVILEGES` / `mysqladmin reload`); for one account re-issue any of its limits with `ALTER USER`. Exceeding `MAX_QUERIES_PER_HOUR` gives `ERROR 1226 ... exceeded the 'max_questions' resource`; the 4th query with a limit of 3 failed and worked again after `FLUSH USER_RESOURCES`.
- Global `max_user_connections` caps every account without its own setting.

Use per-account limits to stop one batch job or misbehaving pool from eating `max_connections` and locking out everyone (the reserved extra connection for `CONNECTION_ADMIN` holders helps DBAs get in: with `max_connections=3` and 3 busy sessions, an ordinary user got `ERROR 1040 Too many connections` and a `CONNECTION_ADMIN` user connected).

## Verify
```sql
SELECT user, host, max_user_connections, max_questions, User_attributes FROM mysql.user WHERE user IN ('report','alice');
SHOW GLOBAL STATUS LIKE 'Locked_connects';
```
`User_attributes` JSON holds failed-login settings.

## Gotchas
- Limits are per `user@host` row: `'report'@'%'` and `'report'@'10.%'` are counted separately.
- Locking a definer account does not stop views/procedures defined by it from running. (checked with a `SQL SECURITY DEFINER` procedure owned by a locked account: another user could still `CALL` it. Also checked: a session already open when `ACCOUNT LOCK` was issued kept running, and the next login failed with error 3118.)
