---
id: computing-software.systems-network-administration.powershell.variable-scopes-and-dot-sourcing
name: variable-scopes-and-dot-sourcing
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-functions, about-scopes, dot-sourcing, script-scope, global-scope]
level: practitioner
status: verified
description: "Understand PowerShell scopes: global, script, local and private, scope modifiers, dot-sourcing, module scope, and the bugs they cause in scripts and functions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scopes
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scripts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable scopes and dot-sourcing

## Rules
- Each script, function and scriptblock gets a **child scope**. Children can **read** parent variables; an
  assignment creates a new local variable instead of changing the parent's.
- Scopes: `global:` (session), `script:` (the script file or module), `local:` (current), `private:` (not visible
  to children), `using:` (remote/parallel, see using-scope-remote-variables).
- Modules have their own script scope; module functions don't see the caller's variables (good).

```powershell
$count = 0
function Add-One { $count++ }           # increments a new local $count; outer stays 0
function Add-OneFixed { $script:count++ }
Add-One; Add-OneFixed; $count           # 1
```
Better: return values instead of mutating outer scope (`$count = Get-NextCount $count`).

## Dot-sourcing
`. .\helpers.ps1` runs the script in the **current** scope, so its functions and variables stay after it ends.
Without the dot, they vanish when the script exits.
```powershell
. "$PSScriptRoot\lib\Get-Inventory.ps1"
```
Dot-sourcing a function call (`. Get-Thing`) runs the function in the caller's scope: rarely what you want.

## Common bugs
- A variable set in a `ForEach-Object` scriptblock is visible after (same scope), but in `ForEach-Object -Parallel`
  it isn't (separate runspace). `& $scriptblock` runs in a child scope (variables vanish), `. $scriptblock` in the current one.
- `$private:x` is not visible to a function called from the scope that set it.
- Functions defined in a script run without dot-sourcing are gone in the interactive shell afterwards.
- `Set-StrictMode -Version Latest` catches reads of never-assigned variables that would otherwise be `$null`.
- `$global:` in modules makes hidden coupling; avoid.

## Inspect
```powershell
Get-Variable -Scope 1 count        # parent scope
Get-Variable -Scope Script
```

All examples here were run on 7.6.7 (`$count` ends at 1; dot-sourced function and variable remain, the non-dotted run leaves nothing; `Get-Variable -Scope 1` reads the caller's variable).

## Verify
- [ ] Scripts work when run fresh (`pwsh -NoProfile -File script.ps1`), not only in a warm session.
