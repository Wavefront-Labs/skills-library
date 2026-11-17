---
id: computing-software.systems-network-administration.rclone.rclone-vfs-directory-cache-and-performance
name: rclone-vfs-directory-cache-and-performance
category: computing-software
field: systems-network-administration
product: rclone
tags: [vfs, dir-cache-time, poll-interval, vfs-forget, no-modtime, read-only]
level: advanced
status: docs-checked
description: "Tune how long VFS caches directory listings, refresh them, and cut backend transactions for mounts."
sources: ["https://rclone.org/commands/rclone_mount/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--dir-cache-time` (default 5m) says how long a directory listing is considered fresh. Changes made through the VFS appear immediately. Changes made elsewhere (web UI, another rclone) show up only after expiry, unless the backend supports change polling, in which case `--poll-interval` (default 1m, must be smaller than dir-cache-time, 0 disables) picks them up.

## Forcing a refresh

- Send `SIGHUP` to the rclone process to flush every directory cache, for example `kill -SIGHUP $(pidof rclone)` when one instance is running.
- With the remote control enabled, `rclone rc vfs/forget` flushes everything, or `rclone rc vfs/forget file=path/to/file dir=path/to/dir` targets items.

## Reducing transactions

S3 and Swift benefit hugely from `--no-modtime` (or `--use-server-modtime` for a different trade-off) because each modification-time read is a transaction. Related flags: `--no-checksum` (do not compare checksums on up/download), `--no-seek`, and `--read-only`. With `--read-only`, write attempts fail silently on some platforms, so applications may not report errors.

Out-of-order reads and writes are tolerated for a short wait instead of seeking: `--vfs-read-wait` (default 20ms) and `--vfs-write-wait` (default 1s), which apply only when not using an on-disk cache file.

## Chunked reading

For cloud backends, ranges are read in chunks (`--vfs-read-chunk-size`, default 128M, doubling on each read up to `--vfs-read-chunk-size-limit`, which is off by default) so a seek does not discard a whole streaming download; `--vfs-read-chunk-streams` above 0 reads chunks in parallel. `--links` or `--vfs-links` translate symlinks to regular files with a `.rclonelink` extension.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off). Removed or corrected claims the pages did not confirm.

Method: documentation only; no commands were run.
