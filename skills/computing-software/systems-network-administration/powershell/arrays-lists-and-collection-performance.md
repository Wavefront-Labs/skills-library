---
id: computing-software.systems-network-administration.powershell.arrays-lists-and-collection-performance
name: arrays-lists-and-collection-performance
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, powershell-arrays, generic-list, performance]
level: practitioner
status: verified
description: "Build collections efficiently: why += on arrays is quadratic, List[T] and direct pipeline assignment, array subexpressions, and HashSet/Dictionary lookups."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-arrays
  - https://learn.microsoft.com/en-us/powershell/scripting/dev-cross-plat/performance/script-authoring-considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrays, lists and collection performance

## Arrays are fixed size
`$a += $item` creates a new array and copies everything each time: O(n^2). Fine for 100 items, painful for 100,000
(minutes instead of milliseconds).

## Faster patterns
1. Let the pipeline/loop build the array:
```powershell
$results = foreach ($s in $servers) { Test-Connection $s -Count 1 -Quiet }
```
2. Generic list when you must add conditionally:
```powershell
$list = [System.Collections.Generic.List[pscustomobject]]::new()
foreach ($u in $users) { if ($u.Enabled) { $list.Add([pscustomobject]@{Name=$u.Name}) } }
```
`List[T].Add` returns nothing (unlike ArrayList.Add, which returns the index and pollutes output).
3. Measured here appending 1..N: N=40,000 took 28 s with `+=` on Windows PowerShell 5.1 and 4.2 s on PowerShell 7.6.7 (about 7x faster, still quadratic), against 5 to 17 ms for a `foreach` assignment or `List[int].Add`. Which 7.x release introduced the speed-up was not checked; use the patterns above on any version.

## Making sure you have an array
```powershell
$items = @(Get-ChildItem *.log)      # always an array, even with 0 or 1 result
$items.Count
```
Single results are scalars otherwise; `.Count` on a scalar works in 3.0+ but `[0]` indexing on a string gives a char.

## Lookups: use hashing
```powershell
$byName = @{}; foreach ($u in $users) { $byName[$u.SamAccountName] = $u }      # O(1) lookup
$set = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
```
`$array -contains $x` inside a loop is O(n) each time; a HashSet or hashtable makes the loop linear (20,000 lookups in a 20,000-item array: 1.5 s on 7.6.7 and 4.6 s on 5.1 with `-contains`, 19 ms to 186 ms with a `HashSet`).

## Slicing and ranges
`$a[0..9]`, `$a[-1]` (last), `$a[-3..-1]`. Arrays of arrays: `,` unary operator keeps a nested array as one element.

## Typed arrays
`[string[]]$names = ...` converts elements and errors early on bad types.

Checked on 7.6.7: `List[T].Add` returns nothing while `ArrayList.Add` returns the index, `'abc'[0]` is a char, `@()` wrapping gives Count 0 for no result, slicing `$a[-3..-1]`, and `[int[]]$z='a','b'` failing early.

## Verify
- [ ] No `+=` in loops over large inputs; `Measure-Command` confirms run time.
