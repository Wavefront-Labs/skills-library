---
id: computing-software.systems-network-administration.powershell.execution-policy-scopes
name: execution-policy-scopes
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-security, executionpolicy, execution-policy-scopes, set-executionpolicy, remotesigned, allsigned, zone-identifier, unblock-file]
level: practitioner
status: verified
description: "Set PowerShell execution policy correctly: the five scopes and precedence, GPO control, RemoteSigned and Mark of the Web, Unblock-File, and why it is not a security boundary."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Execution policy scopes

Execution policy is a **safety feature to stop accidental script runs**, not a security
control: any user can bypass it (`pwsh -ExecutionPolicy Bypass -File x.ps1`, or paste the
content). Enforce real control with WDAC/AppLocker plus constrained language mode.

## Policies
| Policy | Runs |
|---|---|
| `Restricted` | no scripts (Windows client default) |
| `AllSigned` | only scripts signed by a trusted publisher; prompts for new publishers |
| `RemoteSigned` | local scripts; downloaded (Mark of the Web) scripts must be signed. Windows Server default (the PowerShell 7 zip build also ships a `powershell.config.json` in `$PSHOME` setting it) |
| `Unrestricted` | all; prompts before running scripts not from the local intranet zone (non-Windows default). The prompt waits for input, so a non-interactive `-File` run of a downloaded script hangs |
| `Bypass` | everything, no warnings |
| `Undefined` | no policy at this scope |

## Scopes, highest precedence first
| Scope | Set by | Stored |
|---|---|---|
| `MachinePolicy` | GPO Computer Configuration > Administrative Templates > Windows Components > Windows PowerShell > Turn on Script Execution | registry policy key |
| `UserPolicy` | GPO User Configuration (same path) | registry policy key |
| `Process` | `-ExecutionPolicy` on the command line or `Set-ExecutionPolicy -Scope Process` | `$env:PSExecutionPolicyPreference` |
| `CurrentUser` | `Set-ExecutionPolicy -Scope CurrentUser` | HKCU (5.1) / `powershell.config.json` in the user profile (PS 7) |
| `LocalMachine` | `Set-ExecutionPolicy` (default scope, admin) | HKLM (5.1) / `$PSHOME\powershell.config.json` (PS 7) |

```powershell
Get-ExecutionPolicy -List                  # shows every scope; effective = first non-Undefined
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Set-ExecutionPolicy Bypass -Scope Process -Force   # this session only
```
- GPO scopes (MachinePolicy, UserPolicy) are first in the precedence list in about_Execution_Policies, so they beat
  `-ExecutionPolicy Bypass`; `Set-ExecutionPolicy -Scope MachinePolicy` is refused because Group Policy owns it.
- Windows PowerShell 5.1 and PowerShell 7 keep **separate** settings; set both (on the test machine `LocalMachine` was
  `Unrestricted` in 5.1 and `RemoteSigned` in 7.6.7). PS 7 has GPO templates of its own (`InstallPSCorePolicyDefinitions.ps1`
  and `PowerShellCoreExecutionPolicy.admx` sit in `$PSHOME`).
- Scheduled tasks: put `-ExecutionPolicy Bypass` (or `RemoteSigned`) in the task arguments
  instead of loosening the machine policy, unless GPO forbids it.

## Mark of the Web and Unblock-File
Files downloaded by browsers, Outlook, or extracted from downloaded ZIPs by Explorer carry
an NTFS `Zone.Identifier` stream (ZoneId=3). Under `RemoteSigned` they fail with
"is not digitally signed".
```powershell
Get-Item .\tool.ps1 -Stream Zone.Identifier -ErrorAction SilentlyContinue
Get-ChildItem .\module -Recurse | Unblock-File     # after you have reviewed the content
```
Files from UNC paths in the Internet zone are treated as remote too; add the server to the
Local intranet zone if that is wrong.

## Verify
- [ ] `Get-ExecutionPolicy -List` shows the intended policy at MachinePolicy on managed servers.
- [ ] A test downloaded unsigned script is blocked; a signed one runs.

## Checked
Ran on 5.1.26100 and 7.6.7: `Get-ExecutionPolicy -List`; a script given a `Zone.Identifier` stream (ZoneId=3) with
`powershell -ExecutionPolicy RemoteSigned|AllSigned|Restricted|Bypass -File` (RemoteSigned and AllSigned: "is not
digitally signed"; Restricted: scripts disabled; Bypass: ran); `Unblock-File` removed the stream and RemoteSigned then ran
the file; `Unrestricted` on that MOTW file blocked on an interactive prompt (killed); `$env:PSExecutionPolicyPreference`
holds the Process scope and `Set-ExecutionPolicy Bypass -Scope Process` set it; the PS 7 `$PSHOME\powershell.config.json`
LocalMachine setting (and a `-SettingsFile` run). Policy names, defaults, precedence order, GPO scopes, and the
registry/`powershell.config.json` storage per scope were read from about_Execution_Policies (5.1 and 7.5 versions).
No Group Policy exists on this machine, so GPO behaviour is from the docs, and no policy was changed on any scope.
