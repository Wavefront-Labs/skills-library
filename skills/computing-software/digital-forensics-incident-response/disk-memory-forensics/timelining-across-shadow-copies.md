---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.timelining-across-shadow-copies
name: timelining-across-shadow-copies
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [vss-timeline, volume-shadow-copy, plaso, log2timeline, mftecmd, super-timeline, dfir]
level: advanced
status: docs-checked
description: "Build a timeline that spans Volume Shadow Copies plus the live volume with Plaso log2timeline (--vss_stores, --partitions, --parsers, filter files) and deduplicate across stores."
sources: ["https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html", "https://github.com/libyal/libvshadow", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timelining across shadow copies

**Goal:** recover timeline events that survive only in older snapshots (overwritten logs, earlier registry states, MFT records of deleted files) and merge them with the current volume. The VSS format is used by Windows, as of Vista, to maintain copies of data on a volume (libvshadow README); libvshadow provides tools to access it and is marked alpha.

## Plaso with log2timeline.py
Basic form: `log2timeline.py --storage-file OUTPUT INPUT`; the output is a Plaso storage file analysed with `pinfo` and `psort`. When the image has several partitions, an encrypted partition or Volume Shadow Copies, the tool prompts, unless you preselect:
- `--partitions PARTITION_NUMBERS` (the prompt also accepts "all"),
- `--vss_stores` with `all`, a list such as `1,4,5`, a range such as `1..3`, or `none`,
- `--unattended` to error instead of prompting.

```bash
log2timeline.py --storage-file case.plaso --vss_stores all --partitions 2 image.E01
```
Select parsers with `--parsers` (comma list of presets, parsers and `parser/plugin` names; `!` excludes and takes precedence; list available names with `--parsers list`). Without it, pre-processing picks a preset matching the detected operating system (for example `win7` for Windows NT), else all parsers. Use a filter file (`-f filter`) to extract from selected paths only, for example `{sysregistry}/.+` and `/Users/.+/NTUSER.DAT`; check what was collected with `pinfo.py --sections sources`.
- `--logfile` redirects log messages to a file (`.log.gz` compresses it); `--info` prints supported parsers, presets and output modules.

## Targeted per-store approach (faster)
Expose each shadow copy read-only with a VSS-aware tool (libvshadow's tools, or your imaging suite), run your MFT and event log parsers (for example Eric Zimmerman's command-line tools listed on his site) on each store separately with a per-store label in the output, concatenate, and deduplicate events that are identical across stores (same path, timestamp, event type), keeping the earliest source label.

## Why it matters
- Logs roll over; an older store may still hold events from before a log was cleared.
- File system records of deleted tools can survive in a snapshot taken before deletion.
- Compare registry key last-write times across stores to see when keys changed between snapshots.

## Gotchas
- Duplicates are the main nuisance: unchanged files produce identical entries per store.
- Snapshot creation time is not event time; track both.
- Full runs are long; narrow parsers and filters first.

## Self-check
The timeline marks which events come only from a snapshot, and at least one key event is corroborated by a second artefact.

## Checked
2026-11-08. Confirmed against the Plaso "Using log2timeline.py" guide, the libvshadow README and the Eric Zimmerman tools page: storage-file syntax, partition/VSS prompts and options, `--parsers` syntax and precedence, preset selection, filter files, `--logfile`, `--info`, VSS format description. Removed as unconfirmed: psort output module and date filter syntax, `VSS<N>:` path labelling, `win7_slow`, mount commands for per-store access, vss_carver, and event ID lists.
Method: documentation only; no commands were run.
