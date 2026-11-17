---
id: computing-software.systems-network-administration.powershell.comparison-operators-and-case-sensitivity
name: comparison-operators-and-case-sensitivity
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, comparison-operators, like-operator, contains-operator]
level: practitioner
status: verified
description: "Use PowerShell comparison operators correctly: -eq on arrays filters, -like vs -match, -contains vs -in, case-sensitive c-prefixed variants and $null on the left."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators
  - https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/possibleincorrectcomparisonwithnull
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparison operators and case sensitivity

## Defaults
All string comparisons are **case-insensitive** by default: `'ABC' -eq 'abc'` is True. Prefix `c` for case-sensitive
(`-ceq`, `-clike`, `-cmatch`, `-ccontains`), `i` to be explicit.

## Equality and ordering
`-eq -ne -gt -ge -lt -le`. The **left operand's type** drives conversion: `'10' -lt 9` compares as strings and
returns True ("1" sorts before "9"), while `10 -lt '9'` converts '9' to an int and returns False. Cast explicitly.

## Arrays on the left filter instead of returning a boolean
```powershell
@(1,2,3,2) -eq 2       # returns 2,2
@('a','b') -ne 'a'     # returns 'b'
if (@() -eq $null) {}  # returns empty array -> false
```
Hence the rule: put `$null` on the **left**: `if ($null -eq $value)`. With `$value -eq $null` and an array value
you get filtered elements, not a boolean.

## Wildcards vs regex
- `-like '*.log'` wildcard (`*`, `?`, `[a-z]`), anchored to the whole string.
- `-match '^\d{3}-'` regex, unanchored by default, fills `$Matches`.
- `-notlike`, `-notmatch`.

## Containment
- `$collection -contains $item` and `$item -in $collection`: exact equality on elements (no wildcards).
- `'abc' -contains 'b'` is False: `-contains` is not substring search; use `.Contains('b')` (case-sensitive) or `-like '*b*'`.

## Type tests
`-is [int]`, `-isnot`, `-as [datetime]` (returns $null instead of throwing).

## Replace and split
`-replace 'regex','sub'` (case-insensitive, `-creplace` for sensitive), `-split ','` (regex), `-join ';'`.

Checked by running each example on PowerShell 7.6: `'abc' -as [datetime]` gives `$null`; `-like '[a-c]'` matches one character in the range and is anchored; `-contains`/`-in` do no substring match.

## Verify
- [ ] Script analyser rule PossibleIncorrectComparisonWithNull clean; case-sensitive comparisons explicit.
