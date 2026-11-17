---
id: computing-software.systems-network-administration.rclone.rclone-vfs-cache-modes
name: rclone-vfs-cache-modes
category: computing-software
field: systems-network-administration
product: rclone
tags: [vfs, vfs-cache-mode, vfs-cache-max-size, read-ahead, mount, sparse-files]
level: advanced
status: docs-checked
description: "Choose among VFS cache modes off, minimal, writes and full and size the cache for rclone mount and serve commands."
sources: ["https://rclone.org/commands/rclone_mount/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The VFS layer behind mount, nfsmount and the serve commands has four cache modes, set with `--vfs-cache-mode`.

- `off` (default): reads and writes go straight to the remote. Files cannot be opened for read and write, cannot seek when writing, existing files opened for write need O_TRUNC, and a failed upload cannot be retried.
- `minimal`: like off, but files opened for read and write are buffered to disk. Write-only files still cannot seek and failed uploads are not retried.
- `writes`: read-only files are read directly; write-only and read/write files are buffered to disk first. Supports all normal file operations and retries failed uploads at exponentially increasing intervals up to one minute.
- `full`: all reads and writes are buffered to disk, sparse so only downloaded ranges consume space. Otherwise like `writes`. Reads go `--buffer-size` (in memory) plus `--vfs-read-ahead` (on disk) ahead; keep the buffer small and raise read-ahead if needed. FAT and exFAT lack sparse files and perform badly, with an ERROR logged.

## Cache sizing

`--vfs-cache-max-age` (default 1h) evicts by last access, `--vfs-cache-max-size` caps total size and `--vfs-cache-min-free-space` guards the disk, polled every `--vfs-cache-poll-interval` (default 1m). Limits are checked on that interval and open files are never evicted, so the cache can temporarily exceed them. The cache lives under `--cache-dir`.

Run two rclone instances that use overlapping remotes with different `--cache-dir` values; sharing a cache hierarchy can corrupt data. `--transfers` sets parallel uploads from the cache; `--checkers` has no effect on the VFS. Cache fingerprints (size, modtime, hash where available) decide whether a cached copy is stale.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
