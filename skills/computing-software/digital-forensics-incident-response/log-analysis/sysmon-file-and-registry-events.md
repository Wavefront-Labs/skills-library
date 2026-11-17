---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-file-and-registry-events
name: sysmon-file-and-registry-events
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-file-events, sysmon-registry-events, sysmon, event-id-11, event-id-13, file-delete, persistence-detection, dfir]
level: practitioner
status: docs-checked
description: "Use Sysmon file and registry events (2, 11, 12-14, 15, 23, 26, 29) to trace dropped payloads, timestomping, ADS writes, deletions and registry changes."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon file and registry events

**Goal:** reconstruct what a process wrote to disk and the registry, linked back to the
process that did it. Events are in Applications and Services Logs/Microsoft/Windows/Sysmon/Operational
(Vista and higher) with UTC timestamps. Run `sysmon -s` for the exact field names of your
version.

## Event reference (from the Sysmon documentation)
| ID | Filter tag | What it is for |
|---|---|---|
| 2 | FileCreateTime | A process explicitly modified a file creation time; tracks real creation time. Attackers may backdate a backdoor; many processes legitimately do this too, so it is not proof of malice |
| 11 | FileCreate | File created or overwritten; useful for autostart locations such as the Startup folder, and temporary and download directories |
| 12 | RegistryEvent | Registry key and value create and delete |
| 13 | RegistryEvent | Registry value set; records the value written for DWORD and QWORD types |
| 14 | RegistryEvent | Key and value rename; records the new name |
| 15 | FileCreateStreamHash | Named file stream created; hashes both the unnamed and named stream; aimed at browser-attached Zone.Identifier "mark of the web" streams |
| 23 | FileDelete | Deleted file is logged and saved to ArchiveDirectory (default `Sysmon` at the volume root); the directory can grow unreasonably |
| 26 | FileDeleteDetected | Deletion logged without saving the file |
| 29 | FileExecutableDetected | New executable (PE format) file created |
| 27 | FileBlockExecutable | Sysmon detected and blocked creation of executable (PE) files |

Registry root keys appear abbreviated: HKEY_LOCAL_MACHINE as HKLM, HKEY_USERS as HKU,
HKEY_LOCAL_MACHINE\System\ControlSet00x as HKLM\System\CurrentControlSet, and
HKEY_LOCAL_MACHINE\Classes as HKCR.

## Config notes
- Events 12-14 share the `RegistryEvent` tag; 23, 26, 29 use `FileDelete`, `FileDeleteDetected`
  and `FileExecutableDetected`.
- Preserving deleted files is controlled by config entries: `ArchiveDirectory`, `CopyOnDeletePE`
  (default False), `CopyOnDeleteSIDs`, `CopyOnDeleteExtensions`, `CopyOnDeleteProcesses`. The
  archive directory is protected by a System ACL (the page suggests `psexec -sid cmd` to reach it).
- Rule logic: `onmatch` of include or exclude; excludes take precedence; rules on the same
  field are ORed, different fields ANDed.

## Using the events
Pivot from a file or registry event to the writing process through its ProcessGuid, then to
that process's creation event (Event ID 1), which carries the full command line and hashes.
Review Event 2 outside of installers and updaters; look at file creates in autostart and
temporary locations and at registry changes in autostart locations, which the documentation
names as the use of events 11 and 12.

## Self-check
For each dropped file or registry change you report the writing process, the time (UTC), the
path or value, and hashes where available.

## Checked
2026-11-09. Confirmed on the Sysmon page (read in full): event descriptions for 2, 11-15, 23, 26, 27, 29, filter tags, registry abbreviations, CopyOnDelete and ArchiveDirectory entries, rule logic, log location, UTC. Removed: field lists per event, specific hunt paths and registry keys, the Defender-exclusion/WDigest/RDP and ransomware hunts, Sysmon 15+ version claim, HKCU-as-HKU\SID claim, the sysmon-modular and SwiftOnSecurity sources (config repos, not read).
Method: documentation only; no commands were run.
