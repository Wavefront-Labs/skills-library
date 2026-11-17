---
id: computing-software.systems-network-administration.zfs.zpool-scrub-error-and-dates
name: zpool-scrub-error-and-dates
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, scrub, error-scrub, thorough, date-range, continue]
level: advanced
status: docs-checked
description: "Use zpool scrub -e for error scrubs, -t for thorough decryption and decompression checks, -C to continue, and -S and -E to limit by creation date."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced scrub modes

```
zpool scrub [-w] [-t] [-C | [-S date] [-E date]] -a|pool...
zpool scrub -e [-w] -a|pool...
```

## Error scrub: -e

Scrubs only files with known data errors (those in `zpool status -v`). It needs the `head_errlog` feature and at least one earlier scrub with that feature enabled. It cannot run alongside another scrub or resilver or while a scrub is paused, and cannot combine with `-C`, `-p`, `-s` or `-t`. A paused error scrub resumes with `zpool scrub -e`.

## Thorough: -t

Decrypts and decompresses blocks as they are read, catching rare corruption where the checksum matches but decryption or decompression fails. Encrypted datasets need their keys loaded; if keys unload mid-scrub, those blocks get a normal scrub. Cannot combine with `-e`, `-p` or `-s`.

## Continue: -C

Resumes from the last saved transaction group, recorded in the `last_scrubbed_txg` pool property. Cannot combine with `-S`, `-E`, `-e`, `-p` or `-s`, but can combine with `-t`.

## Date range: -S and -E

```
zpool scrub -S "2026-10-01 00:00" -E "2026-10-31 23:59" tank
```

Format `YYYY-MM-DD HH:MM` (hour and minute optional) in the machine's local time zone. `-S` sets the earliest block creation time (default pool creation); `-E` the latest (default most recent). Large clock changes can shift which transaction groups match. `-S` cannot combine with `-C`.

## Checked

2026-11-03. Pages read: zpool-scrub(8).

Confirmed: synopsis, -e prerequisites (head_errlog, earlier scrub) and conflicts, -t behaviour with encrypted keys, -C and last_scrubbed_txg, -S/-E format, time zone and clock-skew caveat.

Method: documentation only; no commands were run.
