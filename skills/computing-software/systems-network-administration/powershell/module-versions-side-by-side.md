---
id: computing-software.systems-network-administration.powershell.module-versions-side-by-side
name: module-versions-side-by-side
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-modules, psresourceget, module-versioning, requiredversion, requires-modules, psmodulepath, side-by-side, assembly-conflicts]
level: advanced
status: gated
description: "Control which module version loads: side-by-side install folders, #Requires and RequiredVersion pins, PSModulePath order, update and cleanup, and .NET assembly conflicts."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_modules
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_requires
  - https://learn.microsoft.com/en-us/powershell/scripting/dev-cross-plat/resolving-dependency-conflicts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module versions and side-by-side loading

Modules install into `<ModuleRoot>\<Name>\<Version>\`, so several versions coexist. Without
a pin, `Import-Module` and autoloading pick the **highest version found in the first
`$env:PSModulePath` folder that contains the module**, not necessarily the highest overall.

## See what is installed and what loaded
```powershell
Get-Module Az.Accounts -ListAvailable | Select-Object Name, Version, ModuleBase
Get-Module Az.Accounts                                  # loaded in this session
$env:PSModulePath -split [IO.Path]::PathSeparator
Get-InstalledPSResource Az.Accounts                     # PSResourceGet's view
```
Default PSModulePath order (PS 7.6.7 on Windows, read from `$env:PSModulePath`): user `Documents\PowerShell\Modules`, then
`$env:ProgramFiles\PowerShell\Modules`, then `$PSHOME\Modules`, then `Documents\WindowsPowerShell\Modules`,
`$env:ProgramFiles\WindowsPowerShell\Modules` and the System32 `WindowsPowerShell\v1.0\Modules` folder. Windows PowerShell 5.1
uses the last three only. A stale copy in an earlier folder shadows a newer one later in the list (test: `ModA` 2.0.0 in
the first folder beat 3.0.0 in the second; swapping the folders loaded 3.0.0).

## Pin versions in scripts
```powershell
#Requires -Modules @{ ModuleName = 'Az.Accounts'; ModuleVersion = '3.0.0' }          # minimum
#Requires -Modules @{ ModuleName = 'Pester'; RequiredVersion = '5.6.1' }              # exact
#Requires -Modules @{ ModuleName = 'ExchangeOnlineManagement'; MaximumVersion = '3.9.99' }
Import-Module Pester -RequiredVersion 5.6.1
Import-Module Az.Accounts -MinimumVersion 3.0.0
```
In a module manifest, `RequiredModules = @(@{ModuleName='Az.Accounts'; ModuleVersion='3.0.0'})`
loads dependencies first (a manifest requiring `ModA` 2.5.0 imported and loaded `ModA` 3.0.0); an unsatisfiable version fails
the import: `The required module 'ModA' is not loaded. Load the module or remove the module from 'RequiredModules' in the file ...`.

## Install, update and clean up
```powershell
Install-PSResource Pester -Version '[5.6.1]' -Scope AllUsers -TrustRepository     # exact (NuGet range syntax)
Install-PSResource Az -Version '[12.0,13.0)'                                      # range
Update-PSResource Pester                     # installs newer alongside; does not remove old
Get-InstalledPSResource Pester | Sort-Object Version -Descending | Select-Object -Skip 1 |
  Uninstall-PSResource                        # keep only newest
```
The NuGet range syntax (`[5.6.1]`, `[12.0,13.0)`; a bare `1.0.0.0` is not "1.0.0.0 and higher"), `-Scope` (default CurrentUser; AllUsers
needs elevation), and Update-PSResource's side-by-side install were read on Microsoft Learn. The install, update and uninstall calls
themselves were not run (they would write modules into user or machine folders) (gated: unconfirmed, source is paywalled or blocked). Learn's Update-PSResource page also says there is no
command to uninstall older versions, while `Uninstall-PSResource` takes a PSResourceInfo from the pipeline (`InputObject`, confirmed
on the command), so check the pipeline with `-WhatIf` first.
PowerShellGet v2 equivalents: `Install-Module -RequiredVersion`, `-AllowClobber`,
`-SkipPublisherCheck` (the parameters exist; Windows PowerShell 5.1 here ships Pester 3.4.0 under `Program Files\WindowsPowerShell\Modules`,
and that replacing it needs `-SkipPublisherCheck` (gated: unconfirmed, source is paywalled or blocked)).

## Assembly conflicts (the hard case)
Only one version of a given .NET assembly can load per process (per AssemblyLoadContext).
If module A loaded `Newtonsoft.Json 12` and module B needs `13`, B fails with
`Could not load file or assembly ... version=13.0.0.0`; this combination was not reproduced here and the error text, and the
Az + Microsoft.Graph + ExchangeOnlineManagement example, are (gated: unconfirmed, source is paywalled or blocked). PowerShell 7.6.7 itself already has `Newtonsoft.Json 13.0.0.0` loaded at
start-up, which is why modules built against older or newer copies can clash.
- Fix: start a fresh `pwsh` and import modules in the order that loads the newest shared
  assembly first, or run conflicting work in separate processes (`Start-Job`, separate scripts).
- `[AppDomain]::CurrentDomain.GetAssemblies() | Where-Object FullName -like '*Json*'` shows
  what loaded.

## Verify
- [ ] `(Get-Module X).Version` after import equals the pinned version.
- [ ] Only intended versions remain in `Get-Module X -ListAvailable`.
- [ ] Scheduled scripts carry `#Requires -Modules` so a missing version fails fast.

## Checked
Built throwaway modules in a scratch PSModulePath and ran on PowerShell 7.6.7 and 5.1.26100: `Get-Module -ListAvailable` ordering,
which version `Import-Module` picked with the folders in each order, `-RequiredVersion`, `-MinimumVersion` (picked 3.0.0 from the first
folder holding any match), an unsatisfiable `-MinimumVersion`, `#Requires -Modules` with `ModuleVersion` (minimum), `RequiredVersion` and
`MaximumVersion` (each behaved as the skill says; the unsatisfied one reported the module cannot be found with that version), manifest
`RequiredModules` (satisfied and unsatisfied), the default PSModulePath order in both editions, and the loaded `Newtonsoft.Json`.
PSResourceGet 1.2.0 ships with 7.6.7. Gallery installs were not run because they write into the user's module folders.
