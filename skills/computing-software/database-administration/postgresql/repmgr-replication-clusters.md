---
id: computing-software.database-administration.postgresql.repmgr-replication-clusters
name: repmgr-replication-clusters
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, repmgr, automatic-failover, repmgrd, standby-clone, switchover, high-availability]
level: practitioner
status: gated
description: "Build and operate a repmgr-managed PostgreSQL streaming replication cluster: register nodes, clone standbys, switchover, repmgrd failover and fencing."
sources:
  - https://www.repmgr.org/docs/current/index.html
  - https://www.repmgr.org/docs/current/repmgrd-automatic-failover.html
  - https://www.repmgr.org/docs/current/preparing-for-switchover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# repmgr-managed replication clusters

repmgr wraps streaming replication setup (`standby clone`, `register`, `switchover`) and runs `repmgrd` for monitoring and automatic failover. It has no DCS (etcd/Consul); split-brain protection is your job (witness, fencing).

## Config on every node
```ini
# /etc/repmgr.conf
node_id=1
node_name='pg1'
conninfo='host=pg1 user=repmgr dbname=repmgr connect_timeout=2'
data_directory='<DATA_DIR>'
use_replication_slots=yes
failover=automatic
promote_command='repmgr standby promote -f /etc/repmgr.conf --log-to-file'
follow_command='repmgr standby follow -f /etc/repmgr.conf --log-to-file --upstream-node-id=%n'
service_start_command='sudo systemctl start postgresql'
service_stop_command='sudo systemctl stop postgresql'
```
`shared_preload_libraries = 'repmgr'` on all nodes (needed by repmgrd). pg_hba.conf must allow `repmgr` for both `repmgr` db and `replication`.

## Bootstrap
```bash
# primary
repmgr -f /etc/repmgr.conf primary register
# standby (empty data dir)
repmgr -h pg1 -U repmgr -d repmgr -f /etc/repmgr.conf standby clone --dry-run
repmgr -h pg1 -U repmgr -d repmgr -f /etc/repmgr.conf standby clone
systemctl start postgresql
repmgr -f /etc/repmgr.conf standby register
repmgr -f /etc/repmgr.conf cluster show
```

## Planned switchover
```bash
repmgr -f /etc/repmgr.conf standby switchover --siblings-follow --dry-run   # run on the standby to promote
repmgr -f /etc/repmgr.conf standby switchover --siblings-follow
```
Needs passwordless SSH between nodes as postgres. Pause repmgrd first (`repmgr service pause`) on older versions.

## Automatic failover
```bash
repmgrd -f /etc/repmgr.conf --daemonize    # or systemd unit, on every node
repmgr -f /etc/repmgr.conf service status
```
- Add a **witness** node in a third location (`repmgr witness register`) so a network partition does not let both sides promote.
- `location=` per node: repmgrd promotes only if it can see a majority in its location.
- After failover the old primary must be rejoined: `repmgr node rejoin -d 'host=pg2 user=repmgr dbname=repmgr' --force-rewind` (uses pg_rewind; needs `wal_log_hints=on` or checksums).

## Checks
```bash
repmgr cluster show            # roles, upstream, status
repmgr cluster crosscheck      # every node can reach every node
repmgr node check              # lag, slots, archiving on this node
```

## Gotchas
- repmgr does not move a VIP or reconfigure clients; script it in `promote_command` or use a proxy (HAProxy with health checks / PgBouncer reconfiguration).
- An old primary that comes back up after failover is a split brain waiting to happen; fence it (`service_stop_command` on it, or STONITH) before anything else.
- For new builds with a DCS available, Patroni is the more common choice; repmgr suits small static clusters.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; repmgr index/failover/switchover pages fetched but repmgr.conf options and command flags not found on them. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
