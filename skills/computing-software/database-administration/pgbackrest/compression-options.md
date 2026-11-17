---
id: computing-software.database-administration.pgbackrest.compression-options
name: compression-options
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, compress-type, compress-level, zstd, lz4]
level: practitioner
status: docs-checked
description: "Pick compress-type and compress-level for backup and archive, with defaults per algorithm."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: trade CPU for repository size.

`compress-type` options:

- `none`: no compression.
- `bz2`: bzip2.
- `gz`: gzip (default).
- `lz4`: not available on all platforms.
- `zst`: Zstandard, not available on all platforms.

`compress-level` applies when the type is not `none`. Defaults depend on type: bz2 9, gz 6, lz4 1, zst 3.

```
[global]
compress-type=zst

[global:archive-push]
compress-level=3
```

The user guide examples set `compress-level=3` under `[global:archive-push]`. Repository files are compatible with command-line compression tools.

Other related options: `compress-level-network` sets compression for data sent between hosts when using remote protocol; `buffer-size` sets the buffer for copy, compress and encrypt operations (gz compression may use an extra 256KiB of memory).

`compress-level` ranges: bz2 1 to 9, gz -1 to 9, lz4 -5 to 12, zst -7 to 22.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the 'since v2.27' recommendation, the claim about info sizes and the archive-push inheritance paragraph. 

Method: documentation only; no commands were run.
