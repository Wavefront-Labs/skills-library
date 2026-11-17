---
id: computing-software.systems-network-administration.linux.journalctl-output-formats-and-grep
name: journalctl-output-formats-and-grep
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, journalctl, journalctl-output, journal-json, journalctl-grep, journal-fields, short-precise, log-export]
level: practitioner
status: docs-checked
description: "Get the right view out of journalctl: -o short-precise/json/cat/verbose, --grep and case rules, field filters (_PID, _COMM, SYSLOG_IDENTIFIER), --output-fields and export."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# journalctl output formats and searching

## Output modes (-o)
| Mode | Use |
|---|---|
| `short` (default) / `short-iso` / `short-precise` (µs) / `short-monotonic` | reading timelines; precise for ordering bursts |
| `cat` | message only |
| `verbose` | every field of each entry — discover what you can filter on |
| `json` / `json-pretty` / `json-sse` | machine processing |
| `export` | binary-safe stream for `systemd-journal-remote` / archiving |

```bash
journalctl -u nginx -o short-precise --since "10 min ago"
journalctl -u sshd -o json-pretty -n 1
journalctl -o verbose -n 1 _COMM=sshd
journalctl -o json --output-fields=MESSAGE,_PID,PRIORITY -n 5
```

## Searching
- `--grep=PATTERN` / `-g` (PCRE2) on the MESSAGE field; matching is case-insensitive if the pattern is all lowercase, otherwise case-sensitive (override with `--case-sensitive=BOOLEAN`).
- Field matches: `_PID=1234`, `_COMM=cron`, `_EXE=/usr/sbin/sshd`, `SYSLOG_IDENTIFIER=kernel`,
  `_SYSTEMD_UNIT=x.service`, `_UID=1000`, `_TRANSPORT=kernel`, `_HOSTNAME=` (merged remote journals).
  Same field twice = OR; different fields = AND; `+` = OR between groups.
- List values: `journalctl -F _SYSTEMD_UNIT`, `journalctl -F PRIORITY`.
- Combine: `journalctl -b -1 -p warning..alert -g 'timeout|reset'`.

## Practical tips
- `--no-pager`/`-q` in scripts; `-n 200 -f` to follow with context; `-r` reverse.
- `-x` adds explanation texts from the message catalog where available.
- Export a time window for a vendor: `journalctl --since ... --until ... -o export > slice.export`; the stream is imported back into native journal format with `systemd-journal-remote`.

## Verify
- [ ] You can produce the same incident timeline in `short-precise` and as JSON filtered by unit and priority.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: output modes `short`, `short-iso`, `short-precise`, `short-monotonic`, `cat`, `verbose`, `json`, `json-pretty`, `json-sse`, `export`; `--output-fields=` applies to verbose, export, json variants and cat; `-g` PCRE2 and case rule; `--case-sensitive=BOOLEAN`; field matching with `+`; `-F`; `-x`; `--file`; the export stream is imported with `systemd-journal-remote` (so reading it back with `--file` was wrong). Removed the jq pipeline.

Method: documentation only; no commands were run.
