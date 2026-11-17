---
id: computing-software.systems-network-administration.powershell.set-ciminstance-and-remove-ciminstance
name: set-ciminstance-and-remove-ciminstance
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-cim, remove-ciminstance, set-ciminstance, new-ciminstance, whatif, wql]
level: practitioner
status: docs-checked
description: "Change and delete WMI/CIM objects with Set-CimInstance and Remove-CimInstance: -Property hashtables, -Query, -InputObject, -PassThru, -WhatIf and CIM sessions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/set-ciminstance
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/remove-ciminstance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set-CimInstance and Remove-CimInstance

Both cmdlets are Windows-only. Without `-ComputerName` or `-CimSession` they work on local WMI over COM.
With `-ComputerName` they create a temporary WSMan session; the docs say a CIM session gives better
performance when you make several operations against one computer.

## Change properties (Set-CimInstance)
`-Property` takes a hashtable; only the properties named in it change, others are left alone.
```powershell
# by WQL query
Set-CimInstance -Query 'Select * from Win32_Environment where name LIKE "testvar%"' -Property @{VariableValue="abcd"}
# by pipeline
Get-CimInstance -Query 'Select * from Win32_Environment where name LIKE "testvar%"' |
  Set-CimInstance -Property @{VariableValue="abcd"}
# by object, returning the modified instance
$x = Get-CimInstance -Query 'Select * from Win32_Environment where Name="testvar"'
Set-CimInstance -InputObject $x -Property @{VariableValue="somevalue"} -PassThru
```
- You can also edit the property on the object (`$x.VariableValue = "Change"`) and commit with `Set-CimInstance`.
- By default no output; `-PassThru` returns the modified instance.
- In the `-Query` parameter sets, `-Property` is required. Default dialect is WQL (`-QueryDialect` accepts WQL or CQL).
- In a query, escape `"`, `'` and `\` with a backslash; with WQL `LIKE`, wrap `%`, `_` and `[` in square brackets.
- `-InputObject` does not enumerate collections (a collection throws); pipe them instead.
- Default namespace is root/CIMV2 (`-Namespace`, query sets only).
- `-ResourceUri` works only over WSMan; with a DCOM session it errors.

## Delete instances (Remove-CimInstance)
```powershell
Remove-CimInstance -Query 'Select * from Win32_Environment where name LIKE "testvar%"'
$var = Get-CimInstance -Query 'Select * from Win32_Process where name LIKE "notepad%"'
Remove-CimInstance -InputObject $var
```
- Removes the instance on the CIM server only; the object you passed in is not changed.
- Returns no output. The page is inconsistent on piping: the INPUTS section says you can't pipe objects, while the `-InputObject` parameter table lists pipeline input ByValue. Prefer `-InputObject` or `-Query` as in the examples.

## Preview first
Both support `-WhatIf` (show what would happen) and `-Confirm` (prompt before acting); the docs show these with
`Set-CimInstance` splatting (`WhatIf = $true`).

## Checked
Method: 2026-11-08, read both cited learn.microsoft.com cmdlet pages in full (PowerShell-Docs 7.5 markdown source). Rewritten to the pages' syntax, examples and parameter notes. Removed earlier unsupported claims: the `write` qualifier check, the "Not supported" error, Win32_UserProfile cleanup behaviour and static-method creation notes. Not executed.
