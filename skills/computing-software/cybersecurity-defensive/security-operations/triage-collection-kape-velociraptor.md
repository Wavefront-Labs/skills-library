---
id: computing-software.cybersecurity-defensive.security-operations.triage-collection-kape-velociraptor
name: triage-collection-kape-velociraptor
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, kape, velociraptor, triage-collection, targets-and-modules, remote-collection, artifact-collection, hunts, dfir]
level: advanced
status: docs-checked
description: "Collect forensic triage packages with KAPE targets and modules and Velociraptor artifacts instead of imaging every disk; choose artifacts per question and limit endpoint load."
sources: ["https://github.com/EricZimmerman/KapeFiles", "https://raw.githubusercontent.com/EricZimmerman/KapeFiles/master/Targets/Compound/!SANS_Triage.tkape", "https://raw.githubusercontent.com/EricZimmerman/KapeFiles/master/Modules/Compound/!EZParser.mkape", "https://docs.velociraptor.app/docs/deployment/", "https://docs.velociraptor.app/artifact_references/pages/windows.forensics.prefetch/", "https://docs.velociraptor.app/artifact_references/pages/windows.eventlogs.evtxhunter/", "https://docs.velociraptor.app/artifact_references/pages/windows.search.filefinder/", "https://docs.velociraptor.app/artifact_references/pages/windows.sys.startupitems/", "https://docs.velociraptor.app/artifact_references/pages/windows.system.pslist/", "https://docs.velociraptor.app/artifact_references/pages/generic.forensic.timeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triage collection with KAPE and Velociraptor

**Goal:** pull the artefacts that answer most incident questions from one or hundreds of
hosts, rather than imaging full disks.

## KAPE (single host, Windows)
KAPE is a triage program that targets a device or storage location, finds forensically useful artefacts and parses them. Community Targets and Modules live in the KapeFiles repository; update them with `kape.exe --sync` (or the Sync with GitHub button in `gkape.exe`).
- **Targets** (`.tkape`) copy files. `!SANS_Triage` is a compound target that bundles Antivirus, CombinedLogs, EvidenceOfExecution, FileSystem, GroupPolicy, LNKFilesAndJumpLists, RegistryHives, ScheduledTasks, SRUM, WBEM, BITS, WebBrowsers, WindowsTimeline and others.
- **Modules** (`.mkape`) run parsers on what was collected. `!EZParser` is a compound module that runs the Eric Zimmerman parsers (AmcacheParser, AppCompatCacheParser, EvtxECmd, JLECmd, LECmd, MFTECmd, PECmd, RBCmd, RecentFileCacheParser, RECmd, SBECmd, SQLECmd, SrumECmd, SumECmd, WxTCmd).
- Target example from the `!SANS_Triage` file: `kape.exe --tsource c: --tdest <dest> --target CloudStorage_All --sim`. `--tsource` is the source volume, `--tdest` the destination and `--sim` simulates, so you can see the number and size of files a target would return before collecting. Large targets (Recycle Bin data files, Outlook PST/OST, cloud storage user files) are left out of `!SANS_Triage` for that reason.
- For module, Volume Shadow Copy, zip and password flags, see the KAPE manual linked from the KapeFiles README.

## Velociraptor (fleet)
1. Deploy the server and distribute clients. The deployment docs say Velociraptor uses TLS 1.3 by default and that the project prefers distributing MSI packages through package management systems.
2. Pick artifacts by question (documented artifacts below), collect from one host, then widen to a hunt.
3. Results are VQL tables; export them or process them further.

Documented artifacts:
- `Windows.Forensics.Prefetch`: parses `.pf` files for execution history and run counts; on Windows 10 the last 8 execution times plus creation time are visible. Parameters: `dateAfter`, `dateBefore`, `binaryRegex`, `hashRegex`.
- `Windows.EventLogs.EvtxHunter`: searches EVTX files for a regex IOC in message, EventData or UserData. Parameters include `EvtxGlob`, `dateAfter`, `dateBefore`, `IocRegex`, `WhitelistRegex`, `PathRegex`, `ChannelRegex`, `IdRegex` and `SearchVSS`. It can be heavy on the endpoint.
- `Windows.Search.FileFinder`: finds files by glob, inspects content with YARA, hashes and optionally uploads. The docs recommend collecting it with a rate limit of about 20-50 ops per second, because searching content opens and reads every file.
- `Windows.Sys.StartupItems`: startup applications from registry Run keys and Startup folders, with enabled/disabled status from StartupApproved; `AlsoUpload` uploads the startup-folder files.
- `Windows.System.Pslist`: running processes with paths, command lines and optional authenticode and hash; regex parameters filter on process name, PID, path, command line and user.
- `Generic.Forensic.Timeline`: bodyfile-format timeline of files matching a glob (default glob covers the Users folder on the system drive); it does not calculate MD5.

## Choosing what to collect
| Question | Collect |
|---|---|
| What executed? | Prefetch, Amcache, SRUM, event logs (Security 4688 where enabled) |
| Persistence? | Run keys and Startup folders (`Windows.Sys.StartupItems`), scheduled tasks, WMI repository |
| What is running now? | `Windows.System.Pslist` |
| Which hosts hold a file? | `Windows.Search.FileFinder` |

## Gotchas
- Collections contain sensitive data (registry hives, browser data): restrict access to the output.
- Content searches and event-log hunts are heavy on endpoints; rate limit them and test on a few hosts first.
- Treat the Velociraptor server as a remote execution platform and protect it accordingly.

## Verify
- [ ] Collection completes with the expected file count; hash the output archive.
- [ ] Hunt reports results from all targeted clients; investigate clients that did not respond.

## Checked
2026-11-08. Confirmed against the fetched pages: KapeFiles README, `!SANS_Triage.tkape`, `!EZParser.mkape`, the Velociraptor deployment page, and the artifact reference pages for Windows.Forensics.Prefetch, Windows.EventLogs.EvtxHunter, Windows.Search.FileFinder, Windows.Sys.StartupItems, Windows.System.Pslist and Generic.Forensic.Timeline. Removed as unconfirmed (KAPE manual pages are not readable by script; the Velociraptor KapeFiles and hunting pages 404 or are stubs): the full `kape.exe` command line with `--vss`, `--zip`, `--zpw` and module flags, "KAPE copies locked files via raw disk access", the `Windows.KapeFiles.Targets` `_SANS_Triage` workflow, the `velociraptor config client` command, GUI menu paths, hunt resource-limit field names, MFA advice, specific event IDs other than 4688, and the NIST SP 800-86 and Kroll KAPE source labels.
Method: documentation only; no commands were run.
