---
id: computing-software.general-digital-literacy.file-management.copying-large-folders-reliably
name: copying-large-folders-reliably
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, robocopy, rsync, large-copy, resume-copy]
level: intro
status: docs-checked
description: "Copy or move hundreds of gigabytes between drives on Windows with robocopy: restartable mode, limited retries, a log to check, and the /MIR trap."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Copy large folders reliably

For a big copy (old PC to external drive, photo archive), use a tool that restarts and logs. Microsoft recommends always creating a log file to check afterwards.

## Windows: robocopy (built in)
```
robocopy "<SOURCE>\Photos" "<BACKUP_DRIVE>\Photos" /E /Z /R:2 /W:5 /MT:8 /LOG:"<LOG_FILE>" /TEE
```
- `/E` copies subfolders including empty ones. `/Z` restartable mode: an interrupted file copy can pick up where it left off.
- `/R:2 /W:5` retry twice, waiting 5 seconds. The defaults are 1,000,000 retries and 30 seconds.
- `/MT:8` multi-threaded with 8 threads (n is 1 to 128). `/LOG:file` writes status to a file; `/TEE` also writes to the console.
- Running it again when files already exist in the destination skips them (exit code 0: "the copy operation was skipped").
- **`/MIR` is `/E` plus `/PURGE`**: it deletes destination files that no longer exist in the source. Never swap source and destination with `/MIR`.
- Exit code 8 or higher means at least one failure; read the log.

## Verify
- [ ] Exit code below 8, log shows no failures, and a few files open from the copy.

## Checked
2026-11-01. Confirmed against Microsoft Learn "robocopy": /E, /Z, /R and /W defaults, /MT range, /LOG, /TEE, /MIR, /PURGE, exit codes, log recommendation. Removed: rsync and Finder section, FAT32 4 GB note, "exit codes 0-3 are success", file-count comparison advice (no page read).
Method: documentation only; no commands were run.
