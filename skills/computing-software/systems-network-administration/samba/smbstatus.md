---
id: computing-software.systems-network-administration.samba.smbstatus
name: smbstatus
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, smbstatus, open-files, connections, locks, monitoring]
level: intro
status: docs-checked
description: "Inspect live Samba connections, shares and locked open files with smbstatus: brief, shares only, locks only, per user, byte-range locks, notify and JSON output."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smbstatus.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smbstatus
| Option | Effect |
|---|---|
| `-b`, `--brief` | brief output |
| `-p`, `--processes` | list smbd processes and exit (scripts) |
| `-S`, `--shares` | shares only |
| `-L`, `--locks` | locks only |
| `-u USER` | limit to a user |
| `-v`, `--verbose` | verbose |
| `-B`, `--byterange` | include byte-range locks |
| `-n`, `--numeric` | numeric UIDs and GIDs |
| `-N`, `--notify` | registered file notifications |
| `-f`, `--fast` | skip checking that referenced processes still exist (can show stale data) |
| `-j`, `--json` | JSON output |
| `-P`, `--profile` | profiling data (needs a profiling build) |
| `-d LEVEL` | log detail 0-10, default 1 |

Examples:
```
smbstatus -b
smbstatus -L -u alice
smbstatus -S
smbstatus -j
```
JSON top-level keys: `timestamp`, `version`, `smb_conf`, `sessions`, `tcons`, `open_files`. Each open lists `sharemode`, `access_mask`, `opened_at`; oplock and lease fields appear only when used. `-B` adds `byte_range_locks` (type, flavour, start, size).

Use it before maintenance to see who holds a file, then act with `smbcontrol smbd close-share` or `kill-client-ip`.

Gotcha: `-f` is faster but may list processes that exited uncleanly.

## Checked

2026-11-04. Confirmed against the smbstatus(1) and smbcontrol(1) manual pages: every option, the -d range and default, JSON keys, oplock/lease/byte-range fields, and that close-share and kill-client-ip are smbcontrol message types.
Method: documentation only; no commands were run.
