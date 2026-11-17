---
id: computing-software.systems-network-administration.powershell.class-based-dsc-resources
name: class-based-dsc-resources
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, dsc, desired-state-configuration, class-based-dsc-resource, dscresource, dsc-v3, invoke-dscresource, psdesiredstateconfiguration, powershell-classes]
level: advanced
status: docs-checked
description: "Write a class-based DSC resource: [DscResource()] class with Get/Test/Set, Key and Mandatory properties, module layout, testing with Invoke-DscResource, and DSC v3 use."
sources:
  - https://learn.microsoft.com/en-us/powershell/dsc/concepts/class-based-resources
  - https://learn.microsoft.com/en-us/powershell/dsc/tutorials/create-class-based-resource
  - https://learn.microsoft.com/en-us/powershell/module/psdesiredstateconfiguration/invoke-dscresource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing class-based DSC resources

A class-based DSC resource is a PowerShell class in a module file (`.psm1`) with no MOF schema file. Which DSC version and adapter you target (Windows PowerShell 5.1, PowerShell 7, DSC v3) changes how it is run: check the current Microsoft DSC documentation for that.

## Module layout
```
ContosoDsc\
  ContosoDsc.psd1      # DscResourcesToExport = @('ContosoAppSetting')
  ContosoDsc.psm1      # the classes (root module or a nested module both work)
```
Manifest essentials: the resource must be listed in `DscResourcesToExport` in the `.psd1`; `Get-DscResource` and DSC itself use that list to find it. Use `RootModule = 'ContosoDsc.psm1'` and a `ModuleVersion` as for any module.

## The resource
```powershell
enum Ensure { Absent; Present }

[DscResource()]
class ContosoAppSetting {
  [DscProperty(Key)]       [string] $Path          # unique identity of the instance
  [DscProperty(Key)]       [string] $Name
  [DscProperty(Mandatory)] [string] $Value
  [DscProperty()]          [Ensure] $Ensure = [Ensure]::Present
  [DscProperty(NotConfigurable)] [string] $CurrentValue   # read-only, returned by Get

  [ContosoAppSetting] Get() {
    $xml = [xml](Get-Content -Raw -LiteralPath $this.Path)
    $node = $xml.configuration.appSettings.add | Where-Object key -eq $this.Name
    $state = [ContosoAppSetting]::new()
    $state.Path = $this.Path; $state.Name = $this.Name
    $state.Ensure = if ($node) { [Ensure]::Present } else { [Ensure]::Absent }
    $state.Value = $state.CurrentValue = $node.value
    return $state
  }

  [bool] Test() {
    $cur = $this.Get()
    if ($this.Ensure -eq [Ensure]::Absent) { return $cur.Ensure -eq [Ensure]::Absent }
    return $cur.Ensure -eq [Ensure]::Present -and $cur.Value -ceq $this.Value
  }

  [void] Set() {
    $xml = [xml]::new(); $xml.PreserveWhitespace = $true; $xml.Load($this.Path)
    $settings = $xml.configuration.appSettings
    $node = $settings.add | Where-Object key -eq $this.Name
    if ($this.Ensure -eq [Ensure]::Absent) { if ($node) { [void]$settings.RemoveChild($node) } }
    else {
      if (-not $node) { $node = $xml.CreateElement('add'); $node.SetAttribute('key', $this.Name); [void]$settings.AppendChild($node) }
      $node.SetAttribute('value', $this.Value)
    }
    $xml.Save($this.Path)
  }
}
```
Rules:
- At least one `Key` property (several Key properties are used together to identify an instance). `Get()` returns an instance of the class and takes no parameters; `Test()` returns `[bool]` and takes no parameters. Implement all three of `Get()`, `Test()` and `Set()`.
- `Mandatory` properties must be specified or `Invoke-DscResource` raises an error; `NotConfigurable` is read-only and holds a value after `Get()`.
- Guidance on `Ensure`: define an `Ensure` enum and use it as the type of a property named `Ensure`.
- Complex properties are classes whose members carry `[DscProperty()]`.
- Keep `Test()` free of side effects and `Set()` safe to repeat (good practice; not stated by the sources).

## Test without a configuration
```powershell
$p = @{ Name = 'ContosoAppSetting'; ModuleName = 'ContosoDsc'
        Property = @{ Path = '<SITE_PATH>\web.config'; Name = 'Env'; Value = 'Prod' } }
Invoke-DscResource @p -Method Test     # InDesiredState True/False
Invoke-DscResource @p -Method Set
Invoke-DscResource @p -Method Get
```
`Invoke-DscResource` accepts `-Method` values Get, Set and Test, with `-Name`, `-ModuleName` and `-Property`. Prerequisites differ between Windows PowerShell 5.1 and PowerShell 7: see the Invoke-DscResource reference. Wrap these calls in tests per method.

## Use from DSC v3
DSC v2.0 and later ignore the `RunAsCredential` setting on `[DscResource()]`; `PsDscRunAsCredential` is supported only in DSC v1.1 and earlier. In PowerShell 7.0, resources run in the user's context, whereas in Windows PowerShell 5.1 they ran as System unless a user context was specified. For DSC v3 adapter names and commands, see the Microsoft DSC documentation (not covered by this skill's sources).

## Verify
- [ ] `Get-DscResource -Module ContosoDsc` lists the resource with its properties.
- [ ] Test returns False, Set fixes, Test returns True, a second Set changes nothing.

## Checked
Date: 2026-11-02. Confirmed against the class-based-resources page (DscResource class in .psm1 root or nested module, DscResourcesToExport, Key/Mandatory/NotConfigurable semantics, Get/Test/Set signatures, Ensure enum guidance, complex properties, RunAsCredential behaviour in DSC v2+) and the Invoke-DscResource reference (Name, ModuleName, Method Get/Set/Test, Property, user-context note). Removed: PSDesiredStateConfiguration version matrix, the "must be root module for 5.1" rule (the docs allow nested modules), 15-minute consistency interval, supported-types list, class reload note, LCM RefreshMode claim, PowerShellVersion manifest line, DSC v3 adapter names and commands.
Method: documentation only; no commands were run.
