---
id: computing-software.database-administration.mysql.post-install-hardening
name: post-install-hardening
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-secure-installation, secure-file-priv, local-infile, hardening, skip-name-resolve, mysql-security]
level: practitioner
status: docs-checked
description: "Harden a fresh MySQL server: mysql_secure_installation, secure_file_priv, local_infile off, bind-address, no anonymous or remote root accounts."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/mysql-secure-installation.html
  - https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_secure_file_priv
  - https://dev.mysql.com/doc/refman/8.4/en/load-data-local-security.html
  - https://dev.mysql.com/doc/refman/8.4/en/security-guidelines.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-install hardening

## 1. mysql_secure_installation
```bash
mysql_secure_installation
```
Interactive: sets the root password, optionally enables password validation, can remove anonymous users, disallow remote root login and remove the `test` database. Equivalent SQL for automation:
```sql
DROP USER IF EXISTS ''@'localhost', ''@'%';
DELETE FROM mysql.user WHERE user = 'root' AND host NOT IN ('localhost','127.0.0.1','::1');   -- prefer DROP USER per row
DROP DATABASE IF EXISTS test;
FLUSH PRIVILEGES;
```

## 2. File access
```ini
[mysqld]
secure_file_priv = /var/lib/mysql-files      # only this dir for LOAD DATA INFILE / SELECT INTO OUTFILE; '' = anywhere (bad), NULL = disabled
local_infile = OFF                            # LOAD DATA LOCAL lets a malicious server read client files and vice versa
```
`secure_file_priv` is read-only at runtime (restart). Check: `SELECT @@secure_file_priv, @@local_infile;`. Also keep the `FILE` privilege away from application accounts.

## 3. Network
```ini
bind_address = <SERVER_IP>      # a specific interface unless all interfaces are needed
skip_name_resolve = ON          # no DNS on connect; accounts must use IPs/CIDR (not hostnames)
mysqlx = OFF                    # if X Protocol (33060) unused
require_secure_transport = ON   # TLS only for TCP connections
```
Firewall 3306 to app subnets only.

## 4. Accounts and privileges
- No application account with `ALL ON *.*`, `SUPER`, `FILE`, `PROCESS`, `SHUTDOWN`.
- Separate accounts per app/service, restricted to the host or subnet they connect from.
- `default_password_lifetime` / `password_history` per policy; `caching_sha2_password` as default auth.

## 5. Filesystem
- Keep the data directory and option files readable only by the OS account that runs mysqld, and run mysqld as a dedicated unprivileged account, never root.

## Verify checklist
```sql
SELECT user, host, plugin, account_locked FROM mysql.user ORDER BY user;
SHOW GLOBAL VARIABLES WHERE Variable_name IN ('secure_file_priv','local_infile','bind_address','skip_name_resolve','require_secure_transport');
```
The vendor security guidelines page has more checks.

## Checked

2026-11-01. Confirmed against the MySQL 8.4 manual pages mysql-secure-installation, server-system-variables (secure_file_priv empty/NULL meanings, local_infile, default_password_lifetime, password_history), load-data-local-security, security-guidelines. Removed unconfirmed claims (auth_socket on Debian, datadir mode, world-writable option file behaviour, CIS reference, example addresses).

Method: documentation only; no commands were run.

## Gotchas
- `skip_name_resolve` turned on later locks out accounts defined with hostnames; check `mysql.user` hosts first.
- Some client tools need `local_infile` on both sides for bulk loads; enable per session for the ETL account only (client option `--local-infile=1` plus the server `local_infile` variable).
