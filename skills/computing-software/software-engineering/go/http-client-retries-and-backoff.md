---
id: computing-software.software-engineering.go.http-client-retries-and-backoff
name: http-client-retries-and-backoff
category: computing-software
field: software-engineering
product: go
tags: [go, go-http-client, go-http-retries, retries, backoff, idempotency]
level: practitioner
status: draft
description: "Add safe retries to Go HTTP clients: idempotent methods, rewindable bodies, jittered exponential backoff, Retry-After and context deadlines."
sources:
  - https://pkg.go.dev/net/http#Request
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# HTTP client retries and backoff

**Goal:** survive transient failures without amplifying outages.

```go
func doWithRetry(ctx context.Context, c *http.Client, mk func() (*http.Request, error)) (*http.Response, error) {
    var lastErr error
    for attempt := 0; attempt < 4; attempt++ {
        req, err := mk()                      // rebuild: bodies are consumed
        if err != nil { return nil, err }
        resp, err := c.Do(req.WithContext(ctx))
        if err == nil && resp.StatusCode < 500 && resp.StatusCode != 429 { return resp, nil }
        if err == nil {
            lastErr = fmt.Errorf("status %d", resp.StatusCode)
            io.Copy(io.Discard, resp.Body); resp.Body.Close()
        } else { lastErr = err }
        d := time.Duration(rand.Int64N(int64(100*time.Millisecond) << attempt)) // full jitter
        select {
        case <-time.After(d):
        case <-ctx.Done(): return nil, ctx.Err()
        }
    }
    return nil, lastErr
}
```

Retry only idempotent requests (GET, PUT, DELETE, or POST with an `Idempotency-Key`). Honour `Retry-After` on 429/503. Use `req.GetBody` (set automatically for `bytes.Reader`, `strings.Reader`) to rewind. Libraries: `hashicorp/go-retryablehttp`, `cenkalti/backoff/v4`.

## Gotchas
- Retrying inside every layer multiplies attempts; retry at one layer and use a retry budget.
- Set a per-attempt timeout and an overall context deadline.
- Never retry on 4xx other than 408/429.

## Verify
Test against an `httptest` server that fails twice then succeeds; assert call count is 3 and that cancelling the context aborts waiting.
