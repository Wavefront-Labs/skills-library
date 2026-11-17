---
id: computing-software.systems-network-administration.powershell.hashtables-ordered-and-pscustomobject
name: hashtables-ordered-and-pscustomobject
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, hashtables, ordered-dictionary, pscustomobject, generic-list, collections, arrays]
level: practitioner
status: verified
description: "Choose and use hashtables, [ordered] dictionaries, [pscustomobject] and generic lists: lookups, building output objects, array performance and case-sensitivity traps."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_hash_tables
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-pscustomobject
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-arrays
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashtables, ordered dictionaries and PSCustomObject

| Need | Use |
|---|---|
| fast key lookup, config, splatting | `@{}` hashtable (unordered, case-insensitive keys) |
| keys kept in insertion order (output, JSON, CSV columns) | `[ordered]@{}` (OrderedDictionary) |
| a record to emit down the pipeline / export | `[pscustomobject]@{}` |
| growing collection | `[System.Collections.Generic.List[object]]::new()` |
| set membership | `[System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)` |

## Hashtable as a lookup / join
```powershell
$mgr = @{}
Get-Process | ForEach-Object { $mgr[$_.Id] = $_.Name }
$mgr.ContainsKey($PID)          # not $mgr[$PID] -ne $null (value may legitimately be $null)
$mgr.Keys | Sort-Object
foreach ($kv in $mgr.GetEnumerator()) { "$($kv.Key) -> $($kv.Value)" }
```
- Keys are case-insensitive by default (checked: `$h['A']` finds `a`). Case-sensitive: `[hashtable]::new([StringComparer]::Ordinal)`.
- Modifying a hashtable while enumerating `.Keys` throws; enumerate `@($h.Keys)` (a copy).
- Piping a hashtable sends **one** object; use `.GetEnumerator()` to pipe entries.
- `$h.Count` is the entry count, but a key named `Count` shadows it; use `$h.get_Count()` defensively.

## Output records: [pscustomobject]
```powershell
$report = foreach ($s in $servers) {
  $os = Get-CimInstance Win32_OperatingSystem      # local; add -CimSession $s for remote hosts
  [pscustomobject]@{
    Server   = $s
    OS       = $os.Caption
    Uptime   = (Get-Date) - $os.LastBootUpTime
    PatchDue = $os.LastBootUpTime -lt (Get-Date).AddDays(-30)
  }
}
$report | Export-Csv servers.csv -NoTypeInformation
```
- The `[pscustomobject]@{}` literal keeps key order (it is special-cased); `New-Object
  PSObject -Property $hash` does not.
- Capture `foreach` output into a variable instead of `$arr += ...`: `+=` copies the whole
  array each time (quadratic).
- Add a member later: `$obj | Add-Member -NotePropertyName Owner -NotePropertyValue 'ops'`.
- Give it a type name for custom formatting: `$obj.PSObject.TypeNames.Insert(0, 'Contoso.ServerReport')`.
- Convert to hashtable: `$h = @{}; $obj.PSObject.Properties | ForEach-Object { $h[$_.Name] = $_.Value }`.
- `ConvertFrom-Json -AsHashtable` (PS 6+) returns hashtables instead of PSCustomObjects. It is required when keys differ only by case: plain `ConvertFrom-Json` on `{"a":1,"A":2}` throws "contains keys with different casing". In 7.6 the result is an ordered hashtable.

## Arrays
- `@()` forces an array, so `@(Get-Thing).Count` is safe when zero or one result comes back.
- `,` makes a one-element array: `return ,$list` stops the pipeline from unrolling it.
- `-contains` / `-in` test membership; for big sets use a `HashSet`.

## Verify
- [ ] Exported CSV columns appear in the order defined.
- [ ] Lookups use `ContainsKey` and behave correctly for keys with different case.
