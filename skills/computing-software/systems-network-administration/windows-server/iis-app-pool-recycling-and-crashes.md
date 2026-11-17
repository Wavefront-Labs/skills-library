---
id: computing-software.systems-network-administration.windows-server.iis-app-pool-recycling-and-crashes
name: iis-app-pool-recycling-and-crashes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [iis, app-pool-recycling, w3wp, application-pools, rapid-fail-protection]
level: practitioner
status: docs-checked
description: "Tune IIS application pool recycling, identity and rapid-fail protection, and troubleshoot w3wp crashes and hangs with WAS events, crash dumps and DebugDiag."
sources:
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/applicationpools/add/recycling/
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/applicationpools/add/recycling/periodicrestart
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/applicationpools/add/failure
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/applicationpools/add/processmodel
  - https://learn.microsoft.com/en-us/sysinternals/downloads/procdump
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IIS app pool recycling and w3wp crashes

## Recycling settings
Default `periodicRestart.time` is 29 hours (1740 minutes), so restarts drift through the day. Better: a fixed
off-peak schedule.
```powershell
Import-Module WebAdministration
Set-ItemProperty IIS:\AppPools\AppPool1 -Name recycling.periodicRestart.time -Value '00:00:00'
New-ItemProperty IIS:\AppPools\AppPool1 -Name recycling.periodicRestart.schedule -Value @{value='03:30:00'}
Set-ItemProperty IIS:\AppPools\AppPool1 -Name recycling.logEventOnRecycle -Value 'Time,Requests,Schedule,Memory,IsapiUnhealthy,OnDemand,ConfigChange,PrivateMemory'
```
`logEventOnRecycle` defaults to Time, Requests, Schedule, Memory, IsapiUnhealthy, OnDemand, ConfigChange and
PrivateMemory on IIS 10 and later (Time, Memory, PrivateMemory before). Overlapped recycling is the default;
apps that cannot run two instances at once need `recycling.disallowOverlappingRotation` set to true.
`processModel.idleTimeout` defaults to 20 minutes (`idleTimeoutAction` Terminate, or Suspend on IIS 8.5+). Pools with
slow startup can set idle timeout to 0 and `startMode` to `AlwaysRunning` (default `OnDemand`).

## Identity
ApplicationPoolIdentity (virtual account `IIS AppPool\AppPool1`) has been the default since IIS 7.5 (NetworkService
before). Grant file ACLs to `IIS AppPool\AppPool1`; use a gMSA or domain account for network resources.

## Rapid-fail protection
`failure.rapidFailProtection` stops a pool when `rapidFailProtectionMaxCrashes` (default 5) worker crashes happen
within `rapidFailProtectionInterval` (default 5 minutes); users then get **503** (substatus 503.0, application pool
unavailable: the pool is stopped or disabled). The Windows event log explains why the pool stopped.

## Crash diagnosis
- Capture dumps with a DebugDiag crash rule on w3wp for the pool, or Sysinternals ProcDump: `-ma` full dump,
  `-e` dump on unhandled exception (`-e 1` also first-chance), `-w` wait for the process to start, `-h` dump on a
  hung window. CLR processes are dumped as full dumps anyway. Analyse with DebugDiag Analysis or WinDbg.
- Hangs: take several dumps a few seconds apart and compare blocked threads.

## Verify
- [ ] Recycle events logged at scheduled times only; no repeated crash events after fixes.

## Checked
Date 2026-10-27. Documentation: IIS configuration reference pages for recycling, periodicRestart, failure and
processModel; HTTP status code page (503.0); Sysinternals ProcDump page. Confirmed: defaults above and ProcDump
switches. Windows event IDs for WAS were not confirmed against a page and are not stated.
Method: documentation only; no commands were run.
