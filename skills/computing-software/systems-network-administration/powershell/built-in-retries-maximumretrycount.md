---
id: computing-software.systems-network-administration.powershell.built-in-retries-maximumretrycount
name: built-in-retries-maximumretrycount
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-rest, maximumretrycount, retryintervalsec, invoke-restmethod, http-429]
level: practitioner
status: verified
description: "Use Invoke-RestMethod and Invoke-WebRequest built-in retries (-MaximumRetryCount, -RetryIntervalSec) in PowerShell 7: which failures retry, Retry-After, and limits."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in retries with -MaximumRetryCount

PowerShell 7 web cmdlets can retry by themselves (the parameters exist in 7.6.7 and the current docs, and are absent
from Windows PowerShell 5.1):
```powershell
Invoke-RestMethod -Uri $uri -Headers $h -MaximumRetryCount 4 -RetryIntervalSec 5
```

## What is retried
- Responses with status codes **400-599** (client and server errors) and **304** are retried up to the count.
- Interval is fixed (`-RetryIntervalSec`, default 5 s: two retries took 10 s) between attempts; there's no exponential
  back-off. Each retry logs `Retrying after interval of N seconds. Status code for previous attempt: ...` with `-Verbose`.
- For **429 Too Many Requests** with a `Retry-After` header, the cmdlet waits the header's value instead of the fixed
  interval (`Retry-After: 3` with `-RetryIntervalSec 1` waited 3 s). This arrived in the 7.4 previews (changelog entry
  "WebCmdlets get Retry-After from headers if status code is 429").
- Network-level failures are not retried: a refused connection made one attempt in 7.6.7. Wrap with your own retry if
  you need that (see retry-logic-and-typed-catch). A 404 and a 400 were each retried (3 attempts for
  `-MaximumRetryCount 2`).

## Use it well
- Retrying 4xx (bad request, unauthorized, not found) wastes time. `-SkipHttpErrorCheck` does NOT prevent it: a 404
  with `-MaximumRetryCount 3 -SkipHttpErrorCheck` still made 4 requests and then returned the 404 response. For APIs
  that return 4xx for real errors, skip the built-in retry and use your own loop (see rest-pagination-and-rate-limits).
- Only for idempotent calls. A POST that created something on the first try and then timed out may create
  duplicates.
- Total worst-case wait = count x interval (+ Retry-After values): keep scheduled scripts under their timeout.

```powershell
$resp = Invoke-WebRequest -Uri $uri -MaximumRetryCount 3 -RetryIntervalSec 10 -SkipHttpErrorCheck
if ($resp.StatusCode -ge 400) { throw "Failed after retries: $($resp.StatusCode) $($resp.Content)" }   # runs after the last attempt
```

## Windows PowerShell 5.1
No such parameters. Use a loop with `try/catch` and back-off.

## Verify
- [ ] Against a test endpoint returning 503 then 200, the call succeeds and verbose output (`-Verbose`) shows the retry.
- [ ] A permanently failing endpoint makes `1 + -MaximumRetryCount` requests.

## Checked
Ran against a local Python HTTP server on PowerShell 7.6.7 (5.1 for the missing-parameter claim): 503,503,200 with
`-MaximumRetryCount 4 -RetryIntervalSec 1` (3 requests, verbose retry lines), 404/400/304 (each retried to the count),
429 with `Retry-After: 3` (waited 3 s), refused connection (single attempt), `-SkipHttpErrorCheck` with 404 (retries still
happen) and with 503-then-200, default interval (two retries = 10 s). Docs wording (400-599 and 304, Retry-After on 429)
read from the Invoke-RestMethod reference; the 7.4-preview changelog lines for Retry-After (#18717, #19622) confirmed.
The skill's earlier "7.1+" wording was not confirmable (docs for 7.1 are no longer published), so it was dropped.
