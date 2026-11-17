---
id: computing-software.systems-network-administration.powershell.regex-match-replace-select-string
name: regex-match-replace-select-string
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-data, powershell-regex, regular-expressions, select-string, match-operator, replace-operator, switch-regex, log-parsing]
level: practitioner
status: verified
description: "Parse logs and text with PowerShell regex: -match and $Matches, named groups, -replace with substitutions, Select-String across files, switch -Regex and escaping."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_regular_expressions
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-string
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex with -match, -replace and Select-String

PowerShell regex is .NET regex, **case-insensitive by default**. Use `-cmatch`, `-creplace`,
`Select-String -CaseSensitive` for case-sensitive matching.

## -match and named groups
```powershell
$line = '2026-10-16 03:12:44 DENY TCP 10.1.2.3:51514 -> 10.9.9.9:445'
if ($line -match '^(?<date>\S+) (?<time>\S+) (?<action>\w+) \w+ (?<src>[\d.]+):\d+ -> (?<dst>[\d.]+):(?<port>\d+)') {
  [pscustomobject]@{ Action = $Matches.action; Src = $Matches.src; Port = [int]$Matches.port }
}
```
- `$Matches` is set only when the left side is a **scalar** and the match succeeds; it keeps
  the previous value after a failed match, so always test the `if`.
- On an array, `-match` filters and returns matching elements; `$Matches` is not updated.
- All matches in a string: `[regex]::Matches($text, '\b\d{1,3}(\.\d{1,3}){3}\b').Value`.

## -replace
```powershell
'Smith, John' -replace '^(\w+), (\w+)$', '$2 $1'            # single quotes so $2 is not a PS variable
'C0FFEE' -replace '(?<a>..)(?<b>..)(?<c>..)', '${c}${b}${a}'
$path -replace [regex]::Escape('\\oldsrv\share'), '\\newsrv\share'   # literal text
'a1b22' -replace '\d+', { [int]$_.Value * 2 }               # scriptblock replacement, PS 6+
```
Use `.Replace()` (string method, literal and case-sensitive) when no regex is needed.

## Select-String across files
```powershell
Select-String -Path <LOG_DIR>\*.log -Pattern 'error|fail' -Context 2,0 |
  Select-Object Path, LineNumber, Line

Get-ChildItem <LOG_DIR> -Recurse -Filter *.log |
  Select-String -Pattern 'user=(?<u>\w+)' -AllMatches |
  ForEach-Object { $_.Matches.Groups | Where-Object Name -eq 'u' | ForEach-Object Value } |
  Group-Object -NoElement | Sort-Object Count -Descending
```
- `-SimpleMatch` for literal text (no escaping worries); `-NotMatch` inverts; `-List` stops at
  the first hit per file; `-Raw` (PS 7) returns plain strings.
- Checked on 7.6: `-Context 2,0`, `-List`, `-NotMatch`, `-SimpleMatch`, `-Raw` and `-AllMatches` behave as described.
- Encoding: pass `-Encoding` for UTF-16 logs if matches seem to vanish.

## switch -Regex for multi-pattern parsing
```powershell
switch -Regex -File .\dhcp.log {
  '^\d+,(?<id>10|11),' { "lease: $($Matches.id)" }
  'DNS update failed'  { $dnsFail++ }
  default              { }
}
```
`-File` streams the file line by line (memory-light), and each clause can set `$Matches`.

## Gotchas
- Escape user input with `[regex]::Escape()` before embedding it in a pattern.
- `-split` also takes a regex: `'a.b' -split '.'` returns empty strings; use `-split '\.'` or `'a.b'.Split('.')`.
- Multi-line patterns need the whole file as one string: `Get-Content -Raw`, plus `(?m)` or `(?s)`.

## Verify
- [ ] Parser output count equals `Select-String -Pattern ... | Measure-Object` on the same file.
- [ ] Patterns are tested against at least one non-matching line.
