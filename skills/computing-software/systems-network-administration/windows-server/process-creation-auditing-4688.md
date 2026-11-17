---
id: computing-software.systems-network-administration.windows-server.process-creation-auditing-4688
name: process-creation-auditing-4688
category: computing-software
field: systems-network-administration
product: windows-server
tags: [security-auditing, event-4688, process-command-line-auditing, threat-hunting, advanced-audit-policy]
level: practitioner
status: docs-checked
description: "Enable process creation auditing with command lines (event 4688), size the Security log, and hunt for encoded PowerShell, LOLBins and odd parent processes."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process creation auditing (4688)

## Enable
1. Advanced Audit Policy > Detailed Tracking > **Audit Process Creation** = Success.
2. Computer > Administrative Templates > System > Audit Process Creation > **Include command line in process creation
   events** = Enabled.
3. Raise the Security log size (command lines are long), or forward the events.

## Event fields
`NewProcessName`, `CommandLine`, `ParentProcessName`, `SubjectUserName`, `TokenElevationType`
(`%%1937` = elevated full token), `MandatoryLabel`.

## Hunts
```powershell
$ev = Get-WinEvent -FilterHashtable @{LogName='Security';Id=4688;StartTime=(Get-Date).AddDays(-1)}
$ev | ForEach-Object { $x=[xml]$_.ToXml(); $d=@{}; $x.Event.EventData.Data | % { $d[$_.Name]=$_.'#text' }
  [pscustomobject]@{Time=$_.TimeCreated;User=$d.SubjectUserName;Parent=$d.ParentProcessName;Proc=$d.NewProcessName;Cmd=$d.CommandLine} } |
  Where-Object { $_.Cmd -match '-enc|-encodedcommand|FromBase64String|DownloadString|IEX|certutil.*-urlcache|bitsadmin|mshta|regsvr32.*/i:http|rundll32.*javascript' }
```
Also look for: Office or w3wp.exe spawning cmd/powershell, `wmiprvse.exe` spawning shells (remote WMI execution),
`services.exe` starting random binaries in temp paths, `ntdsutil` or `vssadmin create shadow` on DCs.

## Sensitive data caution
Command lines can contain passwords passed as arguments (bad scripts). Restrict who can read Security logs and the
SIEM index; fix the scripts.

## Complement
Sysmon process-creation events add hashes and more context; PowerShell script block logging shows what encoded
commands actually ran.

## Verify
- [ ] A recent 4688 event shows a populated CommandLine.

## Checked
2026-10-28. Confirmed on the Learn 4688 and command-line-auditing pages: Audit Process Creation subcategory (Detailed Tracking),
the "Include command line in process creation events" policy and its path, empty CommandLine by default, the field
names, `%%1937` as the elevated full token. Removed as unconfirmed: the 1 GB log size, the 2016+ gate for
ParentProcessName, event numbers for Sysmon and script block logging.
Method: documentation only; no commands were run.
