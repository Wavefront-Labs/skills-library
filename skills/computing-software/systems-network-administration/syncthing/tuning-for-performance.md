---
id: computing-software.systems-network-administration.syncthing.tuning-for-performance
name: tuning-for-performance
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, tuning, performance, concurrency]
level: advanced
status: docs-checked
description: "Tune Syncthing for speed with copiers, hashers, pullerMaxPendingKiB, maxFolderConcurrency and related options."
sources: ["https://docs.syncthing.net/users/tuning.html", "https://docs.syncthing.net/advanced/option-max-concurrency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuning for high performance

Use a 64-bit build and keep the index database on an SSD. Then adjust.

## Global options
- `progressUpdateIntervalS`: `-1` disables progress updates.
- `setLowPriority`: `false` runs at normal priority.
- `maxFolderConcurrency`: how many folders may be syncing or scanning at once (default is the number of logical CPU cores, negative means no limit). Match it to the storage, since two folders on one spinning disk lose from concurrency.
- `maxConcurrentIncomingRequestKiB`: global limiter, default 262144 (256 MiB). Consider 1048576 or more with spare memory.

## Per folder
- `fsWatcherEnabled` avoids heavy periodic scans.
- `copiers` and `hashers` raise parallelism if I/O and CPU allow.
- `pullerMaxPendingKiB` defaults to 32768 and helps on high latency links.
- `scanProgressIntervalS`: `-1` disables scan progress.
- `maxConcurrentWrites` defaults to 16. Raise it if you raised other concurrency.
- `blockPullOrder`: `inOrder` can help spinning disks with one source.
- `copyRangeMethod`: a copy-on-write method, if the filesystem supports it, reduces data copied on disk.
- `caseSensitiveFS`: enabling it skips safety checks needed on case-insensitive filesystems. It can cause data loss if the filesystem is not in fact case sensitive.
- `disableFsync` is faster but risks data loss on power failure.
- Ownership and xattr syncing carry a fairly high cost.

## Per device
`numConnections` at or above the CPU core count allows maximum TLS concurrency.

## Environment
For large setups, set `GOMEMLIMIT` to the memory you want Syncthing to use, and tune `GOGC`.

## Checked

2026-11-09. Confirmed against the Syncthing Configuration Tuning page (users/tuning) and the maxFolderConcurrency page (advanced/option-max-concurrency), raw rst from syncthing/docs: every option and default above (256 MiB, 32768 KiB, 16 writes), the 1048576 KiB suggestion, SSD/64-bit advice, GOMEMLIMIT and GOGC. Removed: the line telling the reader to set GOMAXPROCS to cap CPU (the page lists it only under the low-resource profile); the vague "as covered in their own pages" for copyRangeMethod and caseSensitiveFS, replaced with what the tuning page says.

Method: documentation only; no commands were run.
