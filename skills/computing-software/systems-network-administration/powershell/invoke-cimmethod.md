---
id: computing-software.systems-network-administration.powershell.invoke-cimmethod
name: invoke-cimmethod
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, cim, cimcmdlets, invoke-cimmethod, wmi-methods, returnvalue, win32-process-create, set-ciminstance]
level: practitioner
status: gated
description: "Call WMI/CIM methods with Invoke-CimMethod: instance vs static methods, argument hashtables, ReturnValue codes, starting remote processes, and Set-CimInstance edits."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/invoke-cimmethod
  - https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/create-method-in-class-win32-process
  - https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/change-method-in-class-win32-service
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Invoke-CimMethod

## Find the method and its parameters
```powershell
(Get-CimClass Win32_Service).CimClassMethods['Change'].Parameters | Select-Object Name, CimType
```
Methods are either **static** (called on the class, e.g. `Win32_Process.Create`; its `Static` qualifier reads `True`) or
**instance** (called on an object, e.g. `Win32_Service.StopService`; no `Static` qualifier).

## Static method: start a process on a remote host
```powershell
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -CimSession $cs -Arguments @{
  CommandLine      = 'cmd.exe /c gpupdate /target:computer /force'
  CurrentDirectory = $null
}
$r | Select-Object PSComputerName, ReturnValue, ProcessId
```
Output is not returned (redirect it to a file, as `cmd /c echo hi > file` did, or use `Invoke-Command`). The Win32_Process.Create
docs say it cannot start an interactive process remotely; a local call here started the process in the caller's session
(SessionId 1), so do not assume session 0 for local calls. Remote calls were not run (no WinRM listener on this machine).

## Instance method: change a service account
```powershell
Get-CimInstance Win32_Service -Filter "Name='MyAppSvc'" -CimSession $cs |
  Invoke-CimMethod -MethodName Change -Arguments @{ StartName = 'AD\svc-myapp'; StartPassword = $plain } |
  Select-Object PSComputerName, ReturnValue
```
- Argument names are case-insensitive (`commandline` worked) and an unknown name fails (`Invalid parameter "Bogus"`);
  per the Win32_Service.Change docs a NULL `StartPassword` means "not changing the password" and an empty string means the
  service has no password.
- Prefer gMSAs (`StartName = 'AD\gmsa-myapp$'`, `StartPassword = ''`) so no password travels (gated: unconfirmed, source is paywalled or blocked).

## Check ReturnValue, always
A method call "succeeds" in PowerShell even when the method fails; the failure is in
`ReturnValue` (a `Win32_Process.Create` of a nonexistent path returned 9; a bad `CurrentDirectory` returned 8). The code
spaces differ per class (Microsoft Learn):

| Code | Win32_Service methods | Win32_Process.Create |
|---|---|---|
| 0 | success (request accepted) | success |
| 2 | access denied | access denied |
| 3 | dependent services running (cannot stop) | insufficient privilege |
| 5 | service cannot accept control | not defined in the docs |
| 8 / 9 | unknown failure / path not found | unknown failure / path not found |
| 10 | service already running | not defined |
| 15 | logon failed (service lacks correct authentication) | not defined |
| 21 | invalid parameter | invalid parameter |
| 22 | invalid service account (invalid or lacks permissions) | other |

```powershell
if ($r.ReturnValue -ne 0) { throw "Create failed on $($r.PSComputerName): $($r.ReturnValue)" }
```

## Editing properties: Set-CimInstance
Only writable properties can be set (see `CimClassProperties` qualifiers `Write`).
```powershell
Get-CimInstance Win32_Volume -Filter "DriveLetter='E:'" | Set-CimInstance -Property @{ Label = 'Data' }
```
The `Write` qualifier query returned `DriveLetter`, `IndexingEnabled` and `Label` for Win32_Volume, so `Label` is writable; the
`Set-CimInstance` call itself was not run (it would rename a real volume) (gated: unconfirmed, source is paywalled or blocked).
For many objects, methods (not property writes) are the supported interface; check the class docs.

## Gotchas
- Pass typed values where the method signature says so: `Win32_Process.Terminate` accepted both `'5'` and `[uint32]5` for its
  uint32 `Reason` here, so casting is a precaution, not a requirement we could demonstrate.
- Embedded-instance parameters take `New-CimInstance -ClientOnly` objects (`ProcessStartupInformation` with a
  `Win32_ProcessStartup` instance worked).
- `Invoke-WmiMethod` argument order was positional and error-prone; `Invoke-CimMethod`
  uses a named hashtable (safer).

## Verify
- [ ] Every call checks `ReturnValue` and reports the computer name on failure.
- [ ] The changed setting reads back correctly with `Get-CimInstance`.

## Checked
Ran on PowerShell 7.6.7 locally (no remote host available): `CimClassMethods['Change'].Parameters`, static
`Win32_Process.Create` (ReturnValue 0, `cmd /c echo hi > file` wrote the file, ProcessId, SessionId 1), bad path (9), bad
directory (8), case-insensitive and unknown argument names, `Terminate` with string and uint32 `Reason`, embedded
`Win32_ProcessStartup`, the `Static` qualifier, the Win32_Volume `Write` qualifier query, and `Get-CimInstance | Invoke-CimMethod`
via `InterrogateService`. The return-code table comes from the Win32_Service.Change and Win32_Process.Create pages on Microsoft
Learn. `Change` on a real service, remote `-CimSession` calls and `Set-CimInstance` on a volume were not run because they alter the system.
