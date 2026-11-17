---
id: computing-software.cybersecurity-defensive.security-operations.super-timeline-with-plaso
name: super-timeline-with-plaso
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, plaso, super-timeline, log2timeline, psort, timesketch, timeline-analysis]
level: advanced
status: docs-checked
description: "Build and filter a super-timeline with Plaso (log2timeline, pinfo, psort) and review it in Timesketch to reconstruct an intrusion sequence."
sources: ["https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html", "https://plaso.readthedocs.io/en/latest/sources/user/Using-psort.html", "https://plaso.readthedocs.io/en/latest/sources/user/Using-pinfo.html", "https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html", "https://timesketch.org/guides/user/sketch-overview/", "https://github.com/google/timesketch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Super-timelines with Plaso

**Goal:** merge file system times, event logs, registry, browser and application artefacts
into one ordered timeline so the attack sequence becomes visible.

## Build
```
log2timeline.py --storage-file host01.plaso /evidence/HOST01.E01
# narrower: only the parsers you need
log2timeline.py --parsers "win7_slow,!filestat" --storage-file host01.plaso /evidence/kape_output/
pinfo.py host01.plaso
```
- Input can be a single file, a directory or mount point, or a storage media image or device. The default run uses a predefined set of parsers on all discovered file entries.
- Without `--parsers`, pre-processing detects the operating system and uses every preset defined for it (for example `win7` for Windows NT); if no OS is detected, all parsers run.
- `--parsers` takes a comma-separated list of presets, parsers and parser plugins, case-insensitive. A plugin is written `parser/plugin` (for example `sqlite/chrome_27_history`); a leading `!` excludes, and exclusions win. A plugin can only be excluded if its parser is also included. `--parsers list` shows what is available. `win7_slow` is the `win7` preset plus `esedb` and `mft`; `filestat` is the file system stat parser.
- Multiple partitions, BitLocker volumes and Volume Shadow Copies trigger prompts. Avoid them with `--partitions`, `--vss_stores` (for example `all`, `1,4,5`, `none`) and `--unattended` (errors instead of prompting).
- For triage, `-f <filter file>` limits extraction to the file paths in the filter file (for example `{sysregistry}/.+` and `/Users/.+/NTUSER.DAT`); check the result with `pinfo.py --sections sources`.
- `--logfile` redirects log messages to a file; add `-d` for debug detail.
- `pinfo.py` reports when and how the tool was run, pre-processing information, the parsers used, event counts per parser, applied tags and analysis plugin reports; `pinfo.py --compare old.plaso new.plaso` compares counters of two storage files.

## Filter and export
```
psort.py -o dynamic -w host01.csv host01.plaso "date > '2026-10-01 00:00:00' and date < '2026-10-05 00:00:00'"
psort.py -o list
```
- The default output module is `dynamic` and the default time zone is UTC; `--output-time-zone <zone>` changes it for formats such as `dynamic` and `l2tcsv` (`--output-time-zone list` shows zones). Keep UTC for merged timelines.
- `psort.py -o list` lists output modules, including `timesketch` if its dependencies are installed.
- Tagging: `psort.py -o null --analysis tagging --tagging-file <file> timeline.plaso`; filter on tags with `"tag contains '<name>'"`.

## Timesketch
Timesketch is an open-source tool for collaborative forensic timeline analysis. A sketch organises several timelines; use "Import Timeline" to upload a Plaso, CSV or JSONL file. The Explore page has search, filters, charts and saved views, and events can be annotated with comments, tags and stars.

## Analysis approach
1. Start from a known pivot (alert time, malicious file name, first bad login).
2. Look a few minutes either side: what was created, executed, logged in, modified.
3. Expand outward, tagging each event as you go.
4. Build a short narrative timeline for the report from the tagged events.

## Gotchas
- Volume: a single workstation yields very large event counts; filter by time window early.
- File system timestamps (`filestat`) are noisy and can be altered; corroborate with event logs.
- Check clock skew between hosts before merging timelines.
- Full images take a long time to process; run triage collections first.

## Verify
- [ ] The final narrative timeline cites the artefact source for every row.
- [ ] Time zone stated and consistent across all merged hosts.

## Checked
2026-11-08. Confirmed against the Plaso user guide pages (log2timeline, psort, pinfo, parsers and plugins) and the Timesketch GitHub README and sketch-overview guide. Corrected: the time zone option is `--output-time-zone` (the old text had `--output_time_zone`). Removed as unconfirmed: the specific parser string claim "only triage files is faster", hours-long processing figure, Timesketch tag names, analysers (chain of events, browser search, sigma; the analysers guide page 404s), the `data_type:"windows:evtx:record"` query, the claim that parser warnings in `pinfo` mean missed artefacts, the Timesketch "upload the .plaso file directly" statement (the sketch guide confirms Plaso upload via Import Timeline), mactime tag, and the NIST SP 800-86 source.
Method: documentation only; no commands were run.
