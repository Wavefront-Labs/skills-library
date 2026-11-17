---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.windows-11-pca-execution-logs
name: windows-11-pca-execution-logs
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [user-activity-artefacts, pca-launch-dictionary, program-compatibility-assistant, evidence-of-execution, windows-11, dfir]
level: practitioner
status: draft
description: "Use Windows 11 Program Compatibility Assistant files (PcaAppLaunchDic.txt, PcaGeneralDb) as evidence of program execution with paths and last run times."
sources: ["https://aboutdfir.com/new-windows-11-pro-22h2-evidence-of-execution-artifact/", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows 11 PCA execution logs

**Goal:** use a Windows 11 22H2+ artefact that records executables launched via Explorer
with full paths and timestamps.

## Location
`Windows\appcompat\pca\`:
- `PcaAppLaunchDic.txt`: one line per executable: `full path|last execution time`
  (UTC, `YYYY-MM-DD HH:MM:SS.fff`). Plain text, UTF-16LE.
- `PcaGeneralDb0.txt`, `PcaGeneralDb1.txt`: pipe-delimited records of compatibility events
  (run status, path, product name, company, version, program ID, exit codes) with times;
  files alternate as they fill.

## Parse
Text: open in an editor or import as pipe-delimited CSV; KAPE target `PCA` (or `WindowsPCA`
depending on version) collects them; timeline tools treat the time as UTC.

## Interpretation
- Records programs launched through the shell (Explorer double-click, shortcuts) on Windows
  11 22H2 and later; programs run from command lines or services may not appear.
- Includes executables from removable media and user folders, valuable when Prefetch is
  disabled (servers) or purged.
- Survives deletion of the executable.

## Use with
Amcache (hash, first seen), Prefetch, BAM, UserAssist; compare times to resolve
discrepancies.

## Gotchas
- Not present on Windows 10 or Windows 11 before 22H2.
- File grows and is trimmed; not a complete history.

## Verify
For a known test program run on a reference Windows 11 system of the same build, confirm the
PCA entry appears with matching UTC time before relying on absence/presence in casework.
