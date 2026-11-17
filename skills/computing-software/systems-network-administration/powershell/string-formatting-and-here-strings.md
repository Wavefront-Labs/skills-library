---
id: computing-software.systems-network-administration.powershell.string-formatting-and-here-strings
name: string-formatting-and-here-strings
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, format-operator, here-strings, string-interpolation, quoting-rules, subexpression, stringbuilder]
level: practitioner
status: verified
description: "Build strings correctly in PowerShell: quoting rules, $() subexpressions, the -f format operator, here-strings for templates, escaping and large-string performance."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-string-substitutions
  - https://learn.microsoft.com/en-us/dotnet/standard/base-types/composite-formatting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String formatting and here-strings

## Quoting rules
- `'single'` is literal. `"double"` expands `$var` and `$(expression)`.
- Properties and indexes need a subexpression: `"Host: $($vm.Name) ($($vm.State))"`.
  `"$vm.Name"` prints the object's ToString() followed by `.Name`.
- `"$var:"` is parsed as a scope/drive qualifier; write `"${var}:"`.
- Escape with backtick: `` `$ ``, `` `" ``, `` `n `` (newline), `` `t `` (tab), `` `e `` (ESC, PS 6+).
  A literal single quote inside single quotes is doubled: `'It''s'`.

## -f format operator
```powershell
'{0,-20} {1,8:N1} GB {2:P0}' -f $disk.DeviceID, ($disk.Size/1GB), ($disk.FreeSpace/$disk.Size)
'{0:yyyy-MM-dd HH:mm}' -f (Get-Date)
'{0:D5}' -f 42           # 00042
'{0:X8}' -f 3221225477   # C0000005 (NTSTATUS)
'{{literal braces}} {0}' -f 'x'
```
- `{index,alignment:format}`: negative alignment left-aligns.
- `-f` binds tighter than most operators: wrap arithmetic arguments in parentheses.
- Passing an array as the only argument spreads it: `'{0}-{1}' -f $arr`.
- Checked with `-f` and `[cultureinfo]::CurrentCulture = 'de-DE'`: `'{0:N1}' -f 1234.5` gives `1.234,5`, while plain interpolation `"$x"` stays invariant (`1234.5`).
- `'{0}' -f 3*2` prints `33` (the `*` repeats the string), so write `'{0}' -f (3*2)`.
- Formatting with `-f` uses the **current culture** (`N1` may give `1.234,5`). For machine-readable
  output use `$x.ToString('F1', [cultureinfo]::InvariantCulture)`.

## Here-strings for templates and multi-line text
```powershell
$sql = @"
SELECT name, state_desc
FROM sys.databases
WHERE name = N'$($db.Replace("'", "''"))'
"@
$json = @'
{ "literal": "$nothing expands here" }
'@
```
- Opening `@"` / `@'` must end its line; closing `"@` / `'@` must start at **column 0**.
- Inside a double here-string, quotes need no escaping; variables still expand.
- Template filled later: store a single-quoted here-string and call
  `$ExecutionContext.InvokeCommand.ExpandString($template)` only with trusted templates, or
  use `-f` placeholders (safer).

## Joining and building big strings
```powershell
$names -join ', '
[string]::Join("`n", $lines)
$sb = [System.Text.StringBuilder]::new()
foreach ($r in $rows) { [void]$sb.AppendLine("$($r.Name),$($r.Value)") }
$sb.ToString()
```
`$s += 'x'` in a loop allocates a new string every time; use `StringBuilder` or `-join`.

## Verify
- [ ] Output columns align with `-f` alignment in a fixed-width font.
- [ ] Machine-readable numbers use invariant culture on a non-English test box.
