---
id: computing-software.systems-network-administration.powershell.foreach-object-parallel
name: foreach-object-parallel
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-jobs, foreach-parallel, throttlelimit, foreach-object, runspaces, concurrency, pwsh]
level: practitioner
status: verified
description: "Parallelise loops with ForEach-Object -Parallel in PowerShell 7: choosing ThrottleLimit, $using:, thread-safe aggregation, -AsJob, -TimeoutSeconds and when not to use it."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object
  - https://devblogs.microsoft.com/powershell/powershell-foreach-object-parallel-feature/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ForEach-Object -Parallel (PowerShell 7+)

Each input runs in a runspace from a pool, `-ThrottleLimit` at a time (default **5**: ten 0.5 s sleeps took 1.1 s at the
default and 0.6 s at 10). Not available in Windows PowerShell 5.1 (the call fails; use thread jobs or runspaces there).

```powershell
$cutoff = (Get-Date).AddDays(-30)
$servers | ForEach-Object -Parallel {
  $s = $_
  try {
    $os = Get-CimInstance Win32_OperatingSystem -ComputerName $s -ErrorAction Stop -OperationTimeoutSec 20
    [pscustomobject]@{ Server = $s; LastBoot = $os.LastBootUpTime; Stale = $os.LastBootUpTime -lt $using:cutoff }
  } catch {
    [pscustomobject]@{ Server = $s; LastBoot = $null; Stale = $null; Error = $_.Exception.Message }
  }
} -ThrottleLimit 32 -TimeoutSeconds 600 | Export-Csv boot.csv -NoTypeInformation
```

## Choosing ThrottleLimit
- I/O-bound (network calls, remote queries, REST): size it to what the remote side and API rate limits allow rather
  than local CPU; there is no measured sweet spot here, so tune with `Measure-Command`.
- CPU-bound local work: about `[Environment]::ProcessorCount` is the usual starting point.
- Each runspace costs startup time and memory. For tiny per-item work the overhead makes `-Parallel` **slower** than a
  plain loop (200 trivial items: 231 ms versus 17 ms). Batch items, or don't parallelise.

## Rules
- The script block cannot see caller variables except via `$using:var`. Values are passed by
  reference for reference types: mutating `$using:list` from many threads is a race.
- Thread-safe aggregation, when you must share state:
  ```powershell
  $bag = [System.Collections.Concurrent.ConcurrentDictionary[string,int]]::new()
  1..100 | ForEach-Object -Parallel { $d = $using:bag; [void]$d.TryAdd("$_", $_ * 2) } -ThrottleLimit 10
  ```
  Usually better: emit objects and let the pipeline collect them.
- Output order is **not** preserved (1..20 came back as `2,5,7,1,3,...`). Sort afterwards if order matters.
- Common parameters such as `-ErrorAction` are rejected in the `-Parallel` parameter set; set
  `$ErrorActionPreference` inside the block instead.
- Functions and modules from the caller are not available. Import modules inside the block,
  or pass a function's definition: `$f = ${function:Get-Thing}.ToString()` then
  `${function:Get-Thing} = $using:f`.
- `-TimeoutSeconds` stops all remaining work when it expires (running blocks are stopped): three 5 s sleeps with
  `-TimeoutSeconds 1` returned nothing after 1 s, with `The pipeline has been stopped` errors in 7.6.7.
- `-AsJob` returns one `PSTaskJob` with child jobs, for use with `Wait-Job`/`Receive-Job`.
- `-UseNewRunspace` gives a fresh runspace per item instead of reusing pooled ones (runspace ids repeated without it and
  were all different with it at `-ThrottleLimit 1`; a `$global:` counter did not leak between items in the plain run, so
  leakage is worth testing, not assuming).

## Verify
- [ ] Runtime drops versus sequential for the real workload (measure with `Measure-Command`).
- [ ] Unreachable inputs appear in output with an error rather than vanishing.

## Checked
Ran on 7.6.7 (5.1 only for the failure): the `$using:cutoff` example with local and unreachable inputs (each produced an
object, unreachable ones with an error text), throttle timings, ConcurrentDictionary aggregation (100 keys), tiny-work
overhead, unordered output, function-not-found and the `${function:Get-Thing}` workaround, `-TimeoutSeconds`, `-AsJob` with
`Receive-Job -Wait -AutoRemoveJob`, `-UseNewRunspace` (runspace InstanceIds), and the rejected `-ErrorAction`. The earlier "7.1+" tag on `-UseNewRunspace` was dropped as unconfirmed. Remote CIM calls to real servers were not possible here.
