---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.admin-share-and-smb-file-transfer-artefacts
name: admin-share-and-smb-file-transfer-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [admin-shares, smb, lateral-movement, 5140, 5145, file-transfer, dfir]
level: practitioner
status: draft
description: "Detect admin share use and SMB file transfers between hosts (C$, ADMIN$, tool staging): 5140/5145 events, SMB server logs, $MFT creation and network shares."
sources: ["https://attack.mitre.org/techniques/T1021/002/", "https://jpcertcc.github.io/ToolAnalysisResultSheet/", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-5145"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Admin share and SMB file transfer artefacts

**Goal:** show tools or data were copied over SMB between hosts, including staging of
payloads via `C$`/`ADMIN$` before execution.

## Destination (file server or target host)
- Security **5140** (share accessed: share name, source IP, account) and **5145** (detailed
  file share: relative target name and access mask) with "Audit File Share"/"Detailed File
  Share" enabled.
- Security 4624 type 3 from source.
- `$MFT`/USN: new files written by `System` (PID 4) as SMB server writes appear as kernel
  writes; **creation time** of the copied file = time of copy; modified time may be
  preserved from source.
- `Microsoft-Windows-SMBServer/Security` and `Operational` logs (auth failures, SMB1 use).

## Source host
- `net use \\target\C$` in command history, 4648 explicit credentials, Security 5140 on the
  source if it hosted the share.
- Shellbags/LNK for `\\target\C$\...` UNC paths (interactive Explorer use); `TypedPaths`.
- `Microsoft-Windows-SMBClient/Connectivity` and `Security` logs.

## Pattern recognition
- File copied to `\\host\ADMIN$\` (= `Windows\`) or `C$\ProgramData`, then a service/task/WMI
  execution seconds later = lateral tool transfer and execution.
- Large reads of many files from a file server by one account = collection/staging for
  exfiltration (5145 volume per account).

## Hunt
```kusto
SecurityEvent | where EventID == 5145 and ShareName in ("\\\\*\\C$","\\\\*\\ADMIN$")
| where RelativeTargetName endswith ".exe" or RelativeTargetName endswith ".dll" or RelativeTargetName endswith ".ps1"
```

## Gotchas
- 5145 is very noisy; it is often disabled. NetFlow/Zeek `smb_files.log` is an alternative.
- Copy preserves source modification time: rely on creation time on the destination.

## Verify
5145 write to the file path, $MFT creation time on destination and the source's access
evidence agree within seconds.
