---
id: computing-software.systems-network-administration.powershell.powershell-profiles
name: powershell-profiles
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-environment, powershell-profiles, profile-ps1, noprofile, psdefaultparametervalues, startup-performance]
level: practitioner
status: gated
description: "Use PowerShell profiles well: the four profile paths per host and edition, what belongs in them, keeping startup fast, and why automation must run with -NoProfile."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell profiles

A profile is a script dot-sourced at startup of an interactive host.

## Which files
```powershell
$PROFILE | Select-Object *            # all four paths for this host and edition
Test-Path $PROFILE.CurrentUserAllHosts
```
| Property | PS 7 path (Windows) | Applies to |
|---|---|---|
| `AllUsersAllHosts` | `$PSHOME\Profile.ps1` | everyone, every host |
| `AllUsersCurrentHost` | `$PSHOME\Microsoft.PowerShell_profile.ps1` | everyone, console only |
| `CurrentUserAllHosts` | `Documents\PowerShell\Profile.ps1` | you, every host (console, VS Code, ISE-like hosts) |
| `CurrentUserCurrentHost` (`$PROFILE`) | `Documents\PowerShell\Microsoft.PowerShell_profile.ps1` | you, console only |

Windows PowerShell 5.1 uses `Documents\WindowsPowerShell\` and `$env:SystemRoot\System32\WindowsPowerShell\v1.0\`.
VS Code's host uses `Microsoft.VSCode_profile.ps1` (gated: unconfirmed, source is paywalled or blocked). Load order is the table order, top to bottom (the two AllUsers
profiles of a test install printed `AllUsersAllHosts` then `AllUsersCurrentHost` before the script body started).
If Documents is redirected to OneDrive, the profile follows it (and syncs) (gated: unconfirmed, source is paywalled or blocked).

## What belongs in a profile
```powershell
# Documents\PowerShell\Profile.ps1
$PSDefaultParameterValues['Export-Csv:NoTypeInformation'] = $true
$PSDefaultParameterValues['*-AD*:Server'] = 'dc01.ad.example.com'     # wildcards work (tested with '*-Csv:Delimiter')
Set-PSReadLineOption -PredictionSource History -EditMode Windows
function prompt { "[$env:COMPUTERNAME] $($executionContext.SessionState.Path.CurrentLocation)> " }
Set-Alias ll Get-ChildItem
```
Interactive conveniences only: prompt, aliases, PSReadLine, default parameter values,
argument completers.

## What does not
- Anything a script depends on. Scripts must work on a clean host; put dependencies in
  `#Requires -Modules` and the script itself.
- Slow work (network calls, `Import-Module` of large modules, `Connect-*`). Modules
  autoload on first use; let them.
- Secrets.

## Keep startup fast
```powershell
pwsh -NoProfile -Command 'Measure-Command { . $PROFILE.CurrentUserAllHosts }'
```
Dot-sourcing a small test profile took about 13 ms; a slow profile is noticeable at the prompt. Lazy-load heavy items with a function wrapper or
`Register-EngineEvent -SourceIdentifier PowerShell.OnIdle -MaxTriggerCount 1 -Action { ... }` (gated: unconfirmed, source is paywalled or blocked).

## Automation must use -NoProfile
Scheduled tasks, CI, remoting jobs: `pwsh -NoProfile -NonInteractive -File <SCRIPT_PATH>`. A
user's profile changing `$ErrorActionPreference`, aliases or the location will otherwise
change script behaviour: with a profile that defined `ll` and `*-Csv:Delimiter`, `pwsh -File` saw the alias and wrote
`"a";"b"`, while `pwsh -NoProfile -File` did not. Remote sessions never run profiles; to load one there,
`Invoke-Command -Session $s -FilePath $PROFILE` (gated: unconfirmed, source is paywalled or blocked).

## Execution policy
Profiles are scripts: the execution-policy rules apply (see execution-policy-scopes: unsigned or Mark-of-the-Web files fail
under `AllSigned`/`RemoteSigned`, and `Restricted` blocks profiles per about_Execution_Policies).

## Verify
- [ ] `pwsh -NoProfile` and normal start both work; profile load time measured and acceptable.
- [ ] Production scripts pass when run with `-NoProfile`.

## Checked
Ran on PowerShell 7.6.7 and 5.1.26100: `$PROFILE | Select-Object *` (four paths in each edition), a pair of AllUsers profiles placed in a
scratch `$PSHOME` (load order, an alias, a `function prompt`, a wildcard `$PSDefaultParameterValues` entry, effect on a `-File` run with and
without `-NoProfile`), and timing the dot-source. The user's own profile folder was not touched. VS Code host profile name, OneDrive
redirection, `OnIdle` lazy loading and profile loading over remoting were not run.
