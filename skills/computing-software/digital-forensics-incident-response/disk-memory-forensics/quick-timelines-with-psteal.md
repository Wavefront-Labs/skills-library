---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.quick-timelines-with-psteal
name: quick-timelines-with-psteal
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [psteal, plaso, log2timeline, super-timeline, timeline-analysis, dfir]
level: practitioner
status: gated
description: "Produce a quick super-timeline with Plaso's psteal in one command: sources, parsers, output formats, keeping the .plaso storage file and when to switch to log2timeline plus psort."
sources: ["https://plaso.readthedocs.io/en/latest/sources/user/Using-psteal.html", "https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html", "https://plaso.readthedocs.io/en/latest/sources/user/Output-and-formatting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quick timelines with psteal

`psteal` runs Plaso extraction (log2timeline) and output (psort) in one step. Use it for a fast first timeline of an image or triage package; switch to the two-step workflow when you need filtering, multiple outputs or tagging.

## Usage
```bash
psteal.py --source disk.E01 -o dynamic -w timeline.csv
psteal.py --source /cases/triage/HOST01 --parsers win7_slow -o l2tcsv -w host01.csv
psteal.py --source disk.E01 --storage-file host.plaso -o dynamic -w host.csv
```
- `--source`: image (raw, E01, VMDK, VHD), device, directory or single file.
- `-o`: output module (`dynamic` CSV is default-friendly, `l2tcsv`, `json_line`, `xlsx`, `opensearch`); `-w`: output file.
- `--parsers`: preset or list (`win7`, `win7_slow`, `linux`, `macos`, or `!filestat` to exclude MFT stat events for a smaller timeline).
- `--storage-file`: keep the `.plaso` database so you can re-run psort with filters later instead of re-extracting.
- `--partitions all --volumes all` and `--vss_stores all` (or `none`) avoid interactive prompts on multi-partition images.
- Time zone: Plaso stores UTC; `--output_time_zone` sets display only.

## When to move to log2timeline + psort
- You need a date-window or source filter: `psort.py -o dynamic -w out.csv host.plaso "date > '2026-10-01' AND date < '2026-10-05'"`.
- Large images where a full parse takes hours: use log2timeline with a filter file (`-f`) to parse only targeted artefacts.
- Analysis in Timesketch: log2timeline output `.plaso` uploads directly.

## Practical tips
- Run on a fast local disk; Plaso is I/O heavy. Use `--workers` to match CPU cores.
- Check `pinfo.py host.plaso` afterwards for parser counts and errors; a parser with zero events may mean missing artefacts or unsupported versions.
- CSV timelines get huge; load into Timeline Explorer (Windows) or Timesketch rather than Excel.

## Gotchas
- Without `--storage-file`, psteal's intermediate storage is still created; know where it went before deleting.
- Default parsers include `filestat` events for every file, inflating output; exclude when you only need artefact events.

## Verify
`pinfo` shows the expected parsers produced events, and spot-checked events (a known logon, a known file creation) appear in the timeline at the right UTC time.

## Checked

- Date: 2026-11-02.
- Confirmed against: psteal and psort output formats l2tcsv and json_line, win7_slow parser preset (Plaso docs).
- Not confirmed: psteal flag spellings (--source, --storage_file, --output_time_zone, --workers) since the psteal usage page is a stub (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
