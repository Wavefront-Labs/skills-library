---
id: computing-software.cloud-infrastructure-engineering.docker.redis-persistence-in-containers
name: redis-persistence-in-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, redis-container, redis-persistence, redis-aof, redis-rdb, maxmemory, valkey, overcommit-memory, redis-backup]
level: practitioner
status: docs-checked
description: "Run Redis (or Valkey) in a container without losing data: RDB vs AOF, the /data volume, host-level overcommit and huge-page settings, and backup notes."
sources: ["https://hub.docker.com/_/redis", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/", "https://redis.io/docs/latest/operate/oss_and_stack/management/admin/", "https://hub.docker.com/r/valkey/valkey"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis persistence in containers

## Pick a persistence mode
- **RDB snapshots**: compact point-in-time files; you lose writes since the last snapshot. `fork()` for a snapshot can pause serving for milliseconds, or up to a second on a big dataset and slow CPU.
- **AOF** (`appendonly yes`): `appendfsync everysec` fsyncs every second, so you can lose about one second of writes. Since Redis 7.0.0 the AOF is split into several files in the directory named by `appenddirname`.
- Pure cache: disable both and skip the volume.

If persistence is enabled the data lives in `/data` (per the Valkey image page); mount a volume there.

## Compose
```yaml
services:
  redis:
    image: redis:<VERSION>        # or valkey/valkey:<VERSION>
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    volumes:
      - redis-data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf:ro
    stop_grace_period: 30s
volumes:
  redis-data: {}
```
`redis.conf`:
```
appendonly yes
appendfsync everysec
```
Keep passwords out of the command line and `docker inspect`: put them in a mounted config or ACL file rather than passing `--requirepass`.

## Host settings (not settable per container)
Per the Redis administration page, set these on the Linux host:
- `vm.overcommit_memory = 1` (add to `/etc/sysctl.conf`, then reboot or run `sysctl vm.overcommit_memory=1`); background saves can fail with a `fork()` error otherwise.
- Disable Transparent Huge Pages: `echo never > /sys/kernel/mm/transparent_hugepage/enabled`.

## Backups
Copy `dump.rdb` out of the volume; for AOF-only instances copy the `appenddirname` directory, and disable AOF rewrites during the copy or the backup can be invalid (see the persistence page for the steps). Restore with Redis stopped.

## Verify
```bash
docker compose exec redis redis-cli INFO persistence
docker compose restart redis && docker compose exec redis redis-cli DBSIZE    # keys survive
```

## Checked
2026-10-28. Confirmed against the Redis persistence and administration pages and the Valkey Docker Hub page (`/data`, AOF `everysec`, one-second loss, `appenddirname` since 7.0.0, fork pause, overcommit and THP settings). Removed unconfirmed claims: maxmemory-to-limit ratios and copy-on-write doubling, `somaxconn`/`tcp-backlog`, exit 137, ACL file and secrets layout, `madvise` THP setting (the page says `never`), BSD-licence remark, example version tags, grace-period default.
Method: documentation only; no commands were run.
