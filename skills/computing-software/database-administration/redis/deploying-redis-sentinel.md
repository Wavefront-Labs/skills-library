---
id: computing-software.database-administration.redis.deploying-redis-sentinel
name: deploying-redis-sentinel
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-sentinel, sentinel-quorum, sentinel-monitor, down-after-milliseconds, announce-ip, failover]
level: practitioner
status: docs-checked
description: "Deploy Redis Sentinel for automatic failover: three sentinels on separate hosts, quorum, down-after-milliseconds, auth, announce settings behind NAT, and failover tests."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Redis Sentinel

## Topology
At least **three Sentinel processes on three independent hosts** (often co-located with the
master and two replicas, or with app servers). One master, one or more replicas.

## sentinel.conf
```
port 26379
sentinel monitor mymaster 10.0.1.10 6379 2         # name, master ip, port, quorum
sentinel auth-user mymaster sentinel-user          # ACL user (6.2+) or:
sentinel auth-pass mymaster <password>
sentinel down-after-milliseconds mymaster 5000     # unresponsive this long = subjectively down (default 30000)
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1                 # replicas resyncing at once after failover
# Sentinel's own auth: password-only = the same requirepass on every Sentinel
# (6.2+ ACL variant: sentinel-user / sentinel-pass)
requirepass <sentinel-password>
# behind NAT / Docker port mapping:
# sentinel announce-ip 203.0.113.5
# sentinel announce-port 26379
# replica-announce-ip on the redis nodes too
# sentinel resolve-hostnames yes / announce-hostnames yes   (6.2+) for DNS names
```
Sentinel saves its current state in this file and reloads it on restart; it refuses to start if the path is not writable.

## Quorum vs majority
- **Quorum** (2 above): how many sentinels must agree the master is down to declare
  ODOWN (objectively down).
- To actually perform a failover, a **majority** of all sentinels must vote for the leader.
  With 3 sentinels, 2 must be reachable. With only 2 sentinels, losing one host blocks failover.

## Redis nodes
Replicas: `replicaof 10.0.1.10 6379`, `masterauth`/`masteruser` set on **all** nodes (the
master becomes a replica after failover and must authenticate to the new master).
`min-replicas-to-write 1` + `min-replicas-max-lag 10` on the master limits writes accepted by
an isolated old master (data loss window in a partition).

## Operate
```
redis-cli -p 26379 SENTINEL masters
redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
redis-cli -p 26379 SENTINEL replicas mymaster
redis-cli -p 26379 SENTINEL sentinels mymaster
redis-cli -p 26379 SENTINEL ckquorum mymaster        # can we reach quorum and majority?
redis-cli -p 26379 SENTINEL failover mymaster        # forced failover (test/maintenance)
redis-cli -p 26379 SENTINEL reset mymaster           # forget stale replicas/sentinels
```

## Gotchas
- Clients must be Sentinel-aware (ask sentinels for the master address, react to
  `+switch-master`), or use a proxy; hardcoding the master IP defeats failover.
- Removing a sentinel requires `SENTINEL RESET *` on the others, or they keep counting it.
- Asynchronous replication: acknowledged writes on the old master can be lost at failover.

## Verify
`SENTINEL ckquorum mymaster` returns OK; `SENTINEL failover mymaster` promotes a replica within
seconds, `get-master-addr-by-name` returns the new address, and the application keeps working.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the Sentinel page and sentinel.conf (8.2): at least three Sentinels on independently failing hosts; quorum only detects failure, a majority authorises failover; `sentinel monitor <name> <ip> <port> <quorum>`; defaults down-after-milliseconds 30000 and failover-timeout 180000 (examples here use shorter values); `auth-user` (ACL, 6.2+), `sentinel-user`/`sentinel-pass`, password-only `requirepass` on all Sentinels; `resolve-hostnames`/`announce-hostnames` (6.2+); `announce-ip` for NAT; SENTINEL CKQUORUM, FAILOVER, REPLICAS, SENTINELS, RESET and `SENTINEL RESET *` after removing a Sentinel; `min-replicas-to-write`/`min-replicas-max-lag`; masterauth on all nodes.
Method: documentation only; no commands were run.
