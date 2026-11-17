---
id: computing-software.software-engineering.go.httptest-servers-and-recorders
name: httptest-servers-and-recorders
category: computing-software
field: software-engineering
product: go
tags: [go, go-testing, go-httptest, httptest, http-testing]
level: practitioner
status: docs-checked
description: "Test Go HTTP handlers and clients with httptest.NewRecorder and httptest.NewServer, including TLS servers and request construction."
sources:
  - https://pkg.go.dev/net/http/httptest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# net/http/httptest servers and recorders

**Goal:** exercise handlers and clients without opening real ports or the internet.

**Handler unit test:** no network, fastest.

```go
req := httptest.NewRequest(http.MethodPost, "/orders", strings.NewReader(`{"sku":"a"}`))
req.Header.Set("Content-Type", "application/json")
rec := httptest.NewRecorder()
newMux().ServeHTTP(rec, req)
res := rec.Result()
if res.StatusCode != http.StatusCreated { t.Fatalf("got %d: %s", res.StatusCode, rec.Body) }
```

**Client test:** stand up a fake upstream.

```go
srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusTooManyRequests)
}))
t.Cleanup(srv.Close)
c := NewClient(srv.URL)           // inject base URL
```

`httptest.NewTLSServer` starts a TLS server; `srv.Client()` returns an `http.Client` configured to trust the server's TLS test certificate.
`NewRequest` panics on error (acceptable in tests); `NewRequestWithContext` was added in Go 1.23.

## Gotchas
- `ResponseRecorder.Code` can be 0 if the handler never calls `WriteHeader` or `Write`; use `Result()` to get the implicit 200.
- Use `rec.Flushed` to test whether the handler called `Flush`.
- Servers created with `NewServer` or `NewTLSServer` must be shut down with `Close`, which blocks until outstanding requests complete.

## Checked
2026-11-09. Confirmed on pkg.go.dev/net/http/httptest: `NewRequest` (panics on error), `NewRequestWithContext` (added go1.23.0), `NewRecorder`,
`ResponseRecorder` fields `Code`, `Body`, `Flushed`, `NewServer`, `NewTLSServer`, `Server.Client` (trusts the TLS test certificate) and `Server.Close`.
Removed claims not on the page: recorder lacks timeouts and Content-Length, `r.PathValue`/`SetPathValue` behaviour, goroutine-leak wording, "self-signed", and the `-race` advice.
Method: documentation only; no commands were run.

## Verify
Assert both status code and body, and a negative case (malformed JSON returns 400).
