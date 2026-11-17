---
id: computing-software.systems-network-administration.rclone.rclone-performance-tuning
name: rclone-performance-tuning
category: computing-software
field: systems-network-administration
product: rclone
tags: [performance, transfers, checkers, multi-thread-streams, max-buffer-memory, order-by, fast-list]
level: advanced
status: docs-checked
description: "Tune rclone for many small files, large files and mixed workloads using transfers, checkers, chunks, buffers and listing flags."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults are conservative. Change one setting at a time and measure with `-P` or `--stats 1m --stats-one-line --stats-log-level NOTICE`. A transfer is limited by network, request rate, disk IO, CPU or memory; raise the limit you hit until the next one appears.

## Lots of small files

Time is dominated by round trips, so do more at once. `--transfers` (default 4) sets parallel files: raise it until the rate stops rising or errors appear. `--checkers` (default 8) sets parallel listings and comparisons. HTTP 429 or 503 errors or many low-level retries mean you went too far: lower both or cap with `--tpslimit`. Spinning disks and network filesystems can get slower with more parallelism.

## Large files

Files above `--multi-thread-cutoff` on supporting backends are transferred as parallel chunks. `--multi-thread-streams` (default 4) works for all backends, so raise it first. Chunk size is usually a backend flag such as `--s3-chunk-size`; backends without one (local, smb) use `--multi-thread-chunk-size`. Worst-case buffer memory is `--transfers * upload concurrency * chunk size`. Lower upload concurrency, or set `--max-buffer-memory`, which makes transfers wait at the limit. `--use-mmap` returns buffer memory to the OS sooner.

## Mixed sizes

`--order-by size,mixed,50` makes half the transfers take the smallest backlog files and half the largest, keeping both bandwidth and request rate busy. Pair it with a large `--max-backlog` so rclone can order and estimate more accurately.

## Doing less work

Use server-side copy where possible; try `--fast-list` on bucket remotes (fewer transactions, more memory, may be slower, so test); `--no-traverse` when copying few files into a large destination; `--size-only` or `--checksum` to avoid modtime reads (an extra request per file on s3 and swift), or `--use-server-modtime` with `--update`; and `--no-check-dest` only when no destination files exist.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off). Removed or corrected claims the pages did not confirm.

Method: documentation only; no commands were run.
