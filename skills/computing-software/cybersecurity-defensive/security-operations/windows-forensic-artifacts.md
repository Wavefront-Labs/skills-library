---
id: computing-software.cybersecurity-defensive.security-operations.windows-forensic-artifacts
name: windows-forensic-artifacts
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, windows-forensic-artifacts, prefetch, amcache, shimcache, srum, lnk-files, jump-lists, shellbags, registry-forensics, eric-zimmerman-tools, evtx]
level: advanced
status: docs-checked
description: "Interpret key Windows artefacts (Prefetch, Amcache, ShimCache, SRUM, LNK, jump lists, ShellBags, event logs) with the tools that parse them, to prove execution and file access."
sources: ["https://ericzimmerman.github.io/", "https://github.com/EricZimmerman/PECmd", "https://github.com/EricZimmerman/AmcacheParser", "https://github.com/EricZimmerman/AppCompatCacheParser", "https://github.com/EricZimmerman/Srum", "https://github.com/EricZimmerman/LECmd", "https://github.com/EricZimmerman/JLECmd", "https://github.com/EricZimmerman/Evtx", "https://github.com/EricZimmerman/KapeFiles", "https://docs.velociraptor.app/artifact_references/pages/windows.forensics.prefetch/", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows forensic artefacts

**Goal:** answer "did this run, when, by whom, and what did they touch" from artefacts that
survive after the attacker has cleaned up. Tool names below are Eric Zimmerman's command-line parsers.

## Evidence of execution
| Artefact | What the parser reports | Parser |
|---|---|---|
| Prefetch (`.pf` files, including compressed Windows 10/11 ones) | Executable name, full path and hash, run count, last run times, volumes, directories and files loaded | PECmd |
| Amcache (`Amcache.hve`, Windows 7 to 11) | File entries linked to the Program entries they came from, with SHA-1; on Windows 10/11 the data sits in `Root\InventoryApplicationFile` and other `Root\Inventory*` keys | AmcacheParser |
| ShimCache (AppCompatCache, in the SYSTEM hive or the live registry) | Path, last modified time and, where the format has it, an `Executed` flag (Windows 10/11: tag 0x100 in the entry data) | AppCompatCacheParser |
| SRUM (`SRUDB.dat`) | Network usage and connections, app resource use, energy usage, push notifications and the app timeline, per app and user | SrumECmd |
| Event logs | Security event 4688 records process creation; its Process Command Line field is empty unless the "Include command line in process creation events" policy is enabled | EvtxECmd |

Notes from the tool documentation:
- Prefetch: on Windows 10 the last 8 execution times plus the creation time are visible (Velociraptor `Windows.Forensics.Prefetch` documentation).
- Amcache: on Windows 11 26H1 and later the `Root\Inventory*` keys are replaced by `Inventory*.db` SQLite databases, which AmcacheParser also reads. A hive upgraded from Windows 8 can hold old-format entries.
- ShimCache: a `Path` value on packaged (UWP) app entries holds tab-separated fields and no time.
- SRUM: a `SRUDB.dat` collected from a running system is usually dirty; SrumECmd works on a copy and handles that itself. Pass the SOFTWARE hive (`-r`) to fill in user names and Wi-Fi profile names.

## File and folder access
- **LNK files** (LECmd): target paths and time stamps, the volume or network share the target was on, and tracker data (the machine and MAC address that created the shortcut).
- **Jump lists** (JLECmd): automatic (`*.automaticDestinations-ms`) and custom (`*.customDestinations-ms`) lists, the DestList entries, the AppId of the owning program and the shortcuts inside.
- **ShellBags**: exported with SBECmd (command line) or ShellBags Explorer (GUI).
- **OpenSavePidlMRU, LastVisitedPidlMRU**: registry keys that RECmd plugins read as shell items.

## Persistence
See MITRE ATT&CK for what to look for: scheduled tasks (T1053.005), Registry Run keys and Startup folder (T1547.001) and WMI event subscriptions (T1546.003).

## Workflow
1. Collect with KAPE using the `!SANS_Triage` compound target. It bundles targets including EvidenceOfExecution, RegistryHives, ScheduledTasks, SRUM, LNKFilesAndJumpLists, WebBrowsers, WBEM, BITS, FileSystem and CombinedLogs. Large optional targets (Recycle Bin data files, Outlook PST/OST, cloud storage user files) are left out; run a target with `--sim` first to see how many files and how much data it would return.
2. Parse in bulk with the `!EZParser` compound module, which runs AmcacheParser, AppCompatCacheParser, EvtxECmd, JLECmd, LECmd, MFTECmd, PECmd, RBCmd, RecentFileCacheParser, RECmd, SBECmd, SQLECmd, SrumECmd, SumECmd and WxTCmd. KAPE module flags: see the KAPE manual linked from the KapeFiles README.
3. Open the CSVs in Timeline Explorer (filter, group, sort); narrow to the incident window and pivot on file names, hashes and users.

## Gotchas
- ShimCache and Amcache show that a file was present or evaluated; confirm execution with a second artefact.
- Parser JSON output stores time stamps in ISO 8601 UTC; keep the whole report in UTC and name the source artefact beside each time.
- MFTECmd parses `$MFT`, `$Boot`, `$J`, `$SDS`, `$I30` and `$LogFile` for file-system timelines.

## Verify
- [ ] Each "executed" claim is backed by at least two independent artefacts.
- [ ] Times in the report are stated in UTC with the source artefact named.

## Checked
2026-11-08. Confirmed against the fetched pages: the Eric Zimmerman tool index and the PECmd, AmcacheParser, AppCompatCacheParser, Srum (SrumECmd), LECmd, JLECmd, EvtxECmd and KapeFiles README pages; the `!SANS_Triage.tkape` and `!EZParser.mkape` files in the KapeFiles repository; the Microsoft Learn event 4688 page; MITRE ATT&CK technique titles T1053.005, T1547.001 and T1546.003. Removed as unconfirmed by any readable page: all file locations except the SRUM one, "workstations only by default" and the Prefetch-disabled gotchas (the "last 8 run times" figure is now cited to the Velociraptor Prefetch page), "30-60 days" SRUM retention, BAM/DAM, the Sysmon 1 and PowerShell 4104 claims, the ShellBags removable-device claim, USBSTOR and `setupapi.dev.log`, the Velociraptor `Windows.KapeFiles.Targets` collection (the Velociraptor docs page was a stub), the `KAPE --msource` command line, the ShimCache "not reliable proof" statement (replaced by the documented `Executed` column), and the NIST SP 800-86 and SANS poster sources (the poster page is a login-gated landing page).
Method: documentation only; no commands were run.
