---
id: computing-software.database-administration.mysql.connection-management-and-too-many-connections
name: connection-management-and-too-many-connections
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqld-options, too-many-connections, max-connections, thread-cache-size, admin-port, connection-management]
level: practitioner
status: docs-checked
description: "Size max_connections and thread_cache_size, get in when MySQL says 'Too many connections' (admin port, reserved slot), and find who is holding connections."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/connection-management.html
  - https://dev.mysql.com/doc/refman/8.4/en/too-many-connections.html
  - https://dev.mysql.com/doc/refman/8.4/en/administrative-connection-interface.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection management and "Too many connections"

## Error
`ERROR 1040 (HY000): Too many connections` - the server reached `max_connections`
(default 151). MySQL keeps **one extra** slot for a user with `CONNECTION_ADMIN` (or legacy
`SUPER`), so an admin can still log in, unless an app also connects with such a user.

## Getting in during an incident
- Admin interface, separate port (its own listener thread optional), not limited by `max_connections`:
  ```ini
  [mysqld]
  admin_address = 127.0.0.1
  admin_port = 33062
  ```
  `mysql -h 127.0.0.1 -P 33062 -u root -p` (requires `SERVICE_CONNECTION_ADMIN`). Set it up
  **before** you need it; it needs a restart.
- Otherwise use the reserved slot with a `CONNECTION_ADMIN` account; never give apps that privilege.

## Find who holds connections
```sql
SELECT user, substring_index(host, ':', 1) AS client, db, command, count(*) AS n,
       max(time) AS max_time
FROM information_schema.processlist GROUP BY 1,2,3,4 ORDER BY n DESC;
SHOW GLOBAL STATUS LIKE 'Threads_%';          -- Threads_connected, Threads_running, Threads_cached, Threads_created
SHOW GLOBAL STATUS LIKE 'Max_used_connections%';
SHOW GLOBAL STATUS LIKE 'Aborted_c%';         -- Aborted_clients / Aborted_connects
```
Many `Sleep` connections from one app = connection leak or oversized pool. Many running
= the database is slow and pools are piling on (fix the slow query, not the limit).
Kill a batch: generate `KILL <id>;` statements from the query above.

## Sizing
```sql
SET PERSIST max_connections = 1000;
SET PERSIST thread_cache_size = 100;     -- threads reused instead of created per connection
```
- Each connection costs memory (per-thread buffers: `sort_buffer_size`, `join_buffer_size`,
  `read_rnd_buffer_size`, plus `thread_stack`); the worst case is
  `max_connections x per-thread buffers` on top of the buffer pool.
- Raise `open_files_limit` / systemd `LimitNOFILE` with large connection counts.
- `Threads_created` growing fast relative to `Connections` means `thread_cache_size` too small.
- Thousands of mostly idle connections: use the thread pool plugin (Enterprise, Percona,
  MariaDB) or a proxy (ProxySQL, MySQL Router) instead of raising the limit indefinitely.

## Per-user limits
```sql
ALTER USER 'batch'@'%' WITH MAX_USER_CONNECTIONS 20;
SET PERSIST max_user_connections = 500;  -- global per-account default (0 = unlimited)
```

## Verify
`Max_used_connections` stays comfortably below `max_connections` at peak, `Threads_created`
grows slowly, and the admin port login works from the DB host.

## Checked

2026-10-31: confirmed max_connections default 151, the max_connections + 1 extra connection reserved for CONNECTION_ADMIN (or deprecated SUPER) accounts, the administrative interface (enabled by admin_address, admin_port default 33062, no limit on administrative connections, SERVICE_CONNECTION_ADMIN required, own listener thread optional) and max_user_connections default 0 on dev.mysql.com 8.4 pages (too-many-connections, administrative-connection-interface, server-system-variables). Removed the 8.0.14+ version note.
Method: documentation only; no commands were run.
