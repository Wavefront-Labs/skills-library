---
id: computing-software.systems-network-administration.powershell.compare-object-diffs
name: compare-object-diffs
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-pipeline, compare-object, reporting, configuration-drift]
level: practitioner
status: verified
description: "Diff sets of objects with Compare-Object: choosing properties, SideIndicator, IncludeEqual and PassThru, plus faster HashSet comparisons for large lists."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/compare-object
  - https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.hashset-1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compare-Object for diffs

## Basics
```powershell
$before = Get-Content before.txt
$after  = Get-Content after.txt
Compare-Object $before $after
```
`SideIndicator`: `<=` only in the reference (first), `=>` only in the difference (second), `==` in both
(with `-IncludeEqual`).

## Compare objects by properties
Without `-Property`, objects are compared by their string form, which for complex objects is often just the type
name (or, for a `[pscustomobject]`, its `@{...}` text), so unrelated objects can look equal. Verified: two `[pscustomobject]` lists with identical text compare as no difference. Always specify:
```powershell
$a = Get-LocalGroupMember 'Users' | Select-Object Name, ObjectClass
$b = Import-Clixml users-baseline.xml        # saved earlier with Export-Clixml
Compare-Object $b $a -Property Name | Select-Object Name, SideIndicator
```
`-PassThru` returns the original objects (with SideIndicator added) instead of a new object with only the compared
properties:
```powershell
Compare-Object $b $a -Property Name -PassThru | Where-Object SideIndicator -eq '=>'    # newly added
```

## Drift checks
```powershell
$baseline = Import-Csv services-baseline.csv
$now = Get-Service | Select Name,StartType,Status
Compare-Object $baseline $now -Property Name,StartType | Sort Name
```

## Case and culture
`-CaseSensitive` for exact matching; default is case-insensitive.

## Performance
Compare-Object is fine for thousands of items; for hundreds of thousands use a HashSet:
```powershell
$set = [System.Collections.Generic.HashSet[string]]::new([string[]]$before, [System.StringComparer]::OrdinalIgnoreCase)
$added = $after | Where-Object { -not $set.Contains($_) }
```
`-SyncWindow` defaults to `[int]::MaxValue`, meaning the whole collection is searched for a match; a smaller value is faster on big collections but can be less accurate (per the Compare-Object reference).

## Verify
- [ ] Output contains only intended differences; properties chosen explicitly.
