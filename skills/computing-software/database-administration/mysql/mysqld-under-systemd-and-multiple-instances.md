---
id: computing-software.database-administration.mysql.mysqld-under-systemd-and-multiple-instances
name: mysqld-under-systemd-and-multiple-instances
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqld-systemd, mysqld-multi, systemd-unit-mysql, multiple-instances, limitnofile, mysql-service]
level: practitioner
status: docs-checked
description: "Run MySQL under systemd: unit overrides for LimitNOFILE and TZ, mysqld@ template instances on one host (replacing mysqld_multi), and platform caveats."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/using-systemd.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqld-multi.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running mysqld under systemd and multiple instances

On RPM/DEB installs from the MySQL repositories, `mysqld_safe` is not used; systemd starts mysqld directly (`mysqld.service` on RHEL, `mysql.service` on Debian/Ubuntu).

## Overrides (never edit the packaged unit)
```bash
systemctl edit mysqld
```
```ini
[Service]
LimitNOFILE=65535          # open-files limit for mysqld (value is an example)
Environment="TZ=UTC"       # time zone for the server process
```
```bash
systemctl daemon-reload && systemctl restart mysqld
systemctl show mysqld -p LimitNOFILE
```
Use `systemctl edit mysql` on Debian platforms. Use systemd settings (not `[mysqld_safe]` options) for what mysqld_safe used to do; to pass server options through the environment use `systemctl set-environment MYSQLD_OPTS="..."`. On systemd platforms an empty data directory is initialized at startup; set `NO_INIT=true` in `/etc/sysconfig/mysql` to stop that (for example when a remote data mount may be missing).

## Logs and status
```bash
systemctl status mysqld
```
The MySQL error log (`log-error` option) remains the main log.

## Multiple instances on one host
The template unit (`mysqld@.service` on RPM platforms, `mysql@.service` on Debian platforms) starts mysqld with `--defaults-group-suffix=@<name>`, so the `[server]`, `[mysqld]` and `[mysqld@<name>]` groups are read. `@` is the only delimiter systemd supports:
```ini
# /etc/my.cnf
[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysqld-replica01.log
server-id=101
```
```bash
systemctl start mysqld@replica01
systemctl enable mysqld@replica01
systemctl status 'mysqld@replica*'
mysql -S /var/lib/mysql-replica01/mysql.sock -u root -p
```
Each instance needs its own datadir, socket, port, log paths and server-id.

`mysqld_multi` (groups `[mysqldN]`, started by group number) is the approach for non-systemd hosts; on systemd platforms it is not installed and template instances replace it.

## Gotchas
- Debian platforms: AppArmor blocks `/var/lib/mysql-replica*` until `/etc/apparmor.d/usr.sbin.mysqld` is customized or disabled.
- Debian platforms: package removal or upgrade cannot handle `mysqld@` instances; stop the extra instances first.
- Budget memory (buffer pools) across all instances on the host.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual page Managing MySQL Server with systemd (unit names, systemctl edit override, LimitNOFILE, TZ, MYSQLD_OPTS, NO_INIT, multiple instances, defaults-group-suffix, AppArmor and package notes) and the mysqld_multi page. Removed: LimitMEMLOCK, Timeout*, Nice, Restart=on-abort, journalctl, SELinux commands, manual --initialize step, 70% figure (not on those pages).
Method: documentation only; no commands were run.

