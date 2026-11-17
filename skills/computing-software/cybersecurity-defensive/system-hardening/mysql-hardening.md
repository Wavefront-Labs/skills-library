---
id: computing-software.cybersecurity-defensive.system-hardening.mysql-hardening
name: mysql-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [mysql-hardening, mariadb, database-hardening, mysql-secure-installation, tls, least-privilege]
level: practitioner
status: draft
description: "Harden MySQL and MariaDB: secure installation, network binding, TLS required, account and privilege hygiene, local_infile and file privileges off, auditing and patching."
sources: ["https://dev.mysql.com/doc/refman/8.4/en/security-guidelines.html", "https://dev.mysql.com/doc/refman/8.4/en/mysql-secure-installation.html", "https://www.cisecurity.org/benchmark/oracle_mysql", "https://mariadb.com/kb/en/securing-mariadb/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MySQL / MariaDB hardening

## Install baseline
- `mysql_secure_installation` (MariaDB: `mariadb-secure-installation`): set root auth, remove anonymous users,
  disallow remote root, remove the `test` database.
- Run `mysqld` as the unprivileged `mysql` user; datadir owned by mysql with 0750; no other services on the host.

## Network
```ini
[mysqld]
bind-address = 10.0.30.5          # private interface only; 127.0.0.1 if app is local
skip-name-resolve = ON            # avoids DNS-based host matching surprises
require_secure_transport = ON     # reject non-TLS TCP connections
tls_version = TLSv1.2,TLSv1.3
local_infile = OFF
secure_file_priv = /var/lib/mysql-files   # or NULL to disable LOAD DATA/SELECT INTO OUTFILE
symbolic-links = 0                # older versions; removed in 8.0+
```
Firewall 3306 to app hosts only; never internet-exposed.

## Accounts and privileges
- One account per application, host-restricted: `CREATE USER 'app'@'10.0.20.%' IDENTIFIED BY '...' REQUIRE SSL;`
- Grant only needed privileges on the app schema: `GRANT SELECT, INSERT, UPDATE, DELETE ON shop.* TO 'app'@'10.0.20.%';`
  No `ALL PRIVILEGES`, no global grants.
- Remove `FILE`, `PROCESS`, `SUPER` (or the 8.0 dynamic privileges like `SYSTEM_VARIABLES_ADMIN`), `GRANT OPTION`
  from non-admin accounts; `FILE` allows reading server files.
- Review: `SELECT user, host FROM mysql.user;`, `SHOW GRANTS FOR 'app'@'10.0.20.%';`. No `%` hosts for
  privileged users; no empty passwords (`authentication_string = ''`).
- Authentication plugin `caching_sha2_password` (8.0 default); avoid `mysql_native_password` (deprecated,
  disabled by default in 8.4).
- Password policy: `validate_password` component; `password_history`, `password_reuse_interval`; failed login
  tracking (`FAILED_LOGIN_ATTEMPTS`, `PASSWORD_LOCK_TIME` in 8.0.19+).
- Roles (8.0+) for admin groups.

## Logging and auditing
- Error log enabled; general log off in production (logs statements incl. sensitive data).
- Audit: MySQL Enterprise Audit, Percona Audit Log plugin or MariaDB `server_audit` plugin for logins, DDL and
  privilege changes; ship to SIEM.

## Data protection
InnoDB data-at-rest encryption with keyring component/plugin (or disk encryption); encrypted backups;
`mysqldump` credentials in option files with 0600 permissions, not on command lines.

## Patching
Track MySQL Critical Patch Updates (quarterly, Oracle) / MariaDB releases; LTS lines (MySQL 8.4) for stability.

## Verify
`SHOW VARIABLES LIKE 'require_secure_transport'` is ON; a non-TLS connection is rejected; app account `SHOW GRANTS`
lists only schema-level DML; CIS MySQL benchmark scan passes.
