---
id: computing-software.systems-network-administration.powershell.thread-jobs
name: thread-jobs
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-jobs, background-jobs, start-threadjob, thread-jobs, start-job, receive-job, wait-job, threadjob-module]
level: practitioner
status: verified
description: "Run work concurrently with Start-ThreadJob vs Start-Job: throttling, collecting results and errors, timeouts, cleanup, and when a process job is still needed."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_thread_jobs
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs
  - https://learn.microsoft.com/en-us/powershell/module/threadjob/start-threadjob
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread jobs and background jobs

| | `Start-Job` | `Start-ThreadJob` |
|---|---|---|
| Runs in | new `pwsh`/`powershell` **process** | new **runspace** in the same process |
| Startup cost | a few hundred ms each (160-290 ms measured in 5.1 and 7.6.7) | milliseconds (7-21 ms measured) |
| Output | serialised (deserialised objects, no methods: a `Get-Process` result came back as `PSObject`) | live objects (`System.Diagnostics.Process`) |
| Isolation | crash or memory leak cannot hurt caller | shares process; a hang or crash affects caller |
| Throttle | none (you manage it) | `-ThrottleLimit` (default 5), queued beyond it |
| Availability | built in | bundled with PS 6.1+ (7.6.7 has `Microsoft.PowerShell.ThreadJob` 2.2.0 in `$PSHOME\Modules`; 6.1 changelog: "Add ThreadJob module package"); on 5.1 install `ThreadJob` or `Microsoft.PowerShell.ThreadJob` from the Gallery (both pages exist) |

Default to thread jobs. Use `Start-Job` when you need a different PowerShell version
(`-PSVersion 5.1` from PS 7), different credentials (`-Credential`), or process isolation for
unstable modules.

## Fan out, wait with timeout, collect
```powershell
$jobs = foreach ($s in $servers) {
  Start-ThreadJob -Name $s -ThrottleLimit 20 -ArgumentList $s -ScriptBlock {
    param($name)
    Test-NetConnection $name -Port 5985 -InformationLevel Quiet
  }
}
$done = $jobs | Wait-Job -Timeout 120
$jobs | Where-Object State -eq 'Running' | ForEach-Object { Write-Warning "$($_.Name) timed out"; Stop-Job $_ }

$results = foreach ($j in $jobs) {
  [pscustomobject]@{
    Server = $j.Name
    State  = $j.State
    Open   = Receive-Job $j -ErrorVariable jerr -ErrorAction SilentlyContinue
    Error  = $jerr.Exception.Message -join '; '
  }
}
$jobs | Remove-Job -Force
```
- The thread-job throttle applies session-wide, not per call; pass the same `-ThrottleLimit` every time (ten separate calls of a
  0.5 s job took 1.1 s at the default 5, 2.6 s with `-ThrottleLimit 2` on each call and 0.6 s with 10).
- `Receive-Job` drains output; a second call returns nothing unless you used `-Keep`.
- Job errors do not throw in the caller. A script block that `throw`s ends `Failed` with the message in
  `$job.JobStateInfo.Reason.Message` (`$job.ChildJobs[0].Error` was EMPTY in that case); a `Write-Error` leaves the job `Completed` and the
  record comes out of `Receive-Job -ErrorVariable jerr -ErrorAction SilentlyContinue`; `Receive-Job -ErrorAction Stop` re-throws.
- `Receive-Job -Wait -AutoRemoveJob` is the one-liner when you just want everything.
- Always `Remove-Job`; finished jobs keep their output in memory for the session.

## Variables
Script blocks run in a new runspace: caller variables are not visible (`$v` read back empty; `$using:v` returned the value). Pass with
`-ArgumentList` + `param()` or `$using:var` (see the using-scope skill). A module imported in the
caller by explicit path was **not** visible in a thread job (`Get-Command` False) but was with `-InitializationScript { Import-Module ... }`;
modules on `$env:PSModulePath` can still autoload.

## Thread safety
Thread jobs share the process: do not write the same file or non-thread-safe collection from
several jobs. Return objects and aggregate in the caller, or use
`[System.Collections.Concurrent.ConcurrentBag[object]]`.

## Verify
- [ ] Total runtime is roughly (items / throttle) x per-item time, not the sum.
- [ ] Failed and timed-out items appear in the results, not silently missing.
- [ ] `Get-Job` is empty at the end of the script.

## Checked
Ran on PowerShell 7.6.7 (Windows PowerShell 5.1 for `Start-Job` timing): fan-out/`Wait-Job -Timeout`/`Receive-Job -ErrorVariable`/`Remove-Job` using the skill's
code against a local port, throttle timings, `-Keep` and draining, `throw` versus `Write-Error` job states, `$using:`, `-InitializationScript`,
module visibility, `Start-Job -PSVersion 5.1` (returned 5.1), object types from each job kind, start-up times, and `Stop-Job` after a timeout.
The ThreadJob 6.1 packaging comes from CHANGELOG/6.1.md and the Gallery pages. `Test-NetConnection` was pointed at `127.0.0.1` on a test port, not at WinRM 5985.
