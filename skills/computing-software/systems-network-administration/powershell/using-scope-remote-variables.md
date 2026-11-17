---
id: computing-software.systems-network-administration.powershell.using-scope-remote-variables
name: using-scope-remote-variables
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-jobs, ps-remoting, using-scope, argumentlist, invoke-command, foreach-parallel, scopes]
level: practitioner
status: gated
description: "Pass local values into remote commands, jobs and parallel blocks with $using: or -ArgumentList, and handle serialisation, functions and the cases $using cannot do."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_variables
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scopes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $using: scope and passing variables

Script blocks run by `Invoke-Command -ComputerName/-Session`, `Start-Job`, `Start-ThreadJob`,
`ForEach-Object -Parallel` and DSC run in **another runspace**. Local variables are not there.

## $using: (tested in 5.1 and 7.6.7)
```powershell
$svc = 'Spooler'; $days = 7
Invoke-Command -ComputerName $servers {
  Get-Service -Name $using:svc
  Get-WinEvent -FilterHashtable @{ LogName='System'; StartTime=(Get-Date).AddDays(-$using:days) } -MaxEvents 5
}
```
- Values are copied when the command starts. For remoting and `Start-Job` they are
  **serialised** (deserialised copies, no methods: a process object arrived as `PSObject` with 2 methods; depth limits
  not tested); thread jobs and `-Parallel` get references to the same live object (a `List[int]` passed with `$using:` was
  mutated by both, but not by `Start-Job`).
- Read-only: `$using:x = 1` is a parse-time error ("The assignment expression is not valid"). Assign to a local inside the block.
- Keep it to a plain variable reference (property access and indexing, such as `$using:cfg.Paths[0]`, worked in `Start-Job` and a
  PSSession). For anything more complex, compute a local first (`$p = $cfg.Paths[0]`) and pass `$using:p`.
- Not usable in local script blocks run with `&` or `Invoke-Command` without a target (error: "A Using variable cannot be retrieved ...
valid only if the script block is invoked on a remote computer"); `Enter-PSSession` interactive commands (gated: unconfirmed, source is paywalled or blocked).

## -ArgumentList + param()
```powershell
Invoke-Command -ComputerName $servers -ArgumentList $svc, $days -ScriptBlock {
  param($Name, $Days)
  Get-Service -Name $Name
}
```
Positional and explicit; required for script files (`-FilePath`) (gated: unconfirmed, source is paywalled or blocked) and older targets (gated: unconfirmed, source is paywalled or blocked). An array given to `-ArgumentList` is spread over the
parameters (`count=1` for the first element of a 3-item array); pass it as one argument with the unary comma, `-ArgumentList (,$list)` (`count=3`).

## Passing functions
```powershell
function Get-Uptime { (Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime }
$def = ${function:Get-Uptime}.ToString()
Invoke-Command -ComputerName $servers {
  ${function:Get-Uptime} = [scriptblock]::Create($using:def)
  Get-Uptime
}
```
For anything bigger, install a module on the targets or copy it with `Copy-Item -ToSession` (the parameter exists; no copy was run).

## Credentials and secrets
`$using:cred` passed a `PSCredential` intact into a PSSession (`PSCredential` type, user name readable). Whether the password is encrypted on the wire (gated: unconfirmed, source is paywalled or blocked). Never embed plaintext passwords in the script block string.

## Common mistakes
- `"$using:var"` inside a string worked here (`Spooler`); the subexpression form `"$($using:var)"` is still clearer.
- Large objects via `$using:` are serialised per target; for 500 servers that is 500 copies.
  Ship only what you need.

## Verify
- [ ] The remote block returns values derived from the local variables on every target.
- [ ] No local-only types (live COM/.NET handles) are passed to remote targets.

## Checked
Ran on PowerShell 7.6.7: `Start-Job`, `Start-ThreadJob` and `ForEach-Object -Parallel` with `$using:`, a real PSSession created with `New-PSSession -UseWindowsPowerShell`
(local out-of-process Windows PowerShell session) with the skill's `$using:` examples, `-ArgumentList` with and without the unary comma,
the function-copy pattern, `PSCredential`, serialised process object, indexing on `$using:cfg`, string interpolation, the parse-time
error for assignment, and the local `&` error. Remote targets (`-ComputerName`) and `Enter-PSSession` were not available (no WinRM listener).
