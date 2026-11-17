---
id: computing-software.database-administration.mysql.log-rotation-flush-logs-logrotate
name: log-rotation-flush-logs-logrotate
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, flush-logs, mysql-logrotate, log-rotation, error-log, slow-query-log, general-log, binary-log]
level: practitioner
status: draft
description: "Rotate MySQL error, slow and general logs safely with logrotate and FLUSH LOGS, and know why binary logs are never rotated that way."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/log-file-maintenance.html
  - https://dev.mysql.com/doc/refman/8.4/en/flush.html
  - https://man7.org/linux/man-pages/man8/logrotate.8.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Server log maintenance with FLUSH LOGS and logrotate

MySQL keeps log files open; renaming a file does not make mysqld switch. After moving it, tell the server to reopen.

## Reopen commands
```sql
FLUSH ERROR LOGS;     -- reopen error log
FLUSH SLOW LOGS;      -- reopen slow query log
FLUSH GENERAL LOGS;   -- reopen general log
FLUSH BINARY LOGS;    -- close current binlog, start the next numbered file
FLUSH LOGS;           -- all of the above (also relay logs)
```
`mysqladmin flush-logs` = `FLUSH LOGS`. Needs the `RELOAD` privilege; a dedicated account is enough:
```sql
CREATE USER 'logrotate'@'localhost' IDENTIFIED BY '<PASSWORD>';
GRANT RELOAD ON *.* TO 'logrotate'@'localhost';
```
Store its credentials in `/root/.my.cnf` or a login path (`mysql_config_editor set --login-path=logrotate ...`).

## logrotate config
```
/var/log/mysql/error.log /var/log/mysql/slow.log {
    daily
    rotate 14
    missingok
    notifempty
    compress
    delaycompress
    create 640 mysql mysql
    sharedscripts
    postrotate
        if test -x /usr/bin/mysqladmin && /usr/bin/mysqladmin --login-path=logrotate ping >/dev/null 2>&1; then
            /usr/bin/mysqladmin --login-path=logrotate flush-error-log flush-slow-log
        fi
    endscript
}
```
Use the specific flush (`flush-error-log`, `flush-slow-log`, `flush-general-log`) rather than `flush-logs`, which also switches the binary log on every rotation and produces many small binlogs. `copytruncate` works without a flush but can lose lines written during the copy.

Test: `logrotate -d /etc/logrotate.d/mysql` (dry run), then `logrotate -f` and check mysqld writes to the new file (`ls -l`, file size grows).

## Binary logs are different
Never rotate or delete binlogs with logrotate or `rm`: the server tracks them in the index file and replicas/backups depend on them. Use `binlog_expire_logs_seconds` and `PURGE BINARY LOGS`.

## Gotchas
- With `log_error = stderr`/journald (some container setups) there is no file to rotate; journald handles retention.
- If the error log is deleted without a flush, mysqld keeps writing to the deleted inode: disk space is not freed until the flush.
