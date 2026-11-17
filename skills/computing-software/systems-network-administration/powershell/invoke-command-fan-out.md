---
id: computing-software.systems-network-administration.powershell.invoke-command-fan-out
name: invoke-command-fan-out
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, powershell-jobs, invoke-command-fanout, invoke-command, throttlelimit, pssession, pscomputername, unreachable-hosts, asjob]
level: advanced
status: docs-checked
description: "Run commands on hundreds of servers with Invoke-Command fan-out: ThrottleLimit, reusable sessions, separating unreachable hosts, -AsJob, timeouts and result shaping."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/invoke-command
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_output
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/new-pssessionoption
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fan-out Invoke-Command to many servers

`Invoke-Command -ComputerName a,b,c` runs against many computers at once; `-ThrottleLimit` is the maximum number of concurrent connections for the command, default 32 (omit it or pass 0 to use 32). The limit applies to the current command only, not to the session or the computer.

## The pattern
```powershell
$servers = Get-ADComputer -Filter 'OperatingSystem -like "*Server*" -and Enabled -eq $true' |
  Select-Object -ExpandProperty DNSHostName

$opt = New-PSSessionOption -OpenTimeout 15000 -OperationTimeout 300000 -MaxConnectionRetryCount 1
$results = Invoke-Command -ComputerName $servers -SessionOption $opt -ThrottleLimit 64 `
  -ErrorAction SilentlyContinue -ErrorVariable remErr -ScriptBlock {
    [pscustomobject]@{
      Hotfixes = (Get-HotFix | Measure-Object).Count
      LastBoot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
      Pending  = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
    }
  }

$results | Select-Object PSComputerName, Hotfixes, LastBoot, Pending | Export-Csv patch.csv -NoTypeInformation
$remErr | ForEach-Object {
  [pscustomobject]@{ Server = $_.TargetObject; Reason = $_.FullyQualifiedErrorId; Msg = $_.Exception.Message }
} | Export-Csv unreachable.csv -NoTypeInformation
```
- Results carry a `PSComputerName` property naming the remote computer that produced the data. Return objects, not formatted text, so you
  can tell which server said what. `-HideComputerName` only hides it from the display (it does not change the object) and is meant for a single remote computer.
- Check what `$remErr` actually contains in your environment before relying on `TargetObject` or specific error IDs; this skill's sources do not specify them.
- Compute what you need **remotely**; do not assume live methods on returned objects.

## Reuse sessions for several passes
```powershell
$s = New-PSSession -ComputerName $servers -SessionOption $opt -ThrottleLimit 64 -ErrorAction SilentlyContinue
Invoke-Command -Session $s { Import-Module WebAdministration }
Invoke-Command -Session $s { Get-Website | Select-Object Name, State }
$s | Remove-PSSession
```
Reuse sessions for multi-step work instead of reconnecting for each command.

## Long-running work
`Invoke-Command ... -AsJob -JobName patchscan` returns a job object immediately (the job is created locally and runs remotely); manage it with the `*-Job` cmdlets and get results with `Receive-Job`.
`-InDisconnectedSession` creates a persistent session on each remote computer, starts the command and disconnects; it returns a PSSession object, not the output. It cannot be combined with `-Session` or `-AsJob`. Reconnect later with `Connect-PSSession` or get results with `Receive-PSSession`.

## Tuning and limits
- Keep the script block lean; pass inputs with `-ArgumentList`.
- WinRM quotas on the target and chunking very large lists: check the WinRM documentation for your version (not covered by this skill's sources).

## Verify
- [ ] Count of results + count of errors equals count of targets.
- [ ] Every result row has `PSComputerName`.

## Checked
Date: 2026-11-02. Confirmed against the Invoke-Command reference (ThrottleLimit default 32 and scope, AsJob behaviour, InDisconnectedSession behaviour and restrictions, HideComputerName, ArgumentList), about_Remote_Output (PSComputerName) and New-PSSessionOption (OpenTimeout, OperationTimeout, MaxConnectionRetryCount exist as parameters). Removed: "No jobs or -Parallel needed", error-ID list, deserialisation depth claim, session-setup cost claim, Get-Job -IncludeChildJob, WinRM quota defaults, Test-WSMan/TCP pre-filter, chunk size of 500.
Method: documentation only; no commands were run.
