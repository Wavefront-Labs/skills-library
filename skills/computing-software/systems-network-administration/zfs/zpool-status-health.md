---
id: computing-software.systems-network-administration.zfs.zpool-status-health
name: zpool-status-health
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, status, health, errors, json, slow-io]
level: intro
status: docs-checked
description: "Read pool health with zpool status: -x, -v, -e, -s slow I/O counts, -t and -i status, -g GUIDs, -L and -P paths, and JSON output."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-status.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool status

```
zpool status [-DdegiLPpstx] [-v|-vv] [-c script1[,script2,...]] [-j|--json [--json-flat-vdevs] [--json-int] [--json-pool-key-guid]] [-T d|u] [--power] [pool] [interval [count]]
```

With no pool, all pools are shown. During a scrub or resilver it reports percent done and an approximate time to completion.

## Quick checks

```
zpool status -x      # only pools with errors or unavailable
zpool status -e tank # only unhealthy vdevs
zpool status -v tank # files with data errors since the last complete scrub
```

`-vv` also lists corrupt records inside each file.

## Flags

- `-s`: count of slow I/Os per leaf vdev (those longer than `zio_slow_io_ms`, default 30000 ms). Slow is not failed, but may point at storage problems.
- `-i`: initialization status; `-t`: TRIM status.
- `-g`: GUIDs instead of names (usable in `detach`, `offline`, `remove`, `replace`).
- `-L`: resolve symlinks to real paths; `-P`: full paths.
- `-p`: exact numbers.
- `-D`: dedup histogram (`-DD` adds ARC residency).
- `-d`: Direct I/O verify error counts.
- `-c`: run scripts per vdev and add columns, like `zpool iostat -c`.
- `-T d|u`: timestamp.
- `-j` / `--json`: JSON output.

## Checked

2026-11-03. Pages read: zpool-status(8).

Confirmed: the synopsis, -x, -e, -v/-vv, -s with zio_slow_io_ms default 30000, -i, -t, -g, -L, -P, -p, -D/-DD, -d, -c, -T, -j.

Removed or corrected: the alert advice quoting an output string, which the page does not contain.

Method: documentation only; no commands were run.
