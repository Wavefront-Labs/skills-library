---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.mount-distributed-locks-dlm
name: mount-distributed-locks-dlm
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [dlm, flock, fcntl, posix-locks]
level: advanced
status: docs-checked
description: "Coordinate writers across several weed mount instances with -dlm: filer-held locks with 7s TTL, cross-mount flock/fcntl, and when it is disabled."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/FUSE-Mount
  - https://github.com/seaweedfs/seaweedfs/wiki/Distributed-POSIX-Locks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mount distributed locks dlm

Without it, mounts are independent: last writer wins on flush, and flock/fcntl locks are per mount.

Enable per mount:
```bash
weed mount -filer=localhost:8888 -dir=/mnt/seaweedfs -dlm
```
Write coordination: opening a file for write acquires a cluster-wide lock on that file, held by the filer's lock service. Other mounts opening the same path for write block until it is released. The lock has a 7s TTL renewed by heartbeat, so if a mount crashes the filer drops the lock and waiters unblock.

POSIX locks: `flock(2)` and `fcntl(F_SETLK/F_SETLKW)` become honored by every mount of the cluster. The owner filer per inode keeps an in-memory lock table; non-owner filers forward one hop. Blocking acquires are client-side polling with bounded backoff, with no server-side wait queue.

Gotchas:
- DLM is automatically disabled if `-writebackCache` is set (writeback implies single-writer).
- Locks are advisory and transient, not replicated; they rely on the filer ring.
- Adds latency per open-for-write, so enable only when several mounts write the same files.

Verify: hold `flock` on mount A, then try on mount B and watch it block.

## Checked
Checked 2026-11-09: `-dlm` opt-in, 7s write-lock TTL, automatic disable with `-writebackCache`, owner-filer one-hop forwarding, in-memory unreplicated lock table and client-side polling for blocking acquires all match the pages. Removed the lock-key claim (the FUSE-Mount page says filer path in one section and inode number in another).
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages FUSE-Mount and Distributed-POSIX-Locks, both read in full from a local clone of the wiki.
