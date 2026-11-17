---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso
name: super-timeline-with-plaso
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [disk-forensics, memory-forensics, super-timeline, plaso, log2timeline, psort, pinfo, timesketch, timeline-explorer, evtx, registry, prefetch, amcache, shimcache, lnk, jump-lists, shellbags, mft, usnjrnl, srum, artefacts, windows-forensics, timestomping, anti-forensics, dfir]
level: practitioner
status: gated
description: "Build and read a Windows super-timeline with plaso (log2timeline/psort), filter to the incident window, and know which artefacts prove execution, access and persistence."
sources: ["https://plaso.readthedocs.io/", "https://timesketch.org/", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Super-timeline construction with plaso

**Goal:** merge every timestamp on a system — filesystem, event logs, registry,
browser, execution artefacts — into one sorted timeline, cut it to the incident window,
and interpret it with the right artefact-to-meaning mapping.

## 1. Generate
```bash
# Docker is the least painful install
docker run --rm -v "$PWD":/data log2timeline/plaso log2timeline \
    --storage-file /data/case.plaso /data/image.E01
# useful options:
#   --parsers win7          preset for Windows (check `log2timeline --parsers list`)
#   --partitions all --vss-stores all     include Volume Shadow Copies (old versions of files!)
#   -z UTC                  only if the source has no timezone info; otherwise plaso detects it
pinfo case.plaso            # (via the same docker image) parsers run, event counts, warnings: read it
```
- A full image can take hours and produce tens of millions of events. For fast triage,
  collect a targeted artefact set first (e.g. with a KAPE/velociraptor triage
  collection) and run plaso over that folder.
- Memory images aren't parsed by plaso; export Volatility's `timeliner` output and
  merge by time in Timesketch.

## 2. Filter and export
```bash
psort -o l2tcsv -w timeline.csv case.plaso \
  "date > '2026-09-02 00:00:00' AND date < '2026-09-05 00:00:00'"
psort -o dynamic --output-time-zone UTC -w timeline.csv case.plaso   # dynamic = configurable columns
```
Older plaso releases name the tools `log2timeline.py` / `psort.py` / `pinfo.py`;
check which your install provides. Open in Timeline Explorer (Windows) or import `case.plaso` into **Timesketch** for
search, tagging and collaborative review. Always work in **UTC**.

## 3. Read it — artefacts and what they prove (Windows)
| Question | Artefacts | Notes |
|---|---|---|
| Was a program executed? | Prefetch (`%SystemRoot%\Prefetch\*.pf`), Amcache.hve, BAM/DAM, SRUM, Security 4688 / Sysmon 1 | Prefetch: last 8 run times on Win8+; disabled by default on many servers. **Shimcache** presence alone does *not* prove execution on Win10+. |
| Was a file/folder opened? | LNK files, Jump Lists, ShellBags, RecentDocs, Office MRU | Survive deletion of the target file. |
| What changed on disk? | $MFT, $UsnJrnl:$J, $LogFile | UsnJrnl shows create/rename/delete reasons, even for files now gone. |
| Logons / lateral movement | Security 4624/4625/4648/4672, RDP logs (TerminalServices-*), 7045 service install | See computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting. |
| Persistence | Run keys, Services, Scheduled Tasks (`%SystemRoot%\System32\Tasks`, 4698), WMI subscriptions | |
| Browsing / downloads | Browser history DBs, Zone.Identifier ADS (`HostUrl=`) | Zone.Identifier tells you where a downloaded file came from. |

## 4. Method: pivot, don't scroll
1. Start from a known-bad anchor (malware file creation, an alert time, first bad logon).
2. Look ±5–15 minutes around it; tag every relevant event.
3. Each new artefact (a username, a filename, a source IP) becomes the next search.
4. Work backwards to initial access and forwards to impact.

## Anti-forensics awareness
- **Timestomping:** $STANDARD_INFORMATION altered but $FILE_NAME and UsnJrnl not —
  compare them (plaso emits both MFT timestamp types).
- **Log clearing:** Security 1102 / System 104 events are themselves evidence; gaps in
  record numbers indicate deletion.
- Deleted files may still appear in VSS, UsnJrnl, LNK and Prefetch.
- Clock skew: check the system clock against network evidence before asserting ordering
  across machines.

## Verify
- [ ] `pinfo` reviewed: expected parsers ran, warnings understood.
- [ ] Timeline in UTC; source timezone documented.
- [ ] Execution claims backed by an execution artefact, not by Shimcache or file presence alone.
- [ ] Each conclusion has at least two corroborating artefacts where possible.
- [ ] Tagged events exported as the case timeline.

## Checked

- Date: 2026-11-02.
- Confirmed against: psort and psteal output formats (Plaso Output-and-formatting page) and the filter-style parser presets (Parsers-and-plugins page).
- Not confirmed: log2timeline flags (--storage-file, --partitions, --vss-stores, --output-time-zone) and artefact paths: the Plaso pages fetched are index-level (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
