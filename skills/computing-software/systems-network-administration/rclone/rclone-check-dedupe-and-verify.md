---
id: computing-software.systems-network-administration.rclone.rclone-check-dedupe-and-verify
name: rclone-check-dedupe-and-verify
category: computing-software
field: systems-network-administration
product: rclone
tags: [check, dedupe, cryptcheck, checksum, duplicates, verification]
level: practitioner
status: docs-checked
description: "Verify copies with rclone check and remove or rename duplicates with dedupe, including by-hash dedupe and modes."
sources: ["https://rclone.org/commands/rclone_check/", "https://rclone.org/commands/rclone_dedupe/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## check

`rclone check source:path dest:path` compares sizes and hashes (MD5 or SHA1) and reports mismatches without changing anything. Options:

- `--size-only` quick check by size only
- `--download` download both sides and compare on the fly (for remotes without hashes)
- `--checkfile HASH` treat the source as a SUM-format file
- `--one-way` only check that source files exist and match on the destination
- report files: `--combined`, `--differ`, `--missing-on-dst`, `--missing-on-src`, `--match`, `--error`, each taking a file name or `-` for stdout

In the combined report, `=` means identical, `-` only in destination, `+` only in source, `*` different and `!` error. For crypt remotes use `rclone cryptcheck`.

## dedupe

Deduping by name is only useful on backends that allow duplicate names (Google Drive, OpenDrive). It first merges identically named directories, then deletes all but one of any identical files (same path and hash) without asking, then resolves remaining duplicates by mode. `--by-hash` finds files with duplicate content on any backend with a hash. Without hashes (crypt over Drive), files are never considered identical unless you add `--size-only`.

`--dedupe-mode` values: `interactive` (default), `skip`, `first`, `newest`, `oldest`, `largest`, `smallest`, `rename`, `list` (report only). Dedupe can cause data loss, so test with `--dry-run` or `-i`.

```console
rclone dedupe --dedupe-mode rename "drive:Google Photos"
```

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
