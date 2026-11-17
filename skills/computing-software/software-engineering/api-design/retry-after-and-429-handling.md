---
id: computing-software.software-engineering.api-design.retry-after-and-429-handling
name: retry-after-and-429-handling
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, retry-after, http-429, http-503, backoff, jitter, rate-limiting, rfc-9110]
level: practitioner
status: docs-checked
description: "Signal and honour retry timing: send Retry-After with 429 and 503, and write client backoff that respects it, adds jitter and only retries safe requests."
sources: ["https://www.rfc-editor.org/rfc/rfc9110#field.retry-after", "https://www.rfc-editor.org/rfc/rfc6585#section-4", "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry-After and 429 handling

## Server
`Retry-After` (RFC 9110 section 10.2.3) holds either an HTTP-date or `delay-seconds`, a non-negative decimal integer. With 503 it says how long the service is expected to be unavailable to the client; with a 3xx it is the minimum wait before following the redirect. RFC 6585 allows it on 429 Too Many Requests, which means the user sent too many requests in a given time.
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/json

{"title":"Too many requests","status":429,"detail":"Limit reached; retry after 30 seconds."}
```
- A 429 response SHOULD carry details explaining the condition and MAY carry `Retry-After`. RFC 6585 does not say how the server identifies the user or counts requests (per resource, across the server, per credential or cookie are all allowed).
- 429 responses MUST NOT be stored by a cache.
- Keep the value truthful and do not give every client the same second, which causes a thundering herd after it elapses.

## Client
```python
import random, time, email.utils
def delay(resp, attempt):
    ra = resp.headers.get("Retry-After")
    if ra:
        if ra.isdigit(): return int(ra)
        return max(0, email.utils.parsedate_to_datetime(ra).timestamp() - time.time())
    return random.uniform(0, min(60, 0.5 * 2 ** attempt))   # capped exponential backoff with full jitter
```
- Prefer the server's hint over your own backoff; cap total attempts and total time. Capped exponential backoff keeps load even, and a retry limit stops every client retrying at the cap forever.
- Add jitter: if all failed calls back off to the same time they cause contention again when retried. Randomness spreads them.
- Retry automatically only operations that are safe to repeat: read-only calls, idempotent calls, or calls with an explicit idempotency token. Calls with side effects are not safe to retry otherwise, because a timeout does not prove the side effect did not happen.
- Retry transient server-side failures (such as 429 and 503) and connection failures; client errors generally will not succeed on a repeat, though eventual consistency blurs this.

## Gotchas
- Retries multiply load in layered services (three retries at each of five layers is a 243x load on the database); retry at a single point in the stack, and consider limiting retries locally with a token bucket.
- Parse both forms of the header; the HTTP-date form is easy to forget.

Verify: stub a server that returns `429` with `Retry-After: 2` twice then `200`; confirm the client waits at least 2 seconds each time and succeeds on the third request.

## Checked
2026-11-08. Confirmed against RFC 9110 section 10.2.3 (read in full), RFC 6585 section 4 (read in full) and the AWS Builders' Library article on timeouts, retries and backoff with jitter (read in full). Removed: the claim that 503 is for server-wide overload and 429 for per-client limits (503 semantics, RFC 9110 section 15.6.4, not read; 429 text is looser), the problem+json body and the explicit list of retryable statuses (502, 504 not covered by the sources).
Method: documentation only; no commands were run.
