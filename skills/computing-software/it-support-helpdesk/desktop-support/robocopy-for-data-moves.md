---
id: computing-software.it-support-helpdesk.desktop-support.robocopy-for-data-moves
name: robocopy-for-data-moves
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, command-line-tools, robocopy, data-migration, mirror, copy-permissions, robocopy-exit-codes, multithreaded-copy, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Move user and share data reliably with robocopy: the right switches for copy vs mirror, permissions and timestamps, retries, logging, exit codes, and the /MIR deletion trap."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/return-codes-used-robocopy-utility"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# robocopy-for-data-moves

Goal: copy large folders between disks, PCs or servers with retries, logging and the
right metadata, and never delete data by accident.

## Common command lines
```cmd
:: user data to a new PC/share, keep timestamps, retry briefly, log
robocopy "\\OLDPC\c$\Users\sam\Documents" "<drive>\Migrate\sam\Documents" /E /COPY:DAT /DCOPY:DAT /R:2 /W:5 /MT:16 /XJ /LOG:%TEMP%\sam-docs.log /TEE /NP

:: file server migration keeping NTFS ACLs and owners (run as admin, backup rights)
robocopy \\fs01\dept \\fs02\dept /E /COPYALL /DCOPY:DAT /B /R:1 /W:1 /MT:32 /LOG:%TEMP%\dept.log

:: incremental re-sync before cut-over (mirror) - deletes extra files in destination!
robocopy \\fs01\dept \\fs02\dept /MIR /COPYALL /DCOPY:DAT /B /R:1 /W:1 /MT:32 /LOG+:%TEMP%\dept.log
```
(Paths are examples; adjust source/destination.)

## Switches that matter
| Switch | Meaning |
|---|---|
| `/E` | subdirectories, including empty ones |
| `/MIR` | mirror = `/E` plus `/PURGE`; `/PURGE` deletes destination files and directories no longer in the source |
| `/COPY:<flags>` | D data, A attributes, T timestamps, S ACLs, O owner, U auditing; default is DAT |
| `/COPYALL` | equivalent to `/COPY:DATSOU` |
| `/DCOPY:<flags>` | directory properties (D, A, T, E, X); default is DA |
| `/B` / `/ZB` | backup mode (overrides ACLs that would block access) / restartable mode that falls back to backup mode if access is denied |
| `/R:n /W:n` | retries (default 1,000,000) and wait in seconds (default 30) |
| `/MT:n` | multithreaded, n from 1 to 128, default 8; not usable with `/IPG` or `/EFSRAW`; redirect output with `/LOG` for better performance |
| `/XJ` | exclude junction points (included by default) |
| `/XD` `/XF` | exclude directories / files |
| `/L` | list only: nothing is copied, deleted or time stamped (a dry run) |
| `/LOG:` `/LOG+:` `/TEE` `/NP` | log file (overwrite / append), also echo to console, hide progress |

Microsoft recommends always writing a log file you can review after the run.

## Exit codes
0 = nothing copied, files already in destination; 1 = all files copied; 2 = extra files in
destination, none copied; 3 = some copied plus extra files, no failures; 5 = some copied,
some mismatched; 6 = extra and mismatched files, none copied; 7 = copied, mismatched and
extra; 8 and above = at least one failure. A script that treats only 0 as success will
mis-handle codes 1 to 7.

## Gotchas
- With `/MIR`, swapping source and destination deletes the real data; run with `/L` first
  and read the summary.
- With the default `/R` and `/W`, a locked file can stall the run for a very long time.

## Checked
2026-11-01. Confirmed on the Microsoft Learn robocopy page and the robocopy return codes
article: every switch and default in the table, exit codes. Removed: the CompTIA exam
reference, the multithreading speed claim, Outlook file, AppData, long path and profile
advice, and the dry-run verify command, which those pages do not state.
Method: documentation only; no commands were run.
