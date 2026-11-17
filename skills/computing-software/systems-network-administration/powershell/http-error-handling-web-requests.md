---
id: computing-software.systems-network-administration.powershell.http-error-handling-web-requests
name: http-error-handling-web-requests
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, invoke-restmethod, skiphttperrorcheck, http-status-codes, error-handling]
level: practitioner
status: verified
description: "Handle HTTP errors from Invoke-RestMethod and Invoke-WebRequest: reading status codes and error bodies in 5.1 and 7, SkipHttpErrorCheck and StatusCodeVariable."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP error handling for web requests

By default any non-2xx response throws a terminating error, and the response body (often containing the useful API
error message) is hidden inside the exception.

## PowerShell 7: avoid exceptions for HTTP status
`-SkipHttpErrorCheck` exists from PowerShell 7.0 (7.0 changelog: "Allow web cmdlets to ignore HTTP error statuses").
```powershell
$r = Invoke-RestMethod -Uri $uri -Headers $h -SkipHttpErrorCheck -StatusCodeVariable sc
switch ($sc) {
  {$_ -in 200..299} { $r }
  404 { Write-Warning "Not found: $uri" }
  429 { Start-Sleep -Seconds 30 }            # see Retry-After with -ResponseHeadersVariable
  default { throw "API error $sc : $($r.error.message)" }
}
```
`-ResponseHeadersVariable hdr` gives `Retry-After`, paging links, request IDs (a `Dictionary`; `$hdr['Retry-After']`
returned `3` for a 429 test response). With `-SkipHttpErrorCheck` a JSON error body was parsed into `$r` (`$r.err`).

## PowerShell 7: catching instead
```powershell
try { Invoke-RestMethod $uri }
catch {
  $code = $_.Exception.Response.StatusCode.value__        # 404 (exception type HttpResponseException)
  $body = $_.ErrorDetails.Message           # JSON error body as text
  throw "HTTP $code : $body"
}
```

## Windows PowerShell 5.1
No `-SkipHttpErrorCheck`. The exception is a `System.Net.WebException`. Reading the response stream is NOT reliable:
in 5.1.26100 the stream was already consumed (the `StreamReader` below returned an empty string) while
`$_.ErrorDetails.Message` held the body. Use ErrorDetails first and fall back to the stream:
```powershell
try { Invoke-RestMethod $uri }
catch [System.Net.WebException] {
  $resp = $_.Exception.Response
  $code = [int]$resp.StatusCode
  $body = $_.ErrorDetails.Message
  if (-not $body) { $body = (New-Object IO.StreamReader($resp.GetResponseStream())).ReadToEnd() }
  throw "HTTP $code : $body"
}
```
The same held for `Invoke-WebRequest` in 5.1.

## Retries
Retry only idempotent requests and transient codes (408, 429, 500, 502, 503, 504) with back-off. PowerShell 7 has
`-MaximumRetryCount` and `-RetryIntervalSec` built in, but they retry on every 400-599 and 304 (see
built-in-retries-maximumretrycount), and `-SkipHttpErrorCheck` does not stop that.

## Verify
- [ ] API errors surface the service's message and status code in logs; 4xx are not retried blindly.

## Checked
Ran against a local Python server on PowerShell 7.6.7 and Windows PowerShell 5.1.26100: `-SkipHttpErrorCheck -StatusCodeVariable
-ResponseHeadersVariable` (status 404, `$r.err`, header dictionary, `Retry-After` 3), the 7 catch block (`StatusCode.value__`
404, `ErrorDetails.Message` JSON body, `HttpResponseException`), the 5.1 `WebException` block (empty stream body, populated
`ErrorDetails.Message`; same for `Invoke-WebRequest`), and the retry interaction. The 7.0 version of `-SkipHttpErrorCheck` is from
the PowerShell 7.0 changelog.
