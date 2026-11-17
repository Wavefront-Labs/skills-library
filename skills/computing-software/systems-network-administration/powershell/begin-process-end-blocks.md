---
id: computing-software.systems-network-administration.powershell.begin-process-end-blocks
name: begin-process-end-blocks
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, advanced-functions, cmdletbinding, begin-process-end, process-block, clean-block, pipeline, streaming]
level: practitioner
status: verified
description: "Structure pipeline functions with begin, process, end and clean blocks: one-time setup, per-object streaming, aggregation, cleanup, and the $input/$_ traps."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_methods
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# begin / process / end (and clean)

| Block | Runs | Use for |
|---|---|---|
| `begin` | once, before the first input; pipeline parameters **not yet bound** | open connections, compile regex, init collections |
| `process` | once per piped object (once total if nothing is piped) | the actual work, emit output immediately |
| `end` | once after all input | aggregate output, summary |
| `clean` (PS 7.3+) | always, even on Ctrl+C, `Select-Object -First` stop, or terminating error | dispose sessions, delete temp files |

```powershell
function Test-Port {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory, ValueFromPipeline)][string]$ComputerName,
    [int]$Port = 443,
    [int]$TimeoutMs = 1000
  )
  begin   { $results = [System.Collections.Generic.List[object]]::new() }
  process {
    $tcp = [System.Net.Sockets.TcpClient]::new()
    try {
      $ok = $tcp.ConnectAsync($ComputerName, $Port).Wait($TimeoutMs)
      $r  = [pscustomobject]@{ ComputerName = $ComputerName; Port = $Port; Open = $ok }
      $results.Add($r)
      $r                                  # stream, so downstream cmdlets start immediately
    } catch { Write-Error -ErrorRecord $_ }
    finally { $tcp.Dispose() }
  }
  end     { Write-Verbose "$(@($results | Where-Object Open).Count)/$($results.Count) open" }
}
'web1','web2','db1' | Test-Port -Port 1433 -Verbose
```

## Traps
- In `begin`, a `ValueFromPipeline` parameter is empty; only non-pipeline parameters are set.
- A function without named blocks puts all code in `end`; with piped input, only the last
  object is in the parameter. `$input` (an enumerator of all input) exists in `end`, but
  enumerate it only once.
- Collecting everything in `process` and emitting in `end` breaks streaming and memory use;
  only do that when you must sort or aggregate.
- Avoid `$array += $x` in `process` (copies the array each time). Use `List[T].Add()`.
- `return` in `process` ends **that iteration** only, not the function.
- Upstream `Select-Object -First 1` stops the pipeline: `end` does not run, but `clean` does
  (PS 7.3+). On older versions put cleanup in `try/finally` inside `process`.
- Inside `process`, `$_` is the current pipeline object; prefer the named parameter, which
  also works when the function is called with `-ComputerName a,b` (loop over it).

Checked on 7.6.7 (and `end` on 5.1): upstream `Select-Object -First 1` skips `end` but runs `clean`; in 5.1 a `try/finally` in `process` runs. A name that does not resolve makes `ConnectAsync(...).Wait()` throw, which the `catch` turns into an error.

## Verify
- [ ] Piped and direct calls return identical output.
- [ ] `... | Test-Port | Select-Object -First 1` returns quickly and leaves no open sockets.
