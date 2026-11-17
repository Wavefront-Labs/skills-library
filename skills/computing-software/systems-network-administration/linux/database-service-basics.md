---
id: computing-software.systems-network-administration.linux.database-service-basics
name: database-service-basics
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mariadb, mysql, postgresql, postgresql-service, database-service, postgresql-setup, initdb, pg-hba, mysql-secure-installation, bind-address, listen-addresses, mysqldump, pg-dump, pg-basebackup, data-directory, systemd-database, selinux-database, lfcs, sysadmin, grant, create-user, pg-upgrade, innodb-buffer-pool, shared-buffers]
level: practitioner
status: gated
description: "Run MariaDB/MySQL and PostgreSQL as system services: install, initialise, secure, allow remote connections, move the data directory, basic users and backups, debug failed starts."
sources:
  - https://mariadb.com/kb/en/getting-installing-and-upgrading-mariadb/
  - https://www.postgresql.org/docs/current/runtime.html
  - https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_using_database_servers/index
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Database service basics — MariaDB and PostgreSQL as well-behaved system services

**Goal:** the sysadmin side of a database: it starts at boot, listens where intended,
stores data on the right disk, is backed up, and its logs explain failures. (Query
tuning and replication live in the database-administration skills.)

## 1. MariaDB / MySQL
```bash
dnf install mariadb-server            # apt install mariadb-server (Debian starts it automatically)
systemctl enable --now mariadb
mariadb-secure-installation           # root password/unix_socket auth, drop test DB, remove anonymous users
mariadb -e "CREATE DATABASE app; CREATE USER 'app'@'10.0.%' IDENTIFIED BY '<PASSWORD>'; GRANT ALL ON app.* TO 'app'@'10.0.%'; FLUSH PRIVILEGES;"
```
Config: `/etc/my.cnf.d/server.cnf` (RHEL) or `/etc/mysql/mariadb.conf.d/50-server.cnf` (Debian): (gated: unconfirmed, source is paywalled or blocked)
```ini
[mysqld]
bind-address = 10.0.0.15      # the internal IP rather than 0.0.0.0; check your distribution's default
datadir = /var/lib/mysql
innodb_buffer_pool_size = 2G  # size to the workload and available RAM
log_error = /var/log/mariadb/mariadb.log
```
```bash
firewall-cmd --add-service=mysql --permanent && firewall-cmd --reload   # 3306/tcp
mariadb-dump --all-databases --single-transaction --routines --events > /backup/all-$(date +%F).sql
```
- Local root uses `unix_socket` auth on modern MariaDB: `sudo mariadb` works, `mariadb -u root -p` from
  another account doesn't — intended.
- Host part of the user matters: `'app'@'localhost'` ≠ `'app'@'%'`.

## 2. PostgreSQL
```bash
dnf install postgresql-server && postgresql-setup --initdb        # RHEL: data in /var/lib/pgsql/data
apt install postgresql                                              # Debian: cluster auto-created, /etc/postgresql/<ver>/main/, pg_lsclusters
systemctl enable --now postgresql
sudo -u postgres psql -c "CREATE ROLE app LOGIN PASSWORD '<PASSWORD>'; CREATE DATABASE app OWNER app;"
```
`postgresql.conf`:
```
listen_addresses = '10.0.0.15'          # default 'localhost'
port = 5432
shared_buffers = 2GB                     # ~25% RAM
log_line_prefix = '%m [%p] %u@%d '
log_min_duration_statement = 500         # log slow queries (ms)
```
`pg_hba.conf` (first matching line wins; order matters):
```
# TYPE  DATABASE  USER      ADDRESS        METHOD
local   all       postgres                 peer
local   all       all                      scram-sha-256
host    app       app       10.0.0.0/8     scram-sha-256
hostssl all       all       0.0.0.0/0      scram-sha-256     # only with ssl = on
```
```bash
systemctl reload postgresql     # pg_hba/most settings; listen_addresses/port/shared_buffers need restart
firewall-cmd --add-service=postgresql --permanent && firewall-cmd --reload
sudo -u postgres pg_dumpall > /backup/pg-all-$(date +%F).sql     # or pg_dump -Fc app > app.dump
sudo -u postgres pg_basebackup -D /backup/base -Ft -z -P         # physical backup
```
- `peer` auth = OS user must equal DB role (`sudo -u postgres psql`). "Peer authentication
  failed for user app" = you ran `psql -U app` from the wrong OS user; use `-h 127.0.0.1` to
  hit the `host` line instead.
- `password_encryption = scram-sha-256` (default ≥ 14); `md5` lines in pg_hba still work.
- Debian multi-version: `pg_upgradecluster 15 main` for major upgrades; RHEL uses
  `postgresql-upgrade` or the `postgresql:16` module stream.

## 3. Moving the data directory (both engines)
```bash
systemctl stop postgresql
rsync -av /var/lib/pgsql/data/ /srv/pgdata/           # keep trailing slashes; preserves ownership
# PostgreSQL: systemctl edit postgresql → [Service] Environment=PGDATA=/srv/pgdata  (RHEL) / data_directory in postgresql.conf (Debian)
# MariaDB: datadir=/srv/mysql in server.cnf
semanage fcontext -a -e /var/lib/pgsql /srv/pgdata && restorecon -Rv /srv/pgdata   # SELinux equivalence; mysqld_db_t for MariaDB
systemctl start postgresql
```
Mount the data disk with `noatime`; XFS or ext4; keep WAL/binlogs on the same fsync-safe
storage. Disable transparent hugepages for databases (`tuned-adm profile` or kernel cmdline).

## 4. When it won't start
```bash
journalctl -u mariadb -b; journalctl -u postgresql -b
tail -50 /var/log/mariadb/mariadb.log; tail -50 /var/lib/pgsql/data/log/postgresql-*.log
ls -ld /var/lib/mysql /var/lib/pgsql/data     # ownership mysql:mysql / postgres:postgres, mode 700 (PG refuses anything else)
df -h /var/lib                                # full disk = InnoDB/WAL errors
ausearch -m avc -ts recent                    # SELinux after moving datadir or changing port (semanage port -a -t postgresql_port_t -p tcp 5433)
```
Common: "Address already in use" (another instance / port), "could not open lock file
/run/postgresql" (tmpfiles dir missing → `systemd-tmpfiles --create`), InnoDB "Unable to
lock ./ibdata1" (stale mysqld), PG "data directory has wrong ownership".

## Verify
- [ ] Service survives a reboot (`systemctl is-enabled`, `is-active`), listens on the intended address only (`ss -tlnp | grep -E '3306|5432'`).
- [ ] A remote client on the allowed subnet connects; one outside it is refused by pg_hba/firewall.
- [ ] A dump restores into a scratch database (`mariadb app_test < dump.sql` / `pg_restore -d app_test app.dump`) and a timer runs the backup nightly.

## Checked

2026-11-02

- Confirmed: PostgreSQL runtime and pg_hba.conf pages (official docs), the MariaDB install page and the RHEL 9 database-servers guide index were fetched.
- Removed or gated: The fetched pages are overviews that do not list the specific MariaDB/PostgreSQL option names, mysqldump flags or firewall-cmd flags used here; those are left as gated, to be confirmed in the current man pages and vendor reference.

Method: documentation only; no commands were run.
