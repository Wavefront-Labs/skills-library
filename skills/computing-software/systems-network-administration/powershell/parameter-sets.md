---
id: computing-software.systems-network-administration.powershell.parameter-sets
name: parameter-sets
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, advanced-functions, cmdletbinding, parameter-sets, defaultparametersetname, parametersetname, mutually-exclusive-parameters]
level: practitioner
status: verified
description: "Design mutually exclusive parameter combinations with parameter sets: DefaultParameterSetName, shared parameters, branching on $PSCmdlet.ParameterSetName, fixing ambiguity."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parameter_sets
  - https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/cmdlet-parameter-sets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter sets

Use parameter sets when a function has alternative ways to identify its target (by name vs
by object vs by ID) and certain parameters must never be combined.

```powershell
function Get-Account {
  [CmdletBinding(DefaultParameterSetName = 'ByName')]
  param(
    [Parameter(Mandatory, ParameterSetName = 'ByName', Position = 0)]
    [string]$Name,

    [Parameter(Mandatory, ParameterSetName = 'BySid')]
    [System.Security.Principal.SecurityIdentifier]$Sid,

    [Parameter(Mandatory, ParameterSetName = 'ByObject', ValueFromPipeline)]
    [Microsoft.PowerShell.Commands.LocalUser]$InputObject,

    # no ParameterSetName = member of every set
    [switch]$Enabled
  )
  process {
    $u = switch ($PSCmdlet.ParameterSetName) {
      'ByName'   { Get-LocalUser -Name $Name }
      'BySid'    { Get-LocalUser -SID $Sid }
      'ByObject' { Get-LocalUser -SID $InputObject.SID }
    }
    if (-not $Enabled -or $u.Enabled) { "$($PSCmdlet.ParameterSetName): $($u.Name)" }
  }
}
```

## Rules
- Every set needs at least one parameter unique to it, or PowerShell cannot tell sets apart.
- A parameter can belong to several sets: repeat the `[Parameter()]` attribute, one per set,
  with different `Mandatory`/`Position` values per set.
- A parameter with no `ParameterSetName` belongs to all sets (`__AllParameterSets`).
- Set `DefaultParameterSetName` whenever positional or pipeline input could match two sets;
  otherwise users see *"Parameter set cannot be resolved using the specified named parameters"*.
- Positions are evaluated per set; avoid two different parameters at Position 0 in sets that
  could both be candidates.
- Pipeline binding also chooses the set: each set may have its own `ValueFromPipeline` parameter
  of a different type.
- A switch that selects a mode (`-All`) is a clean way to make a set unique:
  `[Parameter(Mandatory, ParameterSetName='All')][switch]$All`.

The function was run on Windows PowerShell 5.1 and PowerShell 7.6 (`Get-LocalUser` is Windows-only; for a domain use the equivalent `Get-ADUser` calls).

## Inspect and test
```powershell
(Get-Command Get-Account).ParameterSets | Select-Object Name, IsDefault,
  @{n='Params'; e={($_.Parameters.Name | Where-Object { $_ -notin [System.Management.Automation.Cmdlet]::CommonParameters }) -join ','}}
Get-Command Get-Account -Syntax      # one syntax line per set
```
In Pester, assert ambiguity is rejected:
`{ Get-Account -Name x -Sid S-1-5-18 } | Should -Throw -ErrorId 'AmbiguousParameterSet,Get-Account'` (passes on Pester 5.7.1; Pester 3.4 has no `-Throw`).

## Verify
- [ ] `Get-Command -Syntax` shows one line per intended mode and no unexpected combinations.
- [ ] Positional and piped calls resolve without "cannot be resolved" errors.
