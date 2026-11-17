---
id: computing-software.systems-network-administration.powershell.rest-pagination-and-rate-limits
name: rest-pagination-and-rate-limits
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, invoke-restmethod, rest-pagination, rate-limiting, retry-after, http-429, followrellink, odata-nextlink, exponential-backoff]
level: advanced
status: verified
description: "Fetch every page from REST APIs in PowerShell (nextLink, Link headers, offset, cursor) and handle 429/503 with Retry-After, backoff and the PS 7 built-in retry options."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod
  - https://learn.microsoft.com/en-us/graph/paging
  - https://learn.microsoft.com/en-us/graph/throttling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pagination and rate limits

## Pattern 1: next link in the body (OData / Graph / Azure)
```powershell
$uri = 'https://graph.microsoft.com/v1.0/devices?$select=displayName,operatingSystem'
$all = [System.Collections.Generic.List[object]]::new()
do {
  $page = Invoke-RestMethod -Uri $uri -Headers $h
  $all.AddRange([object[]]$page.value)
  $uri = $page.'@odata.nextLink'
} while ($uri)
```
Follow the next link **as given**: it encodes the skip token and query; do not rebuild it. (A local server returning `value` and
`@odata.nextLink` over three pages, the last with a single item, gave 7 records; `[object[]]$page.value` also worked for a one-element page.)
`displayName` and `operatingSystem` are properties of the Graph device resource (Learn). Page-size limits (`$top`) differ per Graph
resource; read the endpoint's page for its maximum.

## Pattern 2: RFC 8288 Link header (GitHub, many SaaS APIs)
```powershell
Invoke-RestMethod -Uri 'https://api.github.com/orgs/<ORG>/repos?per_page=100' -Headers $h -FollowRelLink -MaximumFollowRelLink 50
```
PS 6+ `-FollowRelLink` follows `rel="next"` automatically and emits one result per page (three page objects for a three-page test; array
pages come out as arrays, so flatten with `| ForEach-Object { $_ }`); `-MaximumFollowRelLink 2` returned two pages. GitHub's docs give 100 as the
maximum `per_page` for most endpoints and say larger values are silently reduced. In 5.1 there is no `-FollowRelLink`; parse
`Invoke-WebRequest` `.Headers.Link` (it held `<http://...?p=2>; rel="next"`).

## Pattern 3: offset/limit or cursor
```powershell
$offset = 0; $limit = 500
do {
  $page = Invoke-RestMethod "https://api.vendor.example/v1/tickets?offset=$offset&limit=$limit" -Headers $h
  $page.items
  $offset += $limit
} while ($page.items.Count -eq $limit)
```
Prefer cursors when offered: offsets skip or duplicate rows if data changes during the walk.

## Rate limits: 429 and 503
```powershell
function Invoke-ApiWithRetry {
  param([string]$Uri, [hashtable]$Headers, [int]$MaxRetry = 6)
  for ($i = 0; ; $i++) {
    try { return Invoke-RestMethod -Uri $Uri -Headers $Headers }
    catch {
      $resp = $_.Exception.Response
      $code = [int]$resp.StatusCode
      if ($code -notin 429, 500, 502, 503, 504 -or $i -ge $MaxRetry) { throw }
      $ra = $resp.Headers.RetryAfter.Delta.TotalSeconds            # PS 7 (HttpResponseMessage)
      if (-not $ra) { $ra = [math]::Min(60, [math]::Pow(2, $i)) + (Get-Random -Maximum 1.0) }
      Write-Verbose "HTTP $code, retry $($i+1) in $ra s"
      Start-Sleep -Seconds $ra
    }
  }
}
```
- Honour `Retry-After` exactly when present; otherwise exponential backoff with jitter.
- PowerShell 7 built-in: `-MaximumRetryCount 5 -RetryIntervalSec 10` retries on 304 and any
  400-599 status (including 401/403, which never recover) at a fixed interval, and honours `Retry-After` on 429 (see
  built-in-retries-maximumretrycount). Use the custom loop for selective codes, jitter or logging.
- In 5.1 `$_.Exception.Response` is an `HttpWebResponse`: read `$resp.Headers['Retry-After']`. The loop above, run unchanged in 5.1,
  ignored `Retry-After: 3` and backed off about 1.4 s because `.Headers.RetryAfter` does not exist there; in 7.6.7 it waited exactly 3 s.
- Do not retry non-idempotent POSTs blindly on 5xx; the first attempt may have succeeded.

## Stay under the limit
- Ask for fewer, bigger pages (`per_page=100` on GitHub; the largest `$top` the Graph endpoint allows) and only the fields you need (`$select`).
- Use delta/changes endpoints for repeated syncs instead of full walks.
- Batch where supported (Graph JSON batching takes up to 20 individual requests per batch, per Learn).
- When parallelising (`ForEach-Object -Parallel`), keep the throttle low; parallel callers
  share the same app/tenant quota.

## Verify
- [ ] Record count equals the API's reported total (`@odata.count` with `ConsistencyLevel: eventual`, or the UI).
- [ ] A forced 429 (lower throttle test or mock) waits and resumes without losing pages.

## Checked
Ran against a local Python server on PowerShell 7.6.7 and Windows PowerShell 5.1.26100: the nextLink loop with `AddRange([object[]]...)` (7
records; one-element page), `-FollowRelLink` with and without `-MaximumFollowRelLink` (7 only), the `Link` header on `Invoke-WebRequest`, the
offset/limit loop (7 items), and `Invoke-ApiWithRetry` unchanged against 429 with `Retry-After: 3`, 503 twice then 200, and a 404 (thrown at once) in both
editions. GitHub per_page limits, Graph `$batch` (20 requests), the device resource properties and `ConsistencyLevel: eventual` with `$count` were read on
docs.github.com and Microsoft Learn; the Graph and GitHub URLs in the examples were not called (no token). Graph delta query as a way to get changes without full reads is described on
Microsoft Learn (delta-query-overview); a delta call itself was not made.
