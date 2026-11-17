---
id: computing-software.systems-network-administration.powershell.script-logging-and-transcripts
name: script-logging-and-transcripts
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-error-handling, start-transcript, stop-transcript, script-logging, write-information, redirection, streams]
level: practitioner
status: docs-checked
description: "Log PowerShell runs: Start-Transcript options and defaults, the information stream with Write-Information, stream redirection operators, file encoding and width pitfalls."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.host/start-transcript
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-information
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Script logging, transcripts and redirection

## Start-Transcript
```powershell
Start-Transcript -Path <dir>\run-log.txt -NoClobber -IncludeInvocationHeader
# ... work ...
Stop-Transcript
```
- Records commands typed and console output. Default location: `$HOME\Documents` on Windows, `$HOME` on Linux/macOS; default name
  `PowerShell_transcript.<computername>.<random>.<timestamp>.txt` (random part stops filename guessing and collisions).
- `-Path` (a `.txt` file; wildcards not allowed; the command fails if a directory in the path is missing), `-LiteralPath`, or
  `-OutputDirectory` (PowerShell names the file; a relative path is relative to Documents on Windows, home elsewhere).
  Without a path, the global `$Transcript` variable is used if set.
- An existing file is overwritten without warning unless `-NoClobber`; `-Append` adds to it; `-Force` appends to a read-only file by making it read-write.
- `-IncludeInvocationHeader` logs a timestamp when commands run; `-UseMinimalHeader` (added in 6.2) writes a short header instead of the detailed one.
- Default encoding for a file without a BOM is Utf8NoBom. To record whole sessions, put `Start-Transcript` in a profile.

## Information stream
```powershell
Write-Information -MessageData "step done" -Tags "Audit" -InformationAction Continue
Test-Info 6> Info.txt                         # redirect stream 6 to a file
... | Write-Information -InformationVariable InfoMsg
```
- Introduced in Windows PowerShell 5.0; `Write-Host` wraps it, so Write-Host output can be captured or suppressed.
- `$InformationPreference` defaults to SilentlyContinue, so messages are hidden unless you pass `-InformationAction Continue`.
- Records saved with `-InformationVariable` carry MessageData, Source, TimeGenerated, Tags, User, Computer, ProcessId and thread IDs.
- The page says information streams also work for jobs and scheduled tasks.

## Streams and redirection (about_Redirection)
| # | Stream | Introduced |
|---|---|---|
| 1 | Success | 2.0 |
| 2 | Error | 2.0 |
| 3 | Warning | 3.0 |
| 4 | Verbose | 3.0 |
| 5 | Debug | 3.0 |
| 6 | Information (Write-Information, Write-Host) | 5.0 |
| * | All | 3.0 |

Progress cannot be redirected. Operators: `n>` write, `n>>` append, `n>&1` merge into Success (you can only merge into Success).
```powershell
.\script.ps1 *> script.log                  # all streams to a file
dir .\, fakepath 2>&1 > .\dir.log          # errors and output
& { Write-Warning "w"; Write-Error "e"; "o" } 3>&1 2>&1 > out.log
```
- `>` and `n>` overwrite without warning and fail on read-only, hidden or system files; `>>` does not write read-only files but appends to hidden or system ones.
  Use `Out-File -Force` for those.
- Redirection writes UTF8NoBOM; use `Out-File -Encoding` for other encodings. `Tee-Object` writes to a file and passes output on.
- Table output written to files is formatted at the console width (truncated, e.g. at 80 columns).
  Setting `$PSDefaultParameterValues['Out-File:Width'] = 2000` affects `>` as well but increases memory use; some output also needs `Format-Table -AutoSize`.
- PowerShell 7.4 changed `>` for native-command stdout to preserve bytes (binary-safe); combining stderr into stdout makes the result string data.
- `36 > 42` is not a comparison: it writes `36` to a file named `42`. Use `-gt` / `-lt`.

## Checked
Method: 2026-11-08, read all three cited learn.microsoft.com pages in full (PowerShell-Docs 7.5 markdown). Rewritten to what they state. Removed unsupported claims from the earlier draft: the rotation and `finally` pattern, "transcripts capture native exe output only when written to the console", Write-Log helper claims, Windows Event Log cmdlets and the 5.1-only statement, and the `Tee-Object` "errors and warnings merged" example. Not executed.
