---
id: computing-software.database-administration.cloudnative-pg.dynamic-shared-memory-posix-vs-sysv
name: dynamic-shared-memory-posix-vs-sysv
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [dynamic-shared-memory, shm, posix, sysv, shmmax, parallel-queries]
level: advanced
status: docs-checked
description: "Choose between posix and sysv dynamic_shared_memory_type in CloudNativePG, inspect the /dev/shm tmpfs and SHMMAX/SHMALL limits, and cap the shm volume size."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dynamic_shared_memory_type` matters mainly for parallel queries. CloudNativePG recommends only two values: `posix` (default; `shm_open`) and `sysv` (`shmget`).

**posix.** Usually enough, because the operator mounts a memory-bound `emptyDir` volume called `shm` at `/dev/shm`. Check its size from inside the Postgres container:

```sh
mount | grep shm
```

The expected shape is `shm on /dev/shm type tmpfs (rw,nosuid,nodev,noexec,relatime,size=...)`. To cap the volume:

```yaml
spec:
  ephemeralVolumesSizeLimit:
    shm: 1Gi
```

**sysv.** Viable when your Kubernetes nodes have high `SHMMAX` and `SHMALL`. Verify from within the container:

```sh
ipcs -lm
cat /proc/sys/kernel/shmall
cat /proc/sys/kernel/shmmax
```

If the reported maximum total shared memory is very large (the page's example shows `18014398509481980` kbytes), setting the following is sensible:

```yaml
dynamic_shared_memory_type: "sysv"
```

The page points to a pgsql-general thread on why this setting matters for memory allocation in parallel queries.

## Checked

2026-11-04. Trimmed claims the page does not state. posix and sysv guidance, verification commands and the shm size limit confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
