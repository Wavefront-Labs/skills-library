---
id: computing-software.systems-network-administration.powershell.powershell-scripting-and-modules
name: powershell-scripting-and-modules
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, pwsh, module, script-module, psm1, psd1, module-manifest, new-modulemanifest, functionstoexport, export-modulemember, psmodulepath, requires, comment-based-help, get-help, psscriptanalyzer, pester, unit-testing, mock, psresourceget, install-psresource, publish-psresource, powershellget, psgallery, private-repository, nuget, semver, code-signing, set-authenticodesignature, allsigned, dot-sourcing, public-private-functions, comment-help-keywords]
level: practitioner
status: draft
description: "Turn PowerShell scripts into versioned modules: psm1/psd1 layout, explicit exports, comment-based help, PSScriptAnalyzer, Pester tests with mocks, signing and publishing with PSResourceGet."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/developer/module/writing-a-windows-powershell-module
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/new-modulemanifest
  - https://pester.dev/docs/quick-start
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.psresourceget/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell scripting and modules — from a pile of .ps1 files to a shipped module

**Goal:** package admin functions as a module the team installs by version, discovers
with `Get-Help`, and trusts because it's linted and tested. Writing the functions
themselves (pipeline, `CmdletBinding`, `-WhatIf`, error handling, remoting) is in
`computing-software.systems-network-administration.powershell.pipeline-scripting-and-remoting`.

## 1. Layout
```
OpsTools/
  OpsTools.psd1          # manifest: version, exports, requirements
  OpsTools.psm1          # loader
  Public/Get-StaleComputer.ps1
  Private/ConvertTo-LdapFilter.ps1
  Tests/Get-StaleComputer.Tests.ps1
```
Loader (`OpsTools.psm1`):
```powershell
$public  = Get-ChildItem "$PSScriptRoot/Public/*.ps1"
$private = Get-ChildItem "$PSScriptRoot/Private/*.ps1" -ErrorAction SilentlyContinue
foreach ($f in @($public) + @($private)) { . $f.FullName }
Export-ModuleMember -Function $public.BaseName
```
One function per file, filename = function name. Many teams "build" (concatenate) into
a single psm1 for release because dot-sourcing hundreds of files slows import.

## 2. Manifest
```powershell
New-ModuleManifest -Path ./OpsTools/OpsTools.psd1 -RootModule OpsTools.psm1 `
  -ModuleVersion 1.2.0 -Author '<TEAM>' -Description 'Ops helper functions' `
  -PowerShellVersion 5.1 -CompatiblePSEditions Desktop,Core `
  -FunctionsToExport 'Get-StaleComputer','Remove-StaleComputer' `
  -CmdletsToExport @() -VariablesToExport @() -AliasesToExport @() `
  -RequiredModules @('ActiveDirectory')
Test-ModuleManifest ./OpsTools/OpsTools.psd1
```
- **List exports explicitly** — never `'*'`. Wildcards force PowerShell to load the
  module to discover commands, killing auto-loading performance, and leak helpers.
- `ModuleVersion` follows SemVer; installed modules live side by side in
  `<path>/OpsTools/1.2.0/`. Scripts pin with `#Requires -Modules @{ModuleName='OpsTools'; ModuleVersion='1.2.0'}`.
- `$env:PSModulePath` decides discovery: per-user (Documents/PowerShell/Modules) vs
  all users (Program Files). Windows PowerShell 5.1 and PowerShell 7 use **different**
  user paths — a module installed for one may be invisible to the other.

## 3. Help that `Get-Help` finds
```powershell
function Get-StaleComputer {
  <#
  .SYNOPSIS  Computers that have not logged on for N days.
  .PARAMETER Days  Inactivity threshold.
  .EXAMPLE   Get-StaleComputer -Days 90 | Export-Csv stale.csv
  #>
  [CmdletBinding()] [OutputType([Microsoft.ActiveDirectory.Management.ADComputer])]
  param([ValidateRange(1,3650)][int]$Days = 90)
  ...
}
```
Every public function gets at least SYNOPSIS and one EXAMPLE.

## 4. Lint and test
```powershell
Invoke-ScriptAnalyzer -Path ./OpsTools -Recurse -Settings PSGallery
Invoke-Pester ./OpsTools/Tests -Output Detailed
```
Pester 5 test with a mock so it runs without AD:
```powershell
BeforeAll { Import-Module "$PSScriptRoot/../OpsTools.psd1" -Force }
Describe 'Get-StaleComputer' {
  It 'returns only computers older than the threshold' {
    Mock -ModuleName OpsTools Get-ADComputer {
      [pscustomobject]@{Name='old'; LastLogonDate=(Get-Date).AddDays(-200)}
      [pscustomobject]@{Name='new'; LastLogonDate=(Get-Date).AddDays(-5)} }
    (Get-StaleComputer -Days 90).Name | Should -Be 'old'
  }
}
```
- `-ModuleName` on `Mock` is required when the call happens inside the module — the
  most common "my mock isn't used" bug.
- Pester 5 runs discovery and execution separately: setup code must live in
  `BeforeAll`/`BeforeEach`, not loose in `Describe`.
- Windows ships Pester 3.4 in-box; install 5.x with `-SkipPublisherCheck` side by side.

## 5. Sign and publish
- Sign scripts and modules if hosts run `AllSigned`:
  `Set-AuthenticodeSignature -FilePath <FILE> -Certificate $cert -TimestampServer <TSA_URL>`.
  Always timestamp, or signatures expire with the certificate. Re-sign after every edit.
- Internal feed (file share or NuGet server) with **PSResourceGet** (PowerShell 7.4+,
  installable on 5.1):
```powershell
Register-PSResourceRepository -Name Internal -Uri '<FEED_URL_OR_SHARE>' -Trusted
Publish-PSResource -Path ./OpsTools -Repository Internal -ApiKey '<API_KEY>'
Install-PSResource OpsTools -Repository Internal -Version '[1.2.0,2.0.0)'
```
Legacy PowerShellGet v2 equivalents are `Register-PSRepository`/`Publish-Module`/
`Install-Module`. Don't publish internal modules to the public PSGallery by accident:
always pass `-Repository`.

**Unconfirmed:** PSResourceGet cmdlet parameters changed during its preview releases;
check `Get-Help Publish-PSResource` on your installed version.

## Verify
- [ ] `Test-ModuleManifest` passes; `Get-Command -Module OpsTools` lists only public functions.
- [ ] `Get-Help <Function> -Examples` works for every exported function.
- [ ] PSScriptAnalyzer is clean and Pester passes in CI without live AD.
- [ ] Module installs from the internal feed by version in both 5.1 and 7 if both are supported.
