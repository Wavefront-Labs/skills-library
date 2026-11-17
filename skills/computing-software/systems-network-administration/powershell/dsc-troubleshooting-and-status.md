---
id: computing-software.systems-network-administration.powershell.dsc-troubleshooting-and-status
name: dsc-troubleshooting-and-status
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-dsc, dsc-troubleshooting, get-dscconfigurationstatus, lcm, xdscdiagnostics]
level: advanced
status: docs-checked
description: "Troubleshoot DSC (v1.1): Get-DscConfigurationStatus, DSC event logs, resource module caching and DebugMode to find failing resources."
sources:
  - https://learn.microsoft.com/en-us/powershell/dsc/troubleshooting/troubleshooting?view=dsc-1.1
  - https://learn.microsoft.com/en-us/powershell/module/psdesiredstateconfiguration/get-dscconfigurationstatus?view=dsc-1.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot DSC

## Is the node compliant, and what failed?
```powershell
Get-DscConfigurationStatus -CimSession WEB01
(Get-DscConfigurationStatus -CimSession WEB01).ResourcesNotInDesiredState
Get-DscConfigurationStatus -All    # history of runs
```
`Get-DscConfigurationStatus` returns an object describing whether the last configuration run succeeded; dig into it
(for example `ResourcesNotInDesiredState`) for the failing resources.

## Event logs
DSC writes mainly to three logs: Operational, Analytic and Debug. Analytic and Debug are not enabled by default. The
channels are `Microsoft-Windows-Dsc/Analytic` and `Microsoft-Windows-Dsc/Debug`. Enable them in Event Viewer (View >
Show Analytic and Debug Logs) or with wevtutil:
```cmd
wevtutil.exe set-log "Microsoft-Windows-Dsc/Analytic" /q:true /e:true
wevtutil.exe set-log "Microsoft-Windows-Dsc/Debug" /q:true /e:true
```
The xDscDiagnostics module (`Trace-xDscOperation`) aggregates events from the Analytic, Debug and Operational logs and
prompts you to enable them. The DSC Log resource can write progress into the Analytic log while authoring.

## Resource module caching
After you change a resource module, the engine can keep running the cached copy until the host process is stopped and
restarted. While developing a resource, set the LCM `DebugMode` to `ForceModuleImport` so the engine always reloads the
resource; set it back when finished so caching resumes.

## Verify
- [ ] The latest `Get-DscConfigurationStatus` result shows success and `ResourcesNotInDesiredState` is empty.

## Checked
2026-11-09. Read in full the Learn DSC 1.1 troubleshooting page and the Get-DscConfigurationStatus reference.
Confirmed: Get-DscConfigurationStatus, -All, ResourcesNotInDesiredState, the Operational/Analytic/Debug logs and
their channel names, the wevtutil enable commands, xDscDiagnostics, DebugMode ForceModuleImport and the cache
behaviour. Removed as unconfirmed: Test-DscConfiguration -Detailed, LCMState and Pending.mof handling,
Stop-DscConfiguration, Start-DscConfiguration -UseExisting, the ConfigurationStatus JSON folder, PendingReboot, and
the missing-module and credential-mismatch causes.
Method: documentation only; no commands were run.
