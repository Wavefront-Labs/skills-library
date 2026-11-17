---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.windows-error-reporting-artefacts
name: windows-error-reporting-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [windows-error-reporting, evidence-of-execution, program-execution, crash-dump-analysis, dfir]
level: practitioner
status: draft
description: "Use Windows Error Reporting (WER) files as evidence: Report.wer contents, ReportArchive/ReportQueue locations, crashed malware paths, hashes and event 1000/1001."
sources: ["https://learn.microsoft.com/en-us/windows/win32/wer/windows-error-reporting", "https://learn.microsoft.com/en-us/windows/win32/wer/collecting-user-mode-dumps"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows Error Reporting artefacts

**Goal:** malware and attacker tools crash. When they do, WER records the executable path, version,
hash-related data and loaded modules - sometimes the only proof a since-deleted binary ran.

## Locations
- System-wide: `%ProgramData%\Microsoft\Windows\WER\ReportArchive\` and `ReportQueue\`
- Per-user: `%LOCALAPPDATA%\Microsoft\Windows\WER\ReportArchive\`
- Folder names like `AppCrash_<exe>_<hash>_<id>` or `Kernel_<code>_...`.
- Optional local dumps: `HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps` (`DumpFolder`, default `%LOCALAPPDATA%\CrashDumps`).

## Report.wer fields of interest
- `EventTime` (FILETIME), `AppPath`, `AppName`, `Sig[n]` (application name, version, timestamp,
  faulting module, exception code, offset), `LoadedModule[n]` list (shows injected or side-loaded DLLs),
  `TargetAppId`, `OriginalFilename`, and sometimes `AppSessionGuid`.
- Event logs: Application log event **1000** (Application Error) and **1001** (Windows Error
  Reporting, bucket info) with the same path and module.

## Investigative uses
- Proves execution of a binary path at a time, including from Temp or removable media.
- LoadedModule lists expose DLL side-loading (unexpected DLL path next to a signed EXE).
- Crash of `lsass.exe` after a credential-dumping attempt, or of security products during tampering.
- Local dump files (if configured) contain process memory: decrypted strings, C2 configs.

## Gotchas
- ReportQueue entries are deleted once uploaded/archived; ReportArchive retention is limited.
- Event 1000 timestamps are when the report was written (crash time), not process start time.

## Verify
Correlate Report.wer EventTime with Application log 1000/1001 and other execution artefacts for the same path.
