---
id: computing-software.digital-forensics-incident-response.incident-response-process.print-based-exfiltration-evidence
name: print-based-exfiltration-evidence
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [print-forensics, insider-threat, data-exfiltration, windows-event-logs, dfir]
level: practitioner
status: draft
description: "Prove or rule out document printing as an exfiltration path: PrintService operational log, spool files, print server and printer job logs, and correlation."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Print-based exfiltration evidence

**Goal:** printing defeats DLP on USB and email; investigators need to show what was printed, by
whom, where and when.

## Windows client and print server
- **Microsoft-Windows-PrintService/Operational** (disabled by default; enable via `wevtutil sl
  Microsoft-Windows-PrintService/Operational /e:true` or GPO). Event **307** "Document N, <name>
  owned by <user> on <client> was printed on <printer> through port <port>. Size in bytes: X.
  Pages printed: Y". Document name often includes the file name or window title.
- Event 800/842 related job details on newer builds.
- On print servers this log is the central record; collect it before rotation.

## Spool files
- `%SystemRoot%\System32\spool\PRINTERS\*.SPL` and `*.SHD` exist while jobs queue; retained if
  "Keep printed documents" is set on the printer. SPL in EMF format can be rendered to recover
  page content (tools like EMF Spool Viewer). Deleted SPL/SHD can be carved from unallocated.

## Printer and MFD logs
- Enterprise MFDs keep job accounting logs (user, document name, pages, time) and sometimes
  image logs / stored copies on internal disk. Request exports from the print management system
  (PaperCut, uniFLOW) - often the best evidence.

## Correlate
- File access before the print: LNK/jump lists, Office MRU for the document, SharePoint
  `FileAccessed` events.
- Badge records showing presence at the printer if it is a release-print system.

## Gotchas
- PrintService/Operational is off by default: absence of events is not absence of printing.
- Document names are truncated and may be generic ("Microsoft Word - Document1").
- Personal home printers connected to company laptops show as local printer ports (USB001, WSD).

## Verify
Print events are corroborated by file-access artefacts and print management logs.
