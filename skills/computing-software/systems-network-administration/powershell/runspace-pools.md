---
id: computing-software.systems-network-administration.powershell.runspace-pools
name: runspace-pools
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-jobs, runspace-pool, parallelism, throttlelimit]
level: advanced
status: verified
description: "Run work in parallel with runspace pools for Windows PowerShell 5.1: create the pool, queue scripts with arguments, collect results and errors, and dispose cleanly."
sources:
  - https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.runspaces.runspacefactory.createrunspacepool
  - https://learn.microsoft.com/en-us/powershell/scripting/dev-cross-plat/performance/parallel-execution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runspace pools

In PowerShell 7 prefer `ForEach-Object -Parallel` or `Start-ThreadJob`. In Windows PowerShell 5.1 (no -Parallel; the ThreadJob
module is a separate Gallery install there) runspace pools give in-process parallelism much lighter than Start-Job (a
`Start-Job` round trip took 160-290 ms here against 7 ms for a thread job).

## Pattern
```powershell
$pool = [runspacefactory]::CreateRunspacePool(1, 16)       # min, max concurrent
$pool.Open()
$work = { param($Computer) [pscustomobject]@{Computer=$Computer; Up=(Test-Connection $Computer -Count 1 -Quiet)} }
$jobs = foreach ($c in $computers) {
  $ps = [powershell]::Create().AddScript($work).AddArgument($c)
  $ps.RunspacePool = $pool
  [pscustomobject]@{ PS = $ps; Handle = $ps.BeginInvoke(); Computer = $c }
}
$results = foreach ($j in $jobs) {
  try {
    $j.PS.EndInvoke($j.Handle)                        # blocks until this one finishes
    if ($j.PS.HadErrors) { $j.PS.Streams.Error | ForEach-Object { Write-Warning "$($j.Computer): $_" } }
  } finally { $j.PS.Dispose() }
}
$pool.Close(); $pool.Dispose()
```

## Things to know
- Each runspace is a fresh session: no access to your variables, functions or imported modules (a `$secret` variable read back empty and
  a caller function was not found). Pass data with `AddArgument` (positional) or `AddParameter` (named; both worked); load modules with an
  `InitialSessionState` (a scratch module `ModA` imported this way was usable in the pool):
```powershell
$iss = [initialsessionstate]::CreateDefault()
$iss.ImportPSModule('ActiveDirectory')    # any module on PSModulePath; importing an inbox module such as Microsoft.PowerShell.Utility only warns that it is already a snap-in
$pool = [runspacefactory]::CreateRunspacePool(1, 8, $iss, $Host)
```
- Shared objects across runspaces need thread-safe types (`[System.Collections.Concurrent.ConcurrentBag[object]]`).
- Always dispose `[powershell]` instances (the example does, in `finally`).
- Max runspaces: CPU-bound work = core count; I/O-bound (network calls) can go higher, but watch target systems.

## Verify
- [ ] Results count equals input count (16 jobs through a 16-slot pool returned 16 in 0.6 s); errors surfaced (`HadErrors` and `Streams.Error` were
      populated for a `Write-Error` script); memory stable over a large run.

## Checked
Ran the pool pattern unchanged on PowerShell 7.6.7 and Windows PowerShell 5.1.26100: three `Test-Connection -Quiet` targets (True, True, False), the
`InitialSessionState` pool with a scratch module, isolation of variables and functions, `AddArgument`/`AddParameter`, a 16-way pool
timing test, `HadErrors`/`Streams.Error`, and disposal. The `ActiveDirectory` module itself is not installed here, so the example name was
exercised with a scratch module instead. No claim about memory growth was tested, and it was removed.
