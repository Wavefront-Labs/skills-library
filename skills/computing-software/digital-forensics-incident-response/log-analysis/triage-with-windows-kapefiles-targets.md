---
id: computing-software.digital-forensics-incident-response.log-analysis.triage-with-windows-kapefiles-targets
name: triage-with-windows-kapefiles-targets
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [kapefiles-targets, velociraptor, kape-targets, triage-collection, windows-triage-targets, dfir]
level: practitioner
status: draft
description: "Collect Windows triage packages with Velociraptor's Windows.KapeFiles.Targets (and successor Windows.Triage.Targets): choosing target groups, VSS options, upload limits and processing."
sources: ["https://github.com/EricZimmerman/KapeFiles", "https://docs.velociraptor.app/docs/offline_triage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triage with Windows.KapeFiles.Targets

`Windows.KapeFiles.Targets` is a Velociraptor artifact generated from the community KapeFiles target definitions. It collects the same files KAPE would (registry hives, event logs, `$MFT`, prefetch, browser data...) using Velociraptor's raw NTFS accessor, from one host or a whole hunt, without needing a KAPE licence. Newer Velociraptor releases introduce `Windows.Triage.Targets` as the maintained successor; prefer it where available, with the same concepts.

## Choosing what to collect
Targets are boolean parameters; compound targets bundle many:
- `_SANS_Triage` / `KapeTriage`: broad incident triage (hives, event logs, `$MFT`, `$LogFile`, `$J`, prefetch, Amcache, SRUM, LNK/jump lists, browser history, scheduled tasks, WER, PowerShell history).
- `_BasicCollection`: smaller core set.
- Specific targets: `EventLogs`, `RegistryHives`, `$MFT`, `WebBrowsers`, `RDPCache`, `Antivirus`, `CloudStorage_*` etc.
Start narrow on large hunts (hives + event logs + `$MFT`), then expand on hosts of interest.

## Key parameters
- `Device` (e.g. `C:`), or all drives where supported.
- `VSSAnalysisAge`: collect from Volume Shadow Copies newer than N days (0 = none). Valuable but multiplies size and time.
- `UseAutoAccessor`: tries normal file access first, raw NTFS for locked files.
- Resource limits on the collection: max upload bytes, max rows, timeout, CPU limit. Triage with `$MFT` and VSS can exceed default byte limits; raise them per collection.

## Running
- Single host: Collect > select artifact > set targets > Launch. Monitor the flow's uploads and logs.
- Fleet: create a hunt targeted by label or OS, with conservative targets and CPU limits.
- Offline: build an offline collector (Server.Utils.CreateCollector or GUI "Build offline collector") with the same targets for hosts without agents.

## Processing results
Download the flow's collection zip (uploads preserve paths). Process with EZ Tools / KAPE modules (`--msource` pointed at the extracted tree), Plaso, or Velociraptor's own parsing artifacts (`Windows.EventLogs.EvtxHunter`, `Windows.Forensics.Prefetch`) run on the client instead of copying files.

## Gotchas
- Huge collections across many hosts can fill the server's disk; estimate size (a full triage can be several GB per host with VSS) and use remote upload targets for scale.
- Target definitions are frozen at the Velociraptor build; update the server to get new KapeFiles targets.
- Collecting users' browser data and documents carries privacy implications; scope targets to the investigation.

## Verify
The flow completed without upload-limit errors, the expected hives and `$MFT` are present in the download with their paths, and the collection zip's hash is recorded.
