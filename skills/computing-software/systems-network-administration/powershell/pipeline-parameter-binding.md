---
id: computing-software.systems-network-administration.powershell.pipeline-parameter-binding
name: pipeline-parameter-binding
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-pipeline, pipeline, valuefrompipeline, valuefrompipelinebypropertyname, parameter-binding, trace-command, process-block, advanced-functions]
level: practitioner
status: verified
description: "Make functions accept pipeline input ByValue and ByPropertyName, debug why a pipe does not bind with Trace-Command, and avoid the common binding traps."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/trace-command
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline parameter binding (ByValue and ByPropertyName)

PowerShell binds each piped object to every parameter that can accept it: by value (the whole object, converted
if needed) and by property name (a property or alias matching the parameter name). One piped object can bind
several parameters at once. Checked on 7.6.7 with `param([Parameter(ValueFromPipeline)][string]$S,
[Parameter(ValueFromPipelineByPropertyName)]$Name)` and `[pscustomobject]@{Name='n'}`: `$S` received the
converted text `@{Name=n}` and `$Name` received `n`. `Trace-Command -Name ParameterBinding` labels each attempt
(for example `ValueFromPipeline NO COERCION`); use it rather than assuming an order.

## Write a function that binds both ways
```powershell
function Get-Reach {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName)]
    [Alias('CN','DNSHostName','Name')]          # aliases let objects with these property names bind by property name
    [string[]]$ComputerName
  )
  process {                                      # runs once per piped object
    foreach ($c in $ComputerName) {              # also handles -ComputerName a,b,c
      [pscustomobject]@{ Computer = $c; Reachable = Test-Connection $c -Count 1 -Quiet }
    }
  }
}
'srv1','srv2' | Get-Reach                    # ByValue
[pscustomobject]@{ DNSHostName = 'localhost' } | Get-Reach   # ByPropertyName via the DNSHostName alias
Import-Csv servers.csv | Get-Reach           # CSV column ComputerName binds by name
```

## Rules that bite
- Code outside `process {}` sees only the **last** piped object. A function with no named
  blocks runs everything as `end`, so `$ComputerName` holds just the final item.
- `[string[]]` plus the inner `foreach` is required: piped input arrives one item at a time,
  parameter input arrives as an array.
- Give only one parameter per parameter set `ValueFromPipeline` for a given type: checked, two `[string]`
  ByValue parameters in one set both received the same piped string (`a=z b=z`), which is rarely intended.
- An `[object]` ByValue parameter takes the whole object, but a ByPropertyName parameter still bound as well
  in the test above; type the ByValue parameter narrowly so it does not receive unwanted text conversions.
- ByPropertyName matches the property **name or any alias**. Add `[Alias()]` instead of
  piping through `Select-Object @{n='ComputerName';e={$_.Name}}` everywhere.
- A scriptblock passed to a ByPropertyName parameter is a **delay-bind scriptblock**:
  `Get-ChildItem *.log | Rename-Item -NewName { $_.Name -replace '\.log$','.old' }`.

Run on 7.6.7: `-ComputerName a,b` versus piping, alias binding (`DNSHostName`, `CN`), CSV-style `ComputerName` objects, the no-named-blocks function seeing only the last item (`x=3`), the delay-bind `Rename-Item -NewName { ... }` renaming `.log` to `.old`, and `Get-Help Get-Item -Parameter Path` reporting `true (ByValue, ByPropertyName)`.

## Debug a pipe that will not bind
```powershell
Trace-Command -Name ParameterBinding -PSHost -Expression {
  [pscustomobject]@{ DNSHostName = 'localhost' } | Get-Reach
}
```
Read the `BIND PIPELINE object to parameters` section: it shows each parameter tried,
whether conversion was attempted and why it was skipped. `Get-Help <cmd> -Parameter *`
shows `Accept pipeline input?` for built-in cmdlets.

## Verify
- [ ] `1..3 | ForEach-Object { "srv$_" } | Get-Reach` processes all three, not just srv3.
- [ ] `Get-Reach -ComputerName a,b` and `'a','b' | Get-Reach` return the same rows.
- [ ] `Trace-Command` shows the expected parameter bound for each input shape.
