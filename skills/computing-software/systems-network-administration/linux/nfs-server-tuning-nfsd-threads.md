---
id: computing-software.systems-network-administration.linux.nfs-server-tuning-nfsd-threads
name: nfs-server-tuning-nfsd-threads
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nfs-server, nfsd-threads, nfs-server-tuning, nfs-conf, nfsstat, rpc-threads, rsize, wsize, nconnect, nfsdcld, performance, sysadmin]
level: advanced
status: docs-checked
description: "Tune a Linux NFS server: nfsd threads and nfs.conf [nfsd] settings, sync versus async exports, and reading nfsstat to find the bottleneck."
sources:
  - https://man7.org/linux/man-pages/man5/nfs.conf.5.html
  - https://man7.org/linux/man-pages/man8/nfsstat.8.html
  - https://man7.org/linux/man-pages/man5/exports.5.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NFS server tuning: nfsd threads and friends

**Goal:** an NFS server that keeps up with its clients: enough nfsd threads, the right
protocol options, and evidence for each change.

## 1. Threads
```bash
cat /proc/fs/nfsd/threads                 # current thread count
rpc.nfsd 64                               # change live
```
Persistent in `/etc/nfs.conf`:
```ini
[nfsd]
threads=64
vers3=n            # NFSv4 only unless v3 clients exist
# host=10.0.10.5   # bind to one address
```
Then restart the NFS server service. The `[nfsd]` section recognises `threads`, `min-threads`, `host`,
`scope`, `port`, `grace-time`, `lease-time`, `udp`, `tcp`, `vers3`, `vers4`, `vers4.0`, `vers4.1`,
`vers4.2` and `rdma` (nfs.conf(5)). Raise the thread count in steps and measure each change; the right
number depends on the workload.

## 2. Server-side settings that matter
- Export `sync` (reply only after changes reach stable storage; the default) versus `async` (replies
  earlier; an unclean restart can lose or corrupt data, exports(5)). Keep `sync` and add faster storage instead.
- The underlying filesystem and disks are usually the real limit: watch disk utilisation during load.
- `lease-time` and `grace-time` (integers, `[nfsd]`) control NFSv4 lease and grace periods.

## 3. Client side
```bash
nfsstat -m                         # mounts and their options
```
Mount options (rsize, wsize, nconnect, hard or soft) are documented in nfs(5); check that page for the
client version before changing them.

## 4. Read the stats
```bash
nfsstat -s                         # server-side statistics
nfsstat -c                         # client-side statistics
```
Lots of getattr and access calls in the server operation mix point to a metadata-heavy workload.

## Gotchas
- Thread changes via `rpc.nfsd N` are lost on restart unless they are in `nfs.conf`.
- More threads will not fix a saturated disk; check disk utilisation first.
- `async` exports on a server that can crash risk data loss.

## Verify
- [ ] After a restart, `/proc/fs/nfsd/threads` shows the count set in `nfs.conf`.
- [ ] `nfsstat -m` on clients shows the intended mount options; throughput measured before and after.

## Checked
2026-10-28. Confirmed in nfs.conf(5): the `[nfsd]` keys listed above and that threads and the two times are
integers; in exports(5): `sync` replies after commit to stable storage, `async` can lose data on a crash,
`sync` is the default; in nfsstat(8): `-s`, `-c`, `-m`. Removed (not confirmed in the sources): default thread
count, `pool_stats` column meanings and tuning rules, thread-count ranges, jumbo-frame and sysctl advice,
nconnect kernel version, actimeo and mountstats/nfsiostat notes.
Method: documentation only; no commands were run.
