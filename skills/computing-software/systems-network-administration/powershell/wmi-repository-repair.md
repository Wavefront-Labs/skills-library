---
id: computing-software.systems-network-administration.powershell.wmi-repository-repair
name: wmi-repository-repair
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, cim, wmi-repository, winmgmt, wmi-troubleshooting, mofcomp, wmi-activity-log]
level: advanced
status: docs-checked
description: "Diagnose and repair a broken WMI repository safely: verify and salvage with winmgmt, re-register providers, read WMI error codes, and avoid destructive resets."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/wmisdk/winmgmt
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/scenario-guide-troubleshoot-wmi-connectivity-access-issues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WMI repository troubleshooting

Most WMI errors are **not** repository corruption. Microsoft's winmgmt page warns that errors seen
through WMI may come from other parts of the operating system, and not to delete the WMI
repository as a first action because it can damage the system or installed applications. Rule out
connectivity, permissions and a single bad provider first.

## 1. Triage
```powershell
Get-CimInstance Win32_OperatingSystem            # does the core work?
Get-WinEvent -LogName Microsoft-Windows-WMI-Activity/Operational -MaxEvents 50 |
  Where-Object LevelDisplayName -eq 'Error' | Select-Object TimeCreated, Id, Message
```
Incoming access and core WMI errors are logged in `Microsoft-Windows-WMI-Activity/Operational`.
`wmimgmt.msc` > WMI Control > Properties checks local WMI connectivity; local failures such as
`WMI: Not Found` or `WMI: Generic failure` can come from repository glitches or corruption.

| Error | Meaning (Microsoft's guide) |
|---|---|
| 0x800706BA, 0x80041015 | connectivity: RPC server unavailable, network error (firewall, RPC, DCOM) |
| 0x80070005, 0x80041003 | access: denied by DCOM security, or by a provider/namespace |
| 0x80041002 | WBEM_E_NOT_FOUND |
| 0x8004100E | invalid namespace |
| 0x80041010 | invalid class |
| 0x80041011, 0x80041012, 0x80041013 | provider not found, invalid registration, load failure |
| 0x80041004 | provider failure |

## 2. Check repository consistency (non-destructive)
Elevated:
```
winmgmt /verifyrepository
```
Without a path it verifies the live repository; with a full path to a saved copy of the entire
repository folder it verifies that copy. An inconsistent repository returns
`ERROR_INTERNAL_DB_CORRUPTION` (1358). If it is consistent, stop and look at providers,
permissions and connectivity instead.

## 3. Salvage if inconsistent
```
winmgmt /salvagerepository
winmgmt /verifyrepository
```
`/salvagerepository` checks consistency and, if inconsistent, rebuilds the repository, merging in
the old content where it can be read. MOF files with `#pragma autorecover` are restored.

`winmgmt /resetrepository` resets the repository to its state when the operating system was first
installed (autorecover MOFs are restored). Everything gathered since is lost, and rebuilding has
left some third-party products broken until their setup was re-run and their MOF re-added.
Microsoft's guide does not recommend rebuilding the repository unless Microsoft support does it.
Back up first with `winmgmt /backup <filename>` (needs the full path; it takes a write lock on
the repository while it runs).

## 4. Re-register providers and recompile MOFs
Elevated, the procedure in Microsoft's guide (it restarts the WMI service):
```
sc config winmgmt start= disabled
net stop winmgmt /y
cd %windir%\system32\wbem
for /f %s in ('dir /b *.dll') do regsvr32 /s %s
sc config winmgmt start= Auto
net start winmgmt
dir /b *.mof *.mfl | findstr /v /i uninstall > moflist.txt & for /F %s in (moflist.txt) do mofcomp %s
```
Note the filter that leaves out `uninstall` MOFs, which remove classes. (In a batch file, double
the `%` signs.)

## 5. Permissions for remote access
- By default only members of Administrators can access the WMI namespace remotely.
- Namespace access: `wmimgmt.msc` > WMI Control > Properties > Security tab > select the
  namespace (root\cimv2 is the default) > Security, then allow **Remote Enable** and **Read
  Security**. A user without it gets 0x80041003. Use Advanced > "This namespace and
  subnamespaces" to inherit it.
- DCOM: `dcomcnfg` > My Computer > COM Security > Launch and Activation Permissions > Edit Limits,
  allow Remote Launch and Remote Activation. Alternatively add the user to the local Distributed
  COM Users group.
- Windows Firewall needs the Windows Management Instrumentation (WMI) rule group enabled on the
  target.

## Verify
- [ ] `winmgmt /verifyrepository` reports no inconsistency.
- [ ] The originally failing query succeeds locally and remotely.
- [ ] No new errors in WMI-Activity/Operational after the fix.

## Checked
2026-11-09. Read in full: Microsoft Learn winmgmt reference and the "Scenario guide: Troubleshoot
WMI connectivity and access issues". Confirmed the verify, salvage, reset and backup switches,
autorecover behaviour, error codes, the log name, the provider and MOF re-registration steps,
Remote Enable and DCOM permission steps and the default administrators-only access. Removed as
unconfirmed: the Techcommunity 2009 blog source (Microsoft marks it no longer valid), the
WmiPrvSE event 5857/5858 advice, the storage namespace query, cimwin32.mof and autorecover
registry details, the SCCM note, and the table of symptoms to causes.

Method: documentation only; no commands were run.
