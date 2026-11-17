---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ntuser-dat-user-activity-keys
name: ntuser-dat-user-activity-keys
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [ntuser, recentdocs, windows-registry, typedpaths, wordwheelquery, opensavemru, dfir]
level: practitioner
status: draft
description: "Analyse NTUSER.DAT for user activity: RecentDocs, OpenSave and LastVisited MRUs, TypedPaths, WordWheelQuery, RunMRU, mapped drives and per-user autostarts."
sources: ["https://ericzimmerman.github.io/", "https://www.sans.org/posters/windows-forensic-analysis/", "https://github.com/keydet89/RegRipper3.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NTUSER.DAT user activity keys

**Goal:** reconstruct what a specific user opened, searched, typed and ran. Hive:
`Users\<name>\NTUSER.DAT` (plus `.LOG1/.LOG2`; replay logs).

## Key locations (under `Software\Microsoft\Windows\CurrentVersion\Explorer` unless noted)
| Artefact | Key | Meaning |
|---|---|---|
| RecentDocs | `RecentDocs` and per-extension subkeys | Files/folders opened via Explorer; `MRUListEx` gives order; key last write = time of most recent entry |
| OpenSave MRU | `ComDlg32\OpenSavePidlMRU\<ext>` | Files chosen in Open/Save dialogs (browser uploads too) |
| LastVisited MRU | `ComDlg32\LastVisitedPidlMRU` | Executable that used the dialog and folder last used |
| TypedPaths | `TypedPaths` | Paths typed into Explorer address bar (UNC shares!) |
| WordWheelQuery | `WordWheelQuery` | Explorer search terms |
| RunMRU | `RunMRU` | Commands typed in Win+R |
| UserAssist | `UserAssist\{GUID}\Count` | GUI program launches (ROT13) |
| Mapped drives | `Map Network Drive MRU`, `Network\<letter>` (hive root) | Shares used |
| Per-user Run | `Software\Microsoft\Windows\CurrentVersion\Run` | Autostart |
| Office | `Software\Microsoft\Office\<ver>\<app>\File MRU`, `User MRU\...\File MRU` | Office documents opened |

## Tools
Registry Explorer (bookmarks show decoded MRUs), RECmd with batch file over all user
hives, RegRipper `recentdocs`, `comdlg32`, `typedpaths`, `wordwheelquery`, `runmru`,
`userassist`.

## Interpretation
- MRU order plus key last-write time gives the time only for the **most recent** item in
  each key; other entries' times come from correlation (LNK, jump lists).
- Entries persist after files are deleted; they show the file name existed and was used.

## Gotchas
- Dirty hives: without transaction log replay, recent activity is missing.
- Roaming profiles and multiple machines: confirm which host the hive came from.

## Verify
Corroborate key entries with LNK files and jump lists that carry full timestamps and volume
information.
