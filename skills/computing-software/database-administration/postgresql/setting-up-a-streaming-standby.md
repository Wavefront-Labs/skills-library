---
id: computing-software.database-administration.postgresql.setting-up-a-streaming-standby
name: setting-up-a-streaming-standby
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, streaming-replication, hot-standby, primary-conninfo, standby-signal, pg-basebackup, replication-slots]
level: practitioner
status: verified
description: "Build a PostgreSQL streaming standby: replication role and pg_hba line, pg_basebackup -R with a slot, standby.signal, primary_conninfo, then verify it streams."
sources:
  - https://www.postgresql.org/docs/current/warm-standby.html
  - https://www.postgresql.org/docs/current/app-pgbasebackup.html
  - https://www.postgresql.org/docs/current/runtime-config-replication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up a streaming standby

## On the primary
```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '...';
SHOW wal_level;            -- must be replica or logical (default replica)
SHOW max_wal_senders;      -- default 10; one per standby + pg_basebackup runs
SHOW max_replication_slots;
```
pg_hba.conf (physical replication uses the special `replication` database keyword):
```
hostssl  replication  replicator  10.0.1.20/32  scram-sha-256
```
`SELECT pg_reload_conf();`

## On the standby host
Empty data directory owned by the service user, same major version and architecture. Run as that user:
```bash
pg_basebackup -h 10.0.1.10 -U replicator \
  -D <new-datadir> -X stream -c fast -P -R \
  -C -S standby1          # create and use physical slot "standby1"
```
`-R` writes `standby.signal` and appends to `postgresql.auto.conf`:
```
primary_conninfo = 'user=replicator password=... channel_binding=prefer host=10.0.1.10 port=5432 sslmode=prefer ...'   # libpq defaults are spelled out; no application_name
primary_slot_name = 'standby1'
```
Edit `primary_conninfo` to add `application_name=standby1` (used by
`synchronous_standby_names` and shown in `pg_stat_replication`) and `sslmode=verify-full`
where you have certificates. Store the password in the service user's libpq password file (`~/.pgpass`; `%APPDATA%\postgresql\pgpass.conf` on Windows) rather than in the
conninfo.

Settings that must be **>= primary** on a standby: `max_connections`, `max_worker_processes`,
`max_wal_senders`, `max_prepared_transactions`, `max_locks_per_transaction`.
`hot_standby = on` (default) allows read queries.

Start it with `pg_ctl -D <datadir> start` or your service manager.

## Slots: pros and cons
A slot guarantees the primary keeps WAL the standby still needs, so a disconnected standby
can catch up. It also means a dead standby fills the primary's disk. Set
`max_slot_wal_keep_size` (e.g. `100GB`) on the primary to cap it, and alert on slot lag.
Without slots, use `wal_keep_size` and/or `restore_command` from a WAL archive as fallback.

## Verify
```sql
-- primary
SELECT application_name, client_addr, state, sync_state,
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replay_lag_bytes
FROM pg_stat_replication;
-- standby
SELECT pg_is_in_recovery(), status, sender_host FROM pg_stat_wal_receiver;
```
`state = streaming`, lag near zero, and a test row inserted on the primary is readable on
the standby within a second.

## Gotchas
- `pg_basebackup` copies config files from the primary, including `postgresql.auto.conf` (so any `ALTER SYSTEM`
  values such as `port` or `log_directory` come along); adjust anything host-specific
  (`listen_addresses`, `port`, paths, memory) before first start. Tablespace directories must exist on the standby:
  map them with `-T OLD=NEW` if the standby is on another path (or the same host).
- Firewalls between data centres often kill idle replication connections; set
  `tcp_keepalives_idle` or `wal_receiver_timeout`/`wal_sender_timeout` appropriately.

## Checked
- PostgreSQL 18.6 (Windows scratch cluster, primary on 55432, standby on 55434): `CREATE ROLE ... REPLICATION LOGIN`; `SHOW wal_level` = replica, `max_wal_senders` = 10, `max_replication_slots` = 10; `pg_basebackup -X stream -c fast -P -R -C -S standby1 -T OLD=NEW` created slot `standby1` (`reserved`, inactive until the standby started), wrote an empty `standby.signal` and appended `primary_conninfo` (with spelled-out libpq defaults and no `application_name`) and `primary_slot_name = 'standby1'` to `postgresql.auto.conf`; the copied `postgresql.auto.conf` also carried the primary's own `ALTER SYSTEM` settings, so `port` and `log_directory` had to be overridden; the first attempt without `-T` failed because the primary's tablespace directory was already in use. After adding `application_name=standby1`, the primary's `pg_stat_replication` showed `standby1 | streaming | async`, zero byte lag and sub-second lags; on the standby `pg_stat_wal_receiver` showed `status = streaming`, `pg_is_in_recovery()` = t; data inserted on the primary was readable on the standby.
- Docs: hot-standby page (max_connections, max_prepared_transactions, max_locks_per_transaction, max_wal_senders, max_worker_processes must be equal or higher on the standby), app-pgbasebackup (`-R` creates `standby.signal` and appends connection settings; needs at least one walsender for the backup plus one for WAL streaming; tablespace mapping), warm-standby (slots keep WAL, `max_slot_wal_keep_size` warning), libpq password file page, `wal_receiver_timeout` / `wal_sender_timeout` exist (60 s default).
- Removed the Linux paths, `sudo -u postgres` and the `systemctl` unit (not run).
