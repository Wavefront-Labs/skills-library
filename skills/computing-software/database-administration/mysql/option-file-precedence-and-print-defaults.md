---
id: computing-software.database-administration.mysql.option-file-precedence-and-print-defaults
name: option-file-precedence-and-print-defaults
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, my-cnf, option-file-precedence, print-defaults, defaults-file, includedir, mysqld-config, my-print-defaults]
level: practitioner
status: verified
description: "Work out which my.cnf settings mysqld actually reads: option file search order, groups, !includedir, --defaults-file, and checking with --print-defaults."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/option-files.html
  - https://dev.mysql.com/doc/refman/8.4/en/option-file-options.html
  - https://dev.mysql.com/doc/refman/8.4/en/my-print-defaults.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option file precedence and --print-defaults

**Goal:** stop editing a my.cnf that mysqld never reads.

## Search order (Unix), later files win
1. `/etc/my.cnf`
2. `/etc/mysql/my.cnf`
3. `SYSCONFDIR/my.cnf`
4. `$MYSQL_HOME/my.cnf` (server only)
5. file named by `--defaults-extra-file`
6. `~/.my.cnf` (client tools; also mysqld when run as that user)
7. `~/.mylogin.cnf` (client only, obfuscated, from `mysql_config_editor`)

Windows: `mysqld --verbose --help` on 9.7.4 listed, in order, `%WINDIR%\my.ini`, `%WINDIR%\my.cnf`, `<SYSTEM_DRIVE>\my.ini`, `<SYSTEM_DRIVE>\my.cnf`, `<BASEDIR>\my.ini`, `<BASEDIR>\my.cnf` (the Windows folder and the system drive root, each with `.ini` and `.cnf`), then `--defaults-extra-file`. Command-line options override all files; within one file the last occurrence of an option wins (a file with `max_connections=111` then `max_connections=222` printed both and the server value was 222).

Distro layouts add `!includedir /etc/mysql/conf.d/` and `/etc/mysql/mysql.conf.d/`: the manual says MySQL makes no guarantee about the order in which files in an `!includedir` directory are read, so do not rely on a `zz-local.cnf` beating `mysqld.cnf`: put overrides in one file, or check the effective value with `variables_info`.

## Groups
`[mysqld]` server; `[mysqld-9.7]` only that series (the server prints the groups it reads: `mysql_cluster mysqld server mysqld-9.7` on 9.7.4, and a `[mysqld-8.4]` section in the test file was ignored while `[mysqld-9.7]` applied); `[client]` all clients; `[mysql]`, `[mysqldump]` per tool; `[mysqld_safe]`. MariaDB reads its own group names (`[mariadb]`, `[server]`, `[mariadbd]`; see its docs, not run here).

## Overrides that ignore the chain
- `--defaults-file=/path` (must be FIRST argument): read only this file. Checked: with `--port=1` placed before `--defaults-file=...`, the server started as if the file were absent (it ignored the file and began a default start-up).
- `--no-defaults`: read no option files (the manual notes `.mylogin.cnf` is still read by programs started with it).
- systemd units sometimes pass `--defaults-file`; check `systemctl cat mysqld`.

## Show what will be used
```bash
mysqld --verbose --help | grep -A1 'Default options'     # file list in order
mysqld --print-defaults                                  # effective args from files, then exits (printed "... would have been started with the following arguments: ..." on 9.7.4)
my_print_defaults mysqld                                 # same, group-based, one option per line
my_print_defaults --defaults-file=/etc/my.cnf client mysql
```
Running server: `SELECT VARIABLE_NAME, VARIABLE_SOURCE, VARIABLE_PATH FROM performance_schema.variables_info WHERE VARIABLE_NAME = 'innodb_buffer_pool_size';` shows `GLOBAL`, `EXPLICIT` (file at VARIABLE_PATH), `PERSISTED`, `DYNAMIC`, `COMMAND_LINE`, `COMPILED`.

## Gotchas
- On Unix, MySQL ignores world-writable option files (manual: "intentional as a security measure"; not testable on this Windows host).
- Options can use `-` or `_` (`--max-connections` and `max_connections` are the same: the server printed `max-connections 222`); a `loose-` prefix is how the manual says an unknown option is tolerated (written `loose-opt_name` in a file; `my_print_defaults` echoed `--loose-nonexistent_option=1`; the actual start-up behaviour was not tested).
- `mysqld-auto.cnf` (SET PERSIST) is read last and beats every file.

## Verify
After a change and restart, `variables_info.VARIABLE_PATH` points at the file you edited.
