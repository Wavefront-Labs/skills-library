---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.bam-dam-execution-evidence
name: bam-dam-execution-evidence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [bam-dam, evidence-of-execution, program-execution, system-hive, windows-forensics, dfir]
level: practitioner
status: draft
description: "Use BAM and DAM (Background Activity Moderator) registry entries as evidence of program execution per user with last execution times on Windows 10 and 11."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://ericzimmerman.github.io/", "https://github.com/keydet89/RegRipper3.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BAM/DAM execution evidence

**Goal:** get per-user last-run times for executables from the Background Activity
Moderator, a Windows 10 (1709+) and 11 artefact.

## Location
SYSTEM hive: `ControlSet00N\Services\bam\State\UserSettings\<SID>` (older builds:
`Services\bam\UserSettings\<SID>`), and `Services\dam\...` for Desktop Activity Moderator.
Each value name is a full device path, e.g.
`\Device\HarddiskVolume3\Users\jdoe\AppData\Local\Temp\a.exe`; data starts with an
8-byte FILETIME = **last execution time (UTC)**.

## Parse
Registry Explorer (BAM bookmark/plugin), RECmd batch, RegRipper `bam` plugin.
Map `HarddiskVolumeN` to drive letters using `MountedDevices` and the volume layout.

## Interpretation
- Shows executables run by the user (SID) with the last run time; good for attributing
  execution to an account.
- Entries for some executables are cleaned up after about 7 days of inactivity at boot
  (observed behaviour), so absence does not mean never run.
- Records programs in background-throttled scenarios; console tools run from cmd may or may
  not appear, depending on how they ran.
- On recent Windows 11 builds BAM recording has been observed to change; confirm on a
  reference system of the same build.

## Use with
Prefetch (run count, eight last runs), Amcache (SHA-1, first run), ShimCache (existence),
UserAssist (GUI launches), 4688 events.

## Verify
Pick a known program the user ran and confirm its BAM time matches Prefetch last run time
within seconds, establishing reliability on that system.
