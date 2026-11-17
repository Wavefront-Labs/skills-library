---
id: computing-software.networking-hardware-and-wireless.powerdns.gmysql-backend
name: gmysql-backend
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, gmysql, mysql, mariadb, backend, innodb, replication]
level: practitioner
status: docs-checked
description: "Configure the PowerDNS gmysql backend: connection settings and defaults, InnoDB read-committed, timeouts, binlog format, foreign keys, and caveats on views and hostnames."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/generic-mysql.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gmysql backend

Connection settings (defaults in brackets):
- `gmysql-host` (IP) or `gmysql-socket` (UNIX socket path); the two are mutually exclusive.
- `gmysql-port` (3306), `gmysql-dbname` (`powerdns`), `gmysql-user` (`powerdns`), `gmysql-group` (`client`), `gmysql-password`.
- `gmysql-dnssec` (no): enable DNSSEC for this backend.
- `gmysql-innodb-read-committed` (yes): use READ-COMMITTED isolation.
- `gmysql-timeout` (10): seconds per read or write attempt; 0 disables.
- `gmysql-thread-cleanup`: calls `mysql_thread_end()` when a thread ends, to work around leaks in old client libraries (for example RHEL 7). Enable only if sure.
- `gmysql-ssl`: deprecated since 5.0.0 and a no-op. Put TLS options in `my.cnf` and select them with `gmysql-group`.

Schema: load `schema.mysql.sql` (the 4.7 schema); `zone2sql --gmysql` assumes it.

Notes:
- Replicating NATIVE domains needs `binlog_format` set to `MIXED` or `ROW`; otherwise you can see "impossible to write to binary log since BINLOG_FORMAT = STATEMENT".
- Optional InnoDB foreign keys: apply `enable-foreign-keys.mysql.sql`. Removing a domain from `domains` then deletes its records, keys and related data. They prevent use with MySQL group replication across servers.
- Secondary support needs a transactional engine such as InnoDB; otherwise a failed zone transfer can fail silently.
- SQL views are unsupported (linked to performance problems and leaks).
- Use an IP, not a hostname, for `gmysql-host`, to avoid needing the database to resolve the database's address.

## Checked

2026-11-04. Read backends/generic-mysql.rst in full and confirmed every setting and default, the 5.0.0 gmysql-ssl deprecation, thread-cleanup, binlog_format requirement and error text, foreign key and group replication warning, transactional engine warning and view warning. Nothing removed.

Method: documentation only; no commands were run.
