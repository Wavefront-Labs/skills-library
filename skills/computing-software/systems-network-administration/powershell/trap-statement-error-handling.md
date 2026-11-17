---
id: computing-software.systems-network-administration.powershell.trap-statement-error-handling
name: trap-statement-error-handling
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-error-handling, trap-statement, terminating-errors, continue, break]
level: advanced
status: verified
description: "Use the trap statement for script-wide error handling: how trap scopes work, continue vs break, and when trap beats or loses to try/catch."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_trap
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The trap statement

`trap` is a scope-wide handler for terminating errors: anywhere in the scope, a terminating error jumps to the
trap. Older than try/catch, still handy as a last-resort handler at the top of a script.

## Syntax
```powershell
trap [System.UnauthorizedAccessException] {
  Write-Warning "Access denied: $($_.TargetObject)"
  continue                       # resume at the statement after the one that failed
}
trap {
  Write-Error "Unhandled: $_"
  break                          # rethrow and stop the script (exit code 1 with -File)
}
```
- No keyword: error is written and execution continues with the next statement (like continue but with output).
- `continue`: suppress the error and continue after the failing statement.
- `break`: rethrow up the call stack.
- The most specific matching trap wins (about_Trap). Traps are hoisted: they apply to every statement in their scriptblock wherever they are written.

## Scope behaviour
A trap in a script catches errors from functions it calls if those functions don't handle them; `continue` then
resumes in the **script's** scope, after the call that failed (the rest of the function is skipped).
```powershell
trap { "trapped: $_"; continue }
function Test { 1/0; 'after in function' }   # not printed
Test; 'after call'                            # printed
```

## Non-terminating errors
Like catch, trap only sees terminating errors. Use `-ErrorAction Stop` or `$ErrorActionPreference = 'Stop'`.

Run on 7.6.7 and 5.1: `break` in the generic trap printed the message and ended the script with exit code 1; the no-keyword trap fired for `1/0`, the error was displayed, and the next statement still ran; a plain non-terminating `Get-Item` error did not invoke the trap until `$ErrorActionPreference = 'Stop'`; the `Test`/`after call` example printed only `after call`.

## When to use
- A top-of-script trap that logs and exits non-zero for anything unhandled (scheduled tasks, CI).
- try/catch for specific, local handling; trap's jump semantics are hard to read in long scripts.

## Verify
- [ ] An unhandled error in a scheduled script is logged by the trap and the task records exit code 1.
