---
id: computing-software.systems-network-administration.powershell.format-ps1xml-custom-views
name: format-ps1xml-custom-views
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-pipeline, format-ps1xml, update-formatdata, format-table, default-display-property-set]
level: advanced
status: verified
description: "Control how objects display with format.ps1xml views, Update-FormatData and DefaultDisplayPropertySet, instead of returning Format-Table output from functions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_format.ps1xml
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/update-formatdata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# format.ps1xml and custom views

Functions should output objects, never `Format-Table` (format objects can't be piped to Export-Csv or Where). To
make your objects display nicely by default, give them a type name and a view.

## Tag the object
```powershell
[pscustomobject]@{ PSTypeName='Contoso.ServerHealth'; Name=$n; CpuPct=$cpu; FreeGB=$free; Uptime=$up; Disks=$d }
```

## Quick option: default property set
```powershell
Update-TypeData -TypeName Contoso.ServerHealth -DefaultDisplayPropertySet Name,CpuPct,FreeGB -Force
```
Without any view, an object with more than four properties prints as a list of all of them. With the default set, both
`Format-Table` and `Format-List` show only the set (a 5-property test object showed 2 columns); `Format-List *` or
`Select-Object *` shows everything.

## Full option: a view file
`Contoso.Format.ps1xml`:
```xml
<Configuration><ViewDefinitions>
  <View>
    <Name>Contoso.ServerHealth</Name>
    <ViewSelectedBy><TypeName>Contoso.ServerHealth</TypeName></ViewSelectedBy>
    <TableControl>
      <TableHeaders>
        <TableColumnHeader><Label>Name</Label><Width>20</Width></TableColumnHeader>
        <TableColumnHeader><Label>CPU%</Label><Alignment>Right</Alignment></TableColumnHeader>
        <TableColumnHeader><Label>Free(GB)</Label><Alignment>Right</Alignment></TableColumnHeader>
      </TableHeaders>
      <TableRowEntries><TableRowEntry><TableColumnItems>
        <TableColumnItem><PropertyName>Name</PropertyName></TableColumnItem>
        <TableColumnItem><ScriptBlock>'{0:N1}' -f $_.CpuPct</ScriptBlock></TableColumnItem>
        <TableColumnItem><PropertyName>FreeGB</PropertyName></TableColumnItem>
      </TableColumnItems></TableRowEntry></TableRowEntries>
    </TableControl>
  </View>
</ViewDefinitions></Configuration>
```
Load it: `Update-FormatData -PrependPath .\Contoso.Format.ps1xml`, or in a module manifest
`FormatsToProcess = 'Contoso.Format.ps1xml'` (both loaded this exact file and produced the three-column table with
`CPU%` showing `12.3` from the `'{0:N1}' -f` script block).

## Tips
- Generate a starting file from existing data: `Get-FormatData -TypeName System.Diagnostics.Process | Export-FormatData -Path p.ps1xml`.
- The view changes display only; all properties remain for `Select *`, CSV and JSON.
- Formatting script blocks should be cheap; they run per row.

## Verify
- [ ] The function's output shows the custom table by default and `| Export-Csv` still contains every property.

## Checked
Ran on PowerShell 7.6.7 and 5.1: the exact view XML via `Update-FormatData -PrependPath` (default list output before,
custom table after), a module with `FormatsToProcess` created by `New-ModuleManifest`, `Update-TypeData
-DefaultDisplayPropertySet` on a second type (table and `Format-List` limited to the set; `Select-Object *` complete),
`ConvertTo-Csv` header still listing all five properties, and `Get-FormatData -TypeName System.Diagnostics.Process |
Export-FormatData` (a 5 KB file). Nothing in this skill depends on an outside service.
