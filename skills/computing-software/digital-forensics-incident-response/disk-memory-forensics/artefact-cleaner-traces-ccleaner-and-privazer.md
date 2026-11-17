---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.artefact-cleaner-traces-ccleaner-and-privazer
name: artefact-cleaner-traces-ccleaner-and-privazer
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [ccleaner, privazer, anti-forensics, artefact-cleaners, windows-forensics, dfir]
level: practitioner
status: draft
description: "Find and interpret traces of artefact cleaners such as CCleaner, PrivaZer and BleachBit: install and run evidence, settings revealing what was wiped, and what survives cleaning."
sources: ["https://www.ccleaner.com/docs/ccleaner/advanced-usage/ccleaner-ini-files", "https://privazer.com/en/", "https://www.bleachbit.org/documentation", "https://attack.mitre.org/techniques/T1070/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Artefact cleaner traces (CCleaner, PrivaZer, BleachBit)

Cleaners remove browser history, MRUs, prefetch, temp files and sometimes free-space or MFT entries (T1070). Their use matters in insider cases (timing relative to a litigation hold or resignation) and as evidence of intent. Cleaners rarely remove their own traces completely.

## Proving installation and execution
- Install: Uninstall keys (`SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CCleaner`), program folders (`%SystemDrive%\Program Files\CCleaner`, `%SystemDrive%\Program Files\PrivaZer`), installer in Downloads with Zone.Identifier.
- Execution: Prefetch (`CCLEANER64.EXE-*.pf`, `PRIVAZER.EXE-*.pf`) gives run count and last 8 run times; Amcache, BAM, UserAssist, Windows Timeline; scheduled tasks for automatic cleaning (`CCleanerSkipUAC`, `CCleaner Update`); Event 4688.
- Portable versions leave Prefetch and BAM entries even when not installed.

## What settings reveal
- CCleaner: `HKCU\Software\Piriform\CCleaner` (or `ccleaner.ini` beside a portable exe) lists enabled cleaning rules (e.g. `(App)Recently Typed URLs=True`, `WipeFreeSpaceDrives`), cookies to keep, and last-run values (`UpdateKey`, `CleanerLast...` depending on version). Enabled rules tell you which artefacts to expect missing.
- PrivaZer: `%SystemDrive%\ProgramData\PrivaZer` / `%APPDATA%\PrivaZer` hold settings and logs; it can overwrite `$MFT` entries and free space, and clean USN journal and shellbags.
- BleachBit: `%APPDATA%\BleachBit\bleachbit.ini` lists selected cleaners; logs if enabled.

## Evidence of cleaning itself
- Sudden gaps: browser history starting on a specific date, empty RecentDocs with recent LNK files elsewhere, Prefetch folder nearly empty except the cleaner.
- `$UsnJrnl` (if not cleaned) shows mass deletes in seconds, timed with cleaner execution; `$LogFile`; Volume Shadow Copies retain pre-cleaning artefacts.
- Free-space wiping leaves patterned unallocated space (zeros or random) and a long process run time.

## What usually survives
VSS snapshots, event logs (unless separately cleared), SRUM, Amcache, cloud-synced browser history, server-side logs (proxy, M365), and artefacts outside the cleaner's rule set.

## Gotchas
- CCleaner and similar are common legitimate utilities; presence is not proof of intent. Focus on timing, settings and which artefacts were targeted.
- Default rules differ by version; check the specific version's defaults before interpreting.

## Verify
The report states which cleaner, which version, run times with sources, which artefact classes were affected, and recovery from shadow copies or other sources where attempted.
