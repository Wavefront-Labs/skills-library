---
id: computing-software.systems-network-administration.powershell.calculated-properties
name: calculated-properties
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-pipeline, calculated-properties, select-object, format-table, sort-object]
level: practitioner
status: verified
description: "Reshape objects with calculated properties in Select-Object, Format-Table and Sort-Object: name/expression keys, formatting, multi-key sorts and the gotchas."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_calculated_properties
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-object
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calculated properties

A calculated property is a hashtable passed where a property name is expected.

| Cmdlet | Keys accepted |
|---|---|
| `Select-Object` | `Name`/`Label` (`n`/`l`), `Expression` (`e`) |
| `Format-Table` | `Name`/`Label`, `Expression`, `FormatString`, `Width`, `Alignment` |
| `Format-List` | `Name`/`Label`, `Expression`, `FormatString` |
| `Format-Wide` | `Expression`, `FormatString` only (a `Name`/`Label` key throws "The n key is not valid") |
| `Sort-Object` | `Expression`, `Ascending`/`Descending` (per key) |
| `Group-Object`, `Compare-Object` | `Expression` |
| `Measure-Object` | a scriptblock only: `-Property @{Expression={...}}` fails to bind (about_Calculated_Properties) |

## Data, not display: Select-Object
```powershell
Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' |
  Select-Object PSComputerName, DeviceID,
    @{n='SizeGB';  e={[math]::Round($_.Size/1GB,1)}},
    @{n='FreePct'; e={[math]::Round(100*$_.FreeSpace/$_.Size,1)}} |
  Where-Object FreePct -lt 15 |
  Export-Csv low-disk.csv -NoTypeInformation
```
Keep numbers numeric in `Select-Object` so later `Where-Object`/`Sort-Object` compare
numerically. `'{0:N1}' -f $x` returns a **string**: sorting it puts "9.5" after "10.2".

## Display only: Format-Table
```powershell
Get-Process | Sort-Object WS -Descending | Select-Object -First 10 |
  Format-Table Name, Id,
    @{n='WS(MB)'; e={$_.WS/1MB}; FormatString='N0'; Alignment='Right'} -AutoSize
```
`Format-*` emits formatting records; nothing useful can be piped after it. Format last.

## Multi-key sort with mixed directions
```powershell
Get-Service | Sort-Object @{e='Status'; Descending=$true}, @{e='Name'; Ascending=$true}
```

## Gotchas
- `$_` inside the expression is the current input object; `$PSItem` is the same thing.
- A name with spaces needs quoting downstream (`Where-Object 'Free %' -lt 10`). Prefer `FreePct`.
- The hashtable cannot see sibling calculated properties. For many derived fields build a
  `[pscustomobject]` in `ForEach-Object` instead.
- `Select-Object -ExpandProperty X` with other properties adds those as NoteProperties onto
  each expanded value, which surprises people. Use it alone to get raw values.
- `Expression` may also be a plain property-name string.
- Checked on PowerShell 7.6 and 5.1: `'{0:N1}' -f` values sort as strings (`10.2` before `9.5`), and a calculated property cannot reference a sibling (it comes back `$null`).

## Verify
- [ ] `| Get-Member` after `Select-Object` shows calculated properties typed as numbers where expected.
- [ ] Sorting on a calculated numeric column orders 9 before 10.
