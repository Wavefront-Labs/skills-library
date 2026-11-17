---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.software-hive-analysis
name: software-hive-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [software-hive, windows-registry, installed-programs, network-profiles, profilelist, dfir]
level: practitioner
status: draft
description: "Analyse the SOFTWARE hive: OS version and install date, installed programs, profile list, network history, Run keys, and scheduled task cache."
sources: ["https://ericzimmerman.github.io/", "https://www.sans.org/posters/windows-forensic-analysis/", "https://github.com/keydet89/RegRipper3.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOFTWARE hive analysis

**Goal:** extract system-wide configuration and history: what OS, what was installed, which
users had profiles, which networks the machine joined, and machine-wide autostarts. Hive:
`Windows\System32\config\SOFTWARE`.

## Key locations
| Fact | Key |
|---|---|
| OS version, build, install date | `Microsoft\Windows NT\CurrentVersion` (`ProductName`, `CurrentBuild`, `DisplayVersion`, `InstallDate` Unix time, `InstallTime` FILETIME, `RegisteredOwner`) |
| User profiles | `Microsoft\Windows NT\CurrentVersion\ProfileList\<SID>` (`ProfileImagePath`, `LocalProfileLoadTimeHigh/Low`); key last write approximates profile creation |
| Installed programs | `Microsoft\Windows\CurrentVersion\Uninstall\*` and `WOW6432Node\...` (`DisplayName`, `InstallDate`, `InstallLocation`) |
| Network history | `Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\{GUID}` (`ProfileName`, `DateCreated`, `DateLastConnected` as SYSTEMTIME, `NameType` 6 wired/71 wireless/23 VPN) and `...\Signatures\Unmanaged|Managed` (gateway MAC `DefaultGatewayMac`) |
| Autostart | `Microsoft\Windows\CurrentVersion\Run`, `RunOnce`, `Policies\Explorer\Run`, `Microsoft\Windows NT\CurrentVersion\Winlogon` (`Shell`, `Userinit`), `Image File Execution Options` (Debugger) |
| Scheduled tasks | `Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree` and `Tasks` |
| Defender exclusions | `Microsoft\Windows Defender\Exclusions\Paths|Processes|Extensions` |

## Tools
Registry Explorer bookmarks; RegRipper `winver`, `profilelist`, `uninstall`, `networklist`,
`run`, `winlogon`, `tasks`; RECmd `Kroll_Batch`.

## What to look for
Remote access tools installed during the incident (AnyDesk, ScreenConnect, Atera), Defender
exclusions added by attackers, Winlogon `Userinit` with extra entries, IFEO debugger
hijacks, tasks in TaskCache with no matching XML (hidden tasks).

## Verify
Installed-program dates match Amcache/Prefetch first-run evidence; network profile times
are interpreted as local time (SYSTEMTIME values are local, not UTC).
