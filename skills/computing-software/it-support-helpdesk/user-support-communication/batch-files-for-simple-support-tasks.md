---
id: computing-software.it-support-helpdesk.user-support-communication.batch-files-for-simple-support-tasks
name: batch-files-for-simple-support-tasks
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, scripting, batch-script, bat-cmd, errorlevel, setlocal, cmd-variables, comptia-a-plus]
level: intro
status: draft
description: "Write small, safe .bat/.cmd scripts for support tasks: variables, errorlevel checks, quoting paths, logging, running elevated, and when to switch to PowerShell instead."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/if"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# batch-files-for-simple-support-tasks

Goal: automate a short, repeatable fix (clear a cache, map a drive, collect
info) with a batch file that fails safely (A+ 220-1202 4.8: .bat use cases
— basic automation, restarting machines, remapping drives, installing apps,
gathering information).

## Template
```bat
@echo off
setlocal EnableExtensions
set "LOG=%TEMP%\support-fix-%COMPUTERNAME%.log"
echo [%date% %time%] start >> "%LOG%"

rem Stop Teams before clearing its cache
taskkill /im ms-teams.exe /f >nul 2>&1

set "CACHE=%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams"
if exist "%CACHE%" (
  rd /s /q "%CACHE%"
  if errorlevel 1 (echo [%time%] cache delete failed >> "%LOG%" & exit /b 1)
)
echo [%date% %time%] done >> "%LOG%"
endlocal
exit /b 0
```

## Rules
- `@echo off`, `setlocal` (variables don't leak), `exit /b <code>` so
  callers (RMM/Intune) see success/failure.
- **Quote paths** (`"%CACHE%"`) — spaces break unquoted commands.
- Check results: `if errorlevel 1` (means ≥ 1) after commands that set it;
  `%ERRORLEVEL%` inside parenthesised blocks needs delayed expansion
  (`setlocal EnableDelayedExpansion` and `!ERRORLEVEL!`).
- Log to a file the desk can read.
- Use environment variables (`%USERPROFILE%`, `%LOCALAPPDATA%`,
  `%SystemDrive%`) instead of hard-coded drive letters and user names.
- Elevation: batch files don't self-elevate; run "as administrator" or via a
  tool that runs as SYSTEM — and remember SYSTEM's `%LOCALAPPDATA%` is not
  the user's.

## Good uses
Remapping drives (`net use`), collecting info (`ipconfig /all`,
`systeminfo` to a file), calling installers with silent switches, quick
cache clears, shortcuts to repetitive commands.

## When to switch to PowerShell
Anything with objects, error handling (`try/catch`), remote execution,
registry/CIM queries, JSON/CSV, or more than ~30 lines.

## Gotchas
- `rd /s /q` on a wrong variable (empty → current directory!) deletes the
  wrong tree — always `if exist` and test with `echo` first.
- Batch files from email/download are a common malware vector — only run
  scripts from your managed repository.

## Verify
Run on a test machine as the intended account; check exit code
(`echo %errorlevel%`) and log; the fix works.
