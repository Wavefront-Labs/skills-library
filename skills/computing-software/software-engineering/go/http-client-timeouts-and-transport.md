---
id: computing-software.software-engineering.go.http-client-timeouts-and-transport
name: http-client-timeouts-and-transport
category: computing-software
field: software-engineering
product: go
tags: [go, go-stdlib, net-http, http-client, go-http-client, timeouts, connection-reuse, retries, go-net-dialer]
level: practitioner
status: verified
description: "Use Go's http.Client safely: timeouts at every layer, Transport pool tuning, closing and draining bodies for connection reuse, context cancellation and retries."
sources:
  - https://pkg.go.dev/net/http#Client
  - https://pkg.go.dev/net/http#Transport
  - https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# http.Client timeouts and Transport tuning

**Goal:** outbound HTTP calls that never hang, reuse connections, and fail fast under downstream trouble.

## 1. Never use http.DefaultClient in services
It has **no timeout**: a stalled server blocks the goroutine forever.
```go
var transport = &http.Transport{
    Proxy:                 http.ProxyFromEnvironment,
    DialContext:           (&net.Dialer{Timeout: 5 * time.Second, KeepAlive: 30 * time.Second}).DialContext,
    TLSHandshakeTimeout:   5 * time.Second,
    ResponseHeaderTimeout: 10 * time.Second,
    ExpectContinueTimeout: 1 * time.Second,
    MaxIdleConns:          100,
    MaxIdleConnsPerHost:   20,          // default 2: causes connection churn under load to one host
    MaxConnsPerHost:       50,          // cap concurrency to protect the downstream
    IdleConnTimeout:       90 * time.Second,
    ForceAttemptHTTP2:     true,
}
var client = &http.Client{Transport: transport, Timeout: 15 * time.Second}   // whole exchange incl. body read
```
Create clients once and share them; they are safe for concurrent use. Per-request clients defeat pooling and leak connections.

## 2. Per-request deadlines with context
```go
ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
defer cancel()
req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
resp, err := client.Do(req)
if err != nil { return fmt.Errorf("get %s: %w", url, err) }
defer resp.Body.Close()
```
Propagating the incoming request's context cancels outbound calls when the client disconnects.

## 3. Bodies: close and drain
```go
defer resp.Body.Close()
if resp.StatusCode != http.StatusOK {
    io.Copy(io.Discard, io.LimitReader(resp.Body, 64<<10))   // drain so the connection can be reused
    return fmt.Errorf("unexpected status %d", resp.StatusCode)
}
var out Payload
if err := json.NewDecoder(io.LimitReader(resp.Body, 10<<20)).Decode(&out); err != nil { ... }
```
- Not closing the body leaks the connection and goroutines; `bodyclose` linter catches it.
- A non-2xx status is **not** an error from `Do`; check `StatusCode`.
- Limit response size from untrusted servers.

## 4. Retries
Retry only idempotent requests (GET, PUT, DELETE, or POST with an idempotency key), on connection errors, 429 and 502/503/504, with exponential backoff and jitter, honouring `Retry-After`, and within the overall context deadline. Request bodies must be rewindable (`req.GetBody`, set automatically for `bytes.Reader`/`strings.Reader`). `hashicorp/go-retryablehttp` implements this.

## 5. Observability
`otelhttp.NewTransport(transport)` adds tracing/metrics; `httptrace.ClientTrace` exposes DNS, connect, TLS and first-byte timings for debugging latency.

## Gotchas
- `Client.Timeout` includes reading the body: streaming downloads need context deadlines instead.
- Redirects: the client follows up to 10 and drops `Authorization`, `WWW-Authenticate` and `Cookie` headers when redirected to a different domain (not the same host or a subdomain; ports do not count); customise `CheckRedirect` if needed.
- TLS `InsecureSkipVerify: true` must never ship; load custom CAs into `tls.Config.RootCAs`.
- DNS changes: long-lived idle connections keep hitting old IPs; `IdleConnTimeout` bounds it.

## Verify
- An `httptest.Server` that sleeps longer than the timeouts makes calls fail within the deadline; under load `netstat` shows a stable number of connections (reuse), not thousands of TIME_WAITs.

## Checked
2026-10-21 on Go 1.27.3 (Windows) against `httptest` servers: the Transport literal compiled; `http.DefaultClient.Timeout` is 0 and `DefaultMaxIdleConnsPerHost` is 2; a 500 ms `Client.Timeout` aborted a slow handler at about 500 ms and also aborted a body read after headers had arrived (`context deadline exceeded (Client.Timeout or context cancellation while reading body)`); a context deadline and `ResponseHeaderTimeout` (`timeout awaiting response headers`) failed as expected; a 404 gave `err == nil`; a redirect loop stopped with `stopped after 10 redirects`; `Authorization` was forwarded to a redirect on the same host but dropped when redirected from 127.0.0.1 to localhost (two ports on one host name still forward it); `req.GetBody` was set for `bytes.Reader` and `strings.Reader` but not for `io.NopCloser(...)`; `httptrace.ClientTrace` hooks fired. Redirect header rule from https://pkg.go.dev/net/http. Also ran: hashicorp/go-retryablehttp retried two 503 responses and then succeeded (3 attempts); `otelhttp.NewTransport(http.DefaultTransport)` wrapped a working client. The netstat/TIME_WAIT check in Verify is a manual load test and was not run.
