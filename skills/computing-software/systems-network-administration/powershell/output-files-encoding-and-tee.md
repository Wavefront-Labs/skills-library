---
id: computing-software.systems-network-administration.powershell.output-files-encoding-and-tee
name: output-files-encoding-and-tee
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-pipeline, out-file-encoding, tee-object, utf8]
level: practitioner
status: verified
description: "Write pipeline output to files correctly: Out-File, Set-Content and Add-Content differences, encoding defaults in 5.1 vs 7, -Width truncation and Tee-Object."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/tee-object
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output files, encoding and Tee-Object

## Which cmdlet
| Cmdlet | Writes | Use for |
|---|---|---|
| `Out-File` / `>` / `>>` | the **formatted** display (what you see on screen) | human-readable logs of formatted output |
| `Set-Content` / `Add-Content` | the objects' **string values** (ToString), no formatting | data files, config files |
| `Export-Csv` / `ConvertTo-Json` | structured data | anything another program reads |

`Get-Process | Out-File p.txt` writes a table; `Get-Process | Set-Content p.txt` writes `System.Diagnostics.Process (name)`
lines (both confirmed). Know which you want.

## Encoding defaults (the classic trap)
- Windows PowerShell 5.1: `Out-File`/`>` default **UTF-16 LE (Unicode)** (bytes `FF FE 4A 00 ...`); `Set-Content` and `Add-Content`
  default to the system ANSI code page (`é` written as `E9`); `Export-Csv` ASCII (`é` became `?`).
- PowerShell 7: **UTF-8 without BOM** everywhere (`4A 6F 73 C3 A9`), including `>` and `Add-Content`.
Files written by 5.1 with `>` look "spaced out" to Linux tools and break scripts expecting UTF-8. Be explicit:
```powershell
$data | Out-File report.txt -Encoding utf8          # 5.1 writes UTF-8 with BOM (EF BB BF); 7 writes none
$data | Set-Content config.ini -Encoding utf8NoBOM  # pwsh 7 only (5.1 rejects the value)
[IO.File]::WriteAllLines($path, $lines)             # UTF-8 no BOM in 5.1 and 7
```
Set a default: `$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'` (it also applied to `>` redirection in both editions).

## Width truncation
`Out-File` wraps/truncates at the console width (a three-column table was cut at 120 characters in a non-interactive run); for wide
tables use `-Width 4096` (182 characters, uncut) or `Format-Table -AutoSize | Out-String -Width 4096`.

## Tee-Object: see it and save it
```powershell
Get-Service | Where-Object Status -eq Stopped | Tee-Object -FilePath stopped.txt | Measure-Object
Get-ChildItem | Tee-Object -Variable files | Select -First 5
```
`-Append` worked in both 7.6.7 and 5.1 and adds to an existing file. Tee wrote the formatted table text (header row
`Status Name DisplayName`) to the file, like Out-File.

## Verify
- [ ] Files open correctly in the consuming tool; encoding chosen explicitly in scripts that run on 5.1.

## Checked
Ran on PowerShell 7.6.7 and Windows PowerShell 5.1.26100 with the string `José`: bytes written by `Out-File`, `>`, `Set-Content`,
`Add-Content`, `Export-Csv` (default), `Out-File -Encoding utf8`, `Set-Content -Encoding utf8NoBOM` (5.1 rejects it),
`[IO.File]::WriteAllLines`, and with `$PSDefaultParameterValues` for `Out-File` and `>`; `Get-Process` through `Out-File` versus
`Set-Content`; `-Width` truncation (120 versus 182 columns); `Tee-Object -FilePath`, `-Variable` and `-Append`.
