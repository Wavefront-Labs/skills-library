---
id: computing-software.systems-network-administration.windows-server.defender-antivirus-on-servers
name: defender-antivirus-on-servers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, os-hardening, windows-server-hardening, defender-antivirus, mpcmdrun, passive-mode, av-exclusions, set-mppreference, server-role-exclusions]
level: practitioner
status: docs-checked
description: "Run Microsoft Defender Antivirus on Windows Server: install, automatic role exclusions, custom exclusions, passive mode with third-party AV, MpCmdRun scans and updates."
sources:
  - https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-on-windows-server
  - https://learn.microsoft.com/en-us/defender-endpoint/configure-server-exclusions-microsoft-defender-antivirus
  - https://learn.microsoft.com/en-us/defender-endpoint/command-line-arguments-microsoft-defender-antivirus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft Defender Antivirus on servers

## Install
Defender Antivirus is installed and enabled by default on Windows Server 2016 and later. To reinstall:
```powershell
Install-WindowsFeature -Name Windows-Defender
```
The optional user interface (feature `Windows-Defender-GUI`, Server 2016) needs the Desktop Experience install option;
it is not available on Server Core. PowerShell and Group Policy work without it.

## Passive mode with another AV
To run Defender Antivirus in passive mode next to a non-Microsoft AV, apply the `ForceDefenderPassiveMode` value of 1
(0 returns it to active); Learn's page gives the registry location. With tamper protection on, once Defender has
been toggled to active mode, tamper protection prevents it going back to passive even with the value 1.
Never run two active real-time engines.

## Exclusions
- Built-in exclusions (OS files) and automatic exclusions for server roles on Server 2016 and later are delivered
  through security intelligence updates, with no configuration. They do not appear in the Windows Security app's
  exclusion lists. The exclusions page lists them per role (for example File Replication Service).
- Add application-specific exclusions from vendor guidance (SQL data/log files, backup repositories):
```powershell
Add-MpPreference -ExclusionPath '<vol>:\SQLData' -ExclusionExtension 'mdf','ldf','ndf'
Add-MpPreference -ExclusionProcess 'sqlservr.exe'
Get-MpPreference | Select ExclusionPath,ExclusionProcess,ExclusionExtension
```
Keep exclusions narrow; folder exclusions are the attacker's favourite hiding place. Prefer central policy (GPO or
Intune) over local edits.

## MpCmdRun
```powershell
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -SignatureUpdate
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -Scan -ScanType 2     # full scan (Learn's example)
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -GetFiles             # collect support logs
```
`-RemoveDefinitions` restores the previous set of signature definitions (see the page for `-All` and options).
Equivalent cmdlets: `Update-MpSignature`, `Start-MpScan`, `Get-MpThreatDetection`.

## Performance
High CPU from MsMpEng on file servers: run `New-MpPerformanceRecording -RecordTo <file.etl>` while it happens, then
`Get-MpPerformanceReport -Path <file.etl> -TopFiles <n>` to find what to examine for exclusion.

## Verify
- [ ] Security intelligence is current on every server (use your fleet reporting).
- [ ] Mode matches design (active unless a third-party AV is primary).

## Checked
2026-10-28. Confirmed on Learn pages (Defender AV on Windows Server, server exclusions, MpCmdRun command line,
performance tuning, Start-MpScan/Update-MpSignature/Get-MpThreatDetection): default install on 2016+,
Install-WindowsFeature names, ForceDefenderPassiveMode 1/0 and tamper protection behaviour, automatic exclusions,
MpCmdRun -SignatureUpdate/-Scan -ScanType/-GetFiles/-RemoveDefinitions, performance recording and report.
Removed as unconfirmed: Get-MpComputerStatus properties and AMRunningMode values, claim that servers never go passive
automatically, DisableLocalAdminMerge, the `-DynamicSignatures` option, quick-scan type number, `-TopProcesses`,
the 24-hour signature age, the role list for automatic exclusions.
Method: documentation only; no commands were run.
