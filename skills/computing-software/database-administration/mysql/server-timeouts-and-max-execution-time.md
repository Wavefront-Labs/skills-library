---
id: computing-software.database-administration.mysql.server-timeouts-and-max-execution-time
name: server-timeouts-and-max-execution-time
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqld-options, wait-timeout, max-execution-time, interactive-timeout, lock-wait-timeout, server-has-gone-away]
level: practitioner
status: verified
description: "Set MySQL timeouts deliberately (wait_timeout, interactive_timeout, max_execution_time, lock_wait_timeout, net timeouts) and diagnose 'MySQL server has gone away'."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_wait_timeout
  - https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_max_execution_time
  - https://dev.mysql.com/doc/refman/8.4/en/gone-away.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server timeouts and max_execution_time

## The settings
All nine defaults in this table were read from a fresh 9.7.4 server (`max_allowed_packet` is 67108864 bytes).

| Variable | Default | Effect |
|---|---|---|
| `wait_timeout` | 28800 s | idle non-interactive connection closed after this |
| `interactive_timeout` | 28800 s | same for clients using `CLIENT_INTERACTIVE` (mysql CLI); copied into session `wait_timeout` at connect |
| `max_execution_time` | 0 (off) | ms limit for **read-only SELECT** statements; not for DML/DDL |
| `lock_wait_timeout` | 31536000 s | metadata lock wait (DDL, LOCK TABLES, FLUSH) |
| `innodb_lock_wait_timeout` | 50 s | row lock wait; error 1205 |
| `net_read_timeout` / `net_write_timeout` | 30 / 60 s | waiting for data from / to the client mid-statement |
| `connect_timeout` | 10 s | handshake |

## Typical production values
```sql
SET PERSIST wait_timeout = 600;          -- idle app connections; must exceed pool idle timeout
SET PERSIST interactive_timeout = 3600;
SET PERSIST max_execution_time = 30000;  -- 30 s cap for SELECTs (or per session / per query)
SET PERSIST lock_wait_timeout = 60;      -- stop DDL waiting a year on a metadata lock
```
Per statement: `SELECT /*+ MAX_EXECUTION_TIME(5000) */ ...`. Per session for reporting
users: set in the app or with `init_connect` (not applied to `CONNECTION_ADMIN` users).
When `max_execution_time` fires: `ERROR 3024 (HY000): Query execution was interrupted, maximum statement execution time exceeded` (reproduced on 9.7.4 both with `SET SESSION max_execution_time=300` and with `/*+ MAX_EXECUTION_TIME(300) */` on a slow cross join).

## Connection pools must agree
Set the pool's max idle/lifetime **below** `wait_timeout` (HikariCP `maxLifetime` a few
seconds to minutes shorter), otherwise the pool hands out connections the server already
closed: `Communications link failure` / `MySQL server has gone away (2006)` / `Lost connection (2013)`.

## Diagnosing "server has gone away" (2006 / 2013)
1. Idle connection exceeded `wait_timeout` -> pool config. Reproduced: with `SET SESSION wait_timeout=1` and a 3 second pause, the next statement failed with `ERROR 2013 Lost connection to MySQL server during query` in the `mysql` client (other drivers report 2006 or their own message).
2. Packet larger than `max_allowed_packet` (default 64MB) -> raise on server **and** client.
3. Query killed (`KILL`, `max_execution_time`, OOM killer restarted mysqld) -> check error log, `Uptime`.
4. Network middlebox (NAT, load balancer) idle timeout shorter than `wait_timeout` (AWS NLB
   350 s) -> TCP keepalive or lower pool idle time.
```sql
SHOW GLOBAL STATUS LIKE 'Aborted_clients';   -- clients that went away without closing properly
SHOW GLOBAL STATUS LIKE 'Uptime';
```

## Gotchas
- Changing a global value only affects **new** sessions (checked: after `SET GLOBAL wait_timeout=77` the same session still read `@@session.wait_timeout = 28800`).
- `max_execution_time` does not apply to stored procedure SELECTs or to statements inside
  a stored program: a cross-join SELECT inside a procedure ran far past a 300 ms limit until it was killed, while the same SELECT outside the procedure failed with 3024 (the manual also limits it to read-only top-level SELECTs; the `MAX_EXECUTION_TIME` hint on an UPDATE gave warning 3125).
- A low `lock_wait_timeout` makes online DDL tools give up sooner; gh-ost/pt-osc set their own.

## Verify
`SELECT @@global.wait_timeout, @@session.wait_timeout;` from an app connection matches intent;
a deliberately slow SELECT is cut at the cap.
