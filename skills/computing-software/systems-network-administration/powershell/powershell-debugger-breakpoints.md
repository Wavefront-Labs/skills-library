---
id: computing-software.systems-network-administration.powershell.powershell-debugger-breakpoints
name: powershell-debugger-breakpoints
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-error-handling, powershell-debugging, set-psbreakpoint, enter-pshostprocess, debug-runspace, debugger]
level: advanced
status: docs-checked
description: "Debug PowerShell with line, command and variable breakpoints, Action scriptblocks, console debugger commands, remote scripts, and Enter-PSHostProcess runspace debugging."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_debuggers
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/set-psbreakpoint
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enter-pshostprocess
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell debugging with breakpoints

## Set breakpoints
```powershell
Set-PSBreakpoint -Script sample.ps1 -Line 5                       # stops before line 5 runs
Set-PSBreakpoint -Script sample.ps1 -Command Increment            # before each call to the function
Set-PSBreakpoint -Script sample.ps1 -Command "write*"             # wildcard command names
Set-PSBreakpoint -Script sample.ps1 -Variable Server -Mode ReadWrite
Set-PSBreakpoint -Script test.ps1 -Command DiskTest -Action { if ($Disk -gt 2) { break } }
Set-PSBreakpoint -Script sample.ps1 -Line 1,14,19 -Column 2 -Action { & (log.ps1) }
Get-PSBreakpoint | Remove-PSBreakpoint                            # or Disable-/Enable-PSBreakpoint
```
- Each call creates one kind: line, command or variable (several targets per call are fine).
- Variable names are given without `$`. The default variable mode is Write, so execution stops just before the value changes.
- Line breakpoints are only for script files. Command and variable breakpoints without `-Script` apply to anything run in the session.
- Command breakpoint on a function with begin/process/end breaks at the first line of each section.
- `-Action` runs instead of (or to decide) stopping: `break` stops, `continue` is the default and does not stop; use it for conditions or logging.
- Breakpoints are read-only: to add an action, remove the breakpoint and create a new one.
- `-Runspace` sets a breakpoint in another runspace (example uses `Get-Runspace -Id 1`).
- `Set-PSBreakpoint` cannot set breakpoints on a remote computer; the page suggests copying the script locally. (The about page separately
  describes breakpoints inside an `Enter-PSSession`.)

## Debugger commands (console)
| Command | Action |
|---|---|
| `s` StepInto, `v` StepOver, `o` StepOut | step; StepOut in the main body runs to the end or next breakpoint |
| `c` Continue | run to the next breakpoint or the end |
| `l`, `l <m>`, `l <m> <n>` | list source (current line with 5 before and 10 after; 16 lines from m; n lines from m) |
| `k` | call stack (`Get-PSCallStack`) |
| `q`, Stop, Exit (also `t`) | stop the script and exit; with `Debug-Job`, Exit detaches and the job continues |
| `?`, `h` | help |
| Enter | repeats the last Step, StepOver or List |
| Ctrl+Break | break into a running script (closes the program in Windows PowerShell 2.0 to 4.0) |

- The prompt becomes `[DBG]:`; `$PSDebugContext` exists only while debugging and `$NestedPromptLevel` gives the nesting.
- `$_`, `$args`, `$input`, `$MyInvocation` and `$PSBoundParameters` show the debugger's own pipeline values. Copy them into new variables in the script before the breakpoint.
- Stepping into a statement with a redirection operator makes the debugger step over the rest of the script.
- In the ISE (Windows PowerShell only) use the Debug menu; PowerShell 6 and later use VS Code with the PowerShell extension.

## Remote and running processes
- Since 5.0 the debugger works for remote sessions: in `Enter-PSSession`, set breakpoints on the remote script path and run it; reconnecting
  to a disconnected session that hit a breakpoint starts the debugger automatically.
- `Enter-PSHostProcess -Id <pid>` (or `-Name`, `-HostProcessInfo`, `-CustomPipeName`) enters a local process that hosts PowerShell. You must be an
  Administrators member or the user who started it. Name matching more than one process is an error.
- Then `Get-Runspace` (a busy runspace shows `Availability` Busy; `ScriptStackTrace` may be present) and `Debug-Runspace -Id <n>` or `Enable-RunspaceDebug`.
- Finish: `exit` detaches the debugger, `exit` again leaves the process (or `Exit-PSHostProcess`); `q`/Stop kills the script. The cmdlet can be used inside a remote session to attach to a process on that computer. Supported on non-Windows since 6.2.

## Other tools named on the about page
`Set-PSDebug` (basic stepping and tracing), `Set-StrictMode`, and diagnostic statements with `Write-Debug`, `Write-Verbose`, `Write-Warning`, `Write-Host`.

## Checked
Method: 2026-11-08, read about_Debuggers in full, Set-PSBreakpoint through its examples (description, syntax, examples 1 to 8) and Enter-PSHostProcess through its examples and first parameters (7.5 markdown). Rewritten to what they state. Removed unsupported claims from the earlier draft: `Wait-Debugger`, `Debug-Job` internals, `Get-PSHostProcessInfo` use, the `d` detach key, VS Code shortcuts and F9/F5 behaviour, `Set-PSDebug -Trace` levels, and "PSScriptAnalyzer will not catch it". Not executed.
