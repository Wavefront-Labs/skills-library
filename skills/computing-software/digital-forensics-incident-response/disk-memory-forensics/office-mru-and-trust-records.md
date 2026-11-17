---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.office-mru-and-trust-records
name: office-mru-and-trust-records
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [office-mru, trust-records, ntuser, maldoc, file-access-evidence, dfir]
level: practitioner
status: draft
description: "Analyse Microsoft Office File MRU and Trust Records: documents opened per user with times, and which documents had macros or editing enabled by the user."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Office MRU and Trust Records

**Goal:** list Office documents a user opened and identify documents for which the user
clicked **Enable Content** or **Enable Editing**, a key artefact in maldoc infections.

## File MRU
`NTUSER.DAT\Software\Microsoft\Office\<ver>\<App>\File MRU` (Word, Excel, PowerPoint;
`16.0` for Office 2016-2021/365), and for Microsoft accounts
`...\<App>\User MRU\<LiveId_or_ADAL_id>\File MRU`. Values `Item 1..n`:
`[F00000000][T01D9...][O00000000]*\Users\jdoe\Downloads\invoice.docm`; `T` is a hex
FILETIME of last open (UTC). `Place MRU` lists folders.

## Trust Records
`NTUSER.DAT\Software\Microsoft\Office\<ver>\<App>\Security\Trusted Documents\TrustRecords`
- Value name: full document path (local or URL).
- Data: first 8 bytes FILETIME of when trust was granted; the **last 4 bytes**
  `FF FF FF 7F` indicate **macros enabled** ("Enable Content"); other values typically
  indicate only editing enabled (Protected View exited).

## Parse
Registry Explorer bookmarks (Office), RECmd `Kroll_Batch` includes TrustRecords and MRU;
RegRipper `officedocs2010`, `trustrecords`.

## Use
Phishing investigations: find the maldoc path (usually Downloads or Outlook temp
`Content.Outlook\<random>`), the time macros were enabled, then pivot to process creation
(WINWORD.EXE child processes), Prefetch, and network connections at that time.

## Gotchas
- Path in Outlook's secure temp folder means opened from an email attachment; the file may be
  deleted on close, recover from OST or carving.
- Different Office versions/registry paths per click-to-run vs MSI installs; search all
  versions.

## Verify
Trust record time precedes first malicious process creation by seconds to minutes; the
document hash (if recovered) matches the email attachment.
