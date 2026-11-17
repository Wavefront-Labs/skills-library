---
id: computing-software.software-engineering.go.http-server-request-limits-and-body-size
name: http-server-request-limits-and-body-size
category: computing-software
field: software-engineering
product: go
tags: [go, go-http-server, go-http-limits, max-bytes-reader, request-limits, slowloris]
level: practitioner
status: docs-checked
description: "Bound what clients can make a Go HTTP server do: MaxBytesReader, header limits and read timeouts."
sources:
  - https://pkg.go.dev/net/http#MaxBytesReader
  - https://pkg.go.dev/net/http#Server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP server request limits and body size

**Goal:** a single slow or huge request cannot exhaust memory, sockets or CPU.

```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           h,
    ReadHeaderTimeout: 5 * time.Second,   // time allowed to read request headers
    ReadTimeout:       30 * time.Second,  // whole request including body
    WriteTimeout:      60 * time.Second,  // response writes
    IdleTimeout:       120 * time.Second, // next request on a keep-alive connection
    MaxHeaderBytes:    16 << 10,          // 0 means DefaultMaxHeaderBytes (1 MB)
}

func limited(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        r.Body = http.MaxBytesReader(w, r.Body, 1<<20) // 1 MiB
        next.ServeHTTP(w, r)
    })
}
// decoding: a too-large body yields *http.MaxBytesError
var mbe *http.MaxBytesError
if errors.As(err, &mbe) { http.Error(w, "too large", http.StatusRequestEntityTooLarge) }
```

`MaxBytesReader` is like `io.LimitReader` for incoming request bodies: its result is a `ReadCloser`, it returns a `*MaxBytesError` for a read beyond the limit, and if possible it tells the `ResponseWriter` to close the connection after the limit is reached. `MaxHeaderBytes` limits the request line and header keys and values, not the body. A `ResponseController` (Go 1.20) can set per-request deadlines such as `SetReadDeadline` from inside a handler.

## Gotchas
- `ReadTimeout` covers the entire request including the body and does not let handlers decide per request; the `Server` docs say most users prefer `ReadHeaderTimeout` (the read deadline is reset after the headers, so the handler decides what is too slow for the body). It is valid to use both.
- `WriteTimeout` is reset whenever a new request's header is read and, like `ReadTimeout`, is not per request.
- If `ReadHeaderTimeout` or `IdleTimeout` is zero, `ReadTimeout` is used.

## Verify
Send a body larger than the limit and expect your handler to see `*http.MaxBytesError` and answer 413; stall a client after the headers and expect the connection to be dropped when the header timeout passes.

## Checked
2026-11-03. Confirmed on pkg.go.dev/net/http: `MaxBytesReader` and `MaxBytesError` (go1.19), `Server` field comments for ReadTimeout, ReadHeaderTimeout, WriteTimeout, IdleTimeout, MaxHeaderBytes, `DefaultMaxHeaderBytes` (1 MB), `NewResponseController` and `SetReadDeadline` (go1.20). Removed: slowloris label, `netutil.LimitListener` and semaphore advice, `ParseMultipartForm`, reverse-proxy note, `curl`/`nc` steps.
Method: documentation only; no commands were run.
