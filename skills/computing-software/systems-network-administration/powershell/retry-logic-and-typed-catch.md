---
id: computing-software.systems-network-administration.powershell.retry-logic-and-typed-catch
name: retry-logic-and-typed-catch
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-error-handling, retry-logic, exponential-backoff, typed-catch, transient-errors]
level: practitioner
status: verified
description: "Write retry loops with exponential back-off and typed catch blocks so transient failures (network, locks, throttling) retry and real errors fail fast."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry patterns and typed catch blocks

## Typed catch: handle only what you understand
```powershell
try {
  $r = Invoke-RestMethod $uri -ErrorAction Stop
}
catch [System.Net.Http.HttpRequestException], [System.Net.WebException] {
  # network-level problem: maybe retry
}
catch [System.IO.IOException] {
  # file locked
}
catch {
  throw      # anything else: rethrow unchanged
}
```
On Windows PowerShell 5.1 `[System.Net.Http.HttpRequestException]` is not resolvable until the assembly is loaded (`Unable to find type [System.Net.Http.HttpRequestException]`, which also breaks the `Invoke-WithRetry` default parameter): run `Add-Type -AssemblyName System.Net.Http` first. `Invoke-RestMethod` to a refused connection throws `WebException` on 5.1 and `HttpRequestException` on 7.6.7, so list both when the script runs on both.

Find the type to catch from a real failure: `$Error[0].Exception.GetType().FullName` (and `.InnerException`).

## Generic retry helper
```powershell
function Invoke-WithRetry {
  param([scriptblock]$Script, [int]$MaxAttempts = 5, [int]$BaseDelaySec = 2,
        [type[]]$RetryOn = @([System.Net.Http.HttpRequestException],[System.IO.IOException],[System.TimeoutException]))
  for ($i = 1; ; $i++) {
    try { return & $Script }
    catch {
      $ex = $_.Exception
      $transient = $RetryOn | ? { $ex -is $_ -or $ex.InnerException -is $_ }
      if (-not $transient -or $i -ge $MaxAttempts) { throw }
      $delay = [math]::Min(60, $BaseDelaySec * [math]::Pow(2, $i - 1)) + (Get-Random -Maximum 1000) / 1000
      Write-Warning "Attempt $i failed: $($ex.Message). Retrying in $([math]::Round($delay,1))s"
      Start-Sleep -Seconds $delay
    }
  }
}
Invoke-WithRetry { Copy-Item '<SRC>\big.vhdx' '\\fs01\vm\' -ErrorAction Stop }
```
Jitter avoids many clients retrying in lockstep.

Run on 7.6.7: the helper succeeded on attempt 3 after two simulated `IOException`s, gave up with the original exception at `MaxAttempts`, and made one attempt only for a permanent `ItemNotFoundException` (not in `RetryOn`).

## Rules
- Retry only idempotent operations (GET, copy that overwrites), not "create user" without a check.
- Honour `Retry-After` on HTTP 429/503 (use `-ResponseHeadersVariable` in PS 7).
- Cap total time; log each attempt.
- Make non-terminating errors terminating with `-ErrorAction Stop`, or catch never fires.

## Verify
- [ ] Simulated transient failure (unplug network briefly) succeeds after a retry; a permanent error (bad path) fails on the first attempt.
