---
id: computing-software.cybersecurity-defensive.security-operations.lolbin-hunting
name: lolbin-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, lolbin-hunting, lolbas, living-off-the-land, command-line-analysis, sysmon, edr]
level: practitioner
status: docs-checked
description: "Hunt for living-off-the-land binary abuse: LOLBAS-listed command patterns for rundll32, regsvr32, mshta, certutil, msbuild and more, with baselines to cut noise."
sources: ["https://lolbas-project.github.io/", "https://lolbas-project.github.io/lolbas/Binaries/Certutil/", "https://lolbas-project.github.io/lolbas/Binaries/Regsvr32/", "https://lolbas-project.github.io/lolbas/Binaries/Mshta/", "https://lolbas-project.github.io/lolbas/Binaries/Rundll32/", "https://lolbas-project.github.io/lolbas/Binaries/Bitsadmin/", "https://lolbas-project.github.io/lolbas/Binaries/Msbuild/", "https://lolbas-project.github.io/lolbas/Binaries/Wmic/", "https://attack.mitre.org/techniques/T1218/", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Living-off-the-land binary hunting

**Goal:** catch attackers using signed Windows binaries (LOLBins) to download, execute or
bypass controls, by looking at how they are invoked rather than whether they ran. ATT&CK
T1218 (System Binary Proxy Execution) describes the idea: signed or otherwise trusted
binaries, often Microsoft-signed and native to Windows, proxy execution of malicious content
to bypass process and signature-based defences.

## Prerequisites
Process creation telemetry with full command lines and the parent process (EDR, Sysmon
process creation, or Windows process-creation auditing with command-line logging). Sysmon
Event ID 1 is "Process creation".

## Patterns the LOLBAS project lists per binary
Command shapes below are the examples on each LOLBAS binary page. Hunt for the shape, not the
exact string; the project lists many more binaries (the index lists well over a hundred).

| Binary | LOLBAS functions | Command shape on its LOLBAS page |
|---|---|---|
| `rundll32.exe` | Execute (DLL, Remote, JScript, COM), alternate data streams | `rundll32.exe <dll>,EntryPoint` (any file extension accepted); DLL on an SMB share; `javascript:` argument calling `GetObject("script:<url>")`; `-sta <CLSID>` to load a COM server; a DLL in an NTFS alternate data stream |
| `regsvr32.exe` | AWL bypass and Execute (SCT, Remote, DLL) | `/s /n /u /i:<url>.sct scrobj.dll`; `/s /u /i:<path>.sct scrobj.dll`; `/s <dll>` (runs `DllRegisterServer`) or `/u /s <dll>` (`DllUnRegisterServer`) |
| `mshta.exe` | Execute (HTA, Remote, VBScript, JScript), alternate data streams, download to INetCache | `mshta.exe <file>.hta`; `vbscript:` or `javascript:` argument with `GetObject("script:<url>")`; a bare remote URL (payload lands in INetCache) |
| `certutil.exe` | Download, alternate data streams, encode, decode | `-urlcache -f <url> <file>`; `-verifyctl -f <url> <file>`; `-URL <url>` (GUI); `-encode`, `-decode`, `-decodehex` |
| `bitsadmin.exe` | Download, copy, execute, alternate data streams | `/create`, `/addfile <url> <file>`, `/SetNotifyCmdLine`, `/RESUME`, `/complete` chained in one command line |
| `msbuild.exe` | AWL bypass and Execute (C#, DLL, XSL, CMD) | building an XML, `.csproj` or `.proj` file; `/logger:TargetLogger,<dll>;...`; `@<file>.rsp` (response file used to bypass command-line detections) |
| `wmic.exe` | Execute (CMD, remote, XSL, discovery, antivirus enumeration), copy, alternate data streams | `process call create "<cmd>"`; `/node:"<host>" process call create`; `process get brief /format:"<url or SMB path>.xsl"`; `/Namespace:\\root\SecurityCenter2 Path AntiVirusProduct` |
| `installutil.exe`, `regasm.exe`, `cmstp.exe` | AWL bypass and Execute (.NET DLL or EXE; INF and DLL for cmstp) | see each binary's page |

The LOLBAS pages for certutil, regsvr32, mshta, rundll32, bitsadmin, msbuild and wmic each
list detection pointers, including Sigma rules; the LOLBAS pages themselves name the rule
files, and the Sigma `rules/windows/process_creation` folder holds the process-creation ones.
The pages also list IOCs worth hunting, for example: certutil creating new files on disk;
regsvr32 retrieving files from the Internet or executing `.sct` files; mshta making a network
connection or running raw script on its command line; rundll32 making outbound network
connections or using flags such as `-sta`; bitsadmin spawning child processes; msbuild.exe
being run at all on a workstation.

## Query sketch (Defender advanced hunting)
```kql
DeviceProcessEvents
| where FileName in~ ("certutil.exe","regsvr32.exe","mshta.exe","rundll32.exe","bitsadmin.exe","msbuild.exe","wmic.exe")
| where ProcessCommandLine has_any ("urlcache","verifyctl","http","scrobj","javascript:","vbscript:","/transfer","/addfile","process call create","/format")
| summarize count(), hosts=dcount(DeviceName) by FileName, InitiatingProcessFileName, ProcessCommandLine
| order by hosts asc
```
`FileName`, `ProcessCommandLine`, `InitiatingProcessFileName` and `DeviceName` are columns of
the `DeviceProcessEvents` table. Pair with stack counting: rare command lines and rare
parent-child pairs. Equivalent SIEM queries on Sysmon Event ID 1 use the same strings.

## Baseline then hunt
Run the queries over a representative window (for example 30 days), note legitimate patterns
(software installers, management agents, IT scripts), document them, then focus on what
remains. Renamed binaries: `DeviceProcessEvents` has `ProcessVersionInfoOriginalFileName`
("original file name from the version information of the newly created process"), so match on
it as well as `FileName`.

## Gotchas
- Many LOLBins are used legitimately by IT tooling; filter by parent process and its signer.
- ATT&CK T1218 lists application control (M1038), disabling or removing unneeded binaries
  (M1042) and restricting execution to the accounts that need it (M1026) as mitigations;
  application control and block rules beat hunting alone. The LOLBAS pages for mshta,
  msbuild and wmic link Microsoft's recommended block rules.
- Command-line obfuscation defeats naive string matches; use case-insensitive matching and
  check variants (for example `msbuild.exe @file.rsp` hides the options from the command line).

## Verify
Run a few LOLBAS example commands on a lab host (the regsvr32 LOLBAS page links the Atomic Red
Team T1218.010 tests) and confirm each surfaces in the hunt queries.

## Checked
2026-11-08. Confirmed against the LOLBAS index and the certutil, regsvr32, mshta, rundll32,
bitsadmin, msbuild and wmic binary pages (functions, command shapes, IOCs, detection pointers),
ATT&CK T1218 (definition, mitigations M1038/M1042/M1026), the Sysmon page (Event ID 1) and the
Defender `DeviceProcessEvents` table page (column names, original file name). Removed: the
Splunk sketch and `OriginalFileName` Sysmon claim (not on the cited pages), powershell.exe row
and its flags (not a LOLBAS binary page checked), claims that installutil/regasm/cmstp are
suspicious "from user-writable paths", and the generic WDAC claim. The Sigma process_creation
tree page lists rule folders only; individual rules were not read.
Method: documentation only; no commands were run.
