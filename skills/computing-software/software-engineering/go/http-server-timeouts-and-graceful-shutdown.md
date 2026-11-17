---
id: computing-software.software-engineering.go.http-server-timeouts-and-graceful-shutdown
name: http-server-timeouts-and-graceful-shutdown
category: computing-software
field: software-engineering
product: go
tags: [go, go-stdlib, net-http, http-server-timeouts, go-graceful-shutdown, slowloris, signal-notifycontext, go-http-server, go-signal-shutdown]
level: practitioner
status: verified
description: "Configure Go http.Server timeouts against slow clients, per-handler deadlines, and graceful Shutdown on SIGTERM that drains in-flight requests."
sources:
  - https://pkg.go.dev/net/http#Server
  - https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
  - https://pkg.go.dev/os/signal#NotifyContext
  - https://pkg.go.dev/net/http#Server.Shutdown
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# http.Server timeouts and graceful Shutdown

**Goal:** a Go HTTP server that slow or malicious clients cannot exhaust, and that drains cleanly on deploy.

## 1. Never use the zero-timeout defaults in production
`http.ListenAndServe(addr, h)` has **no timeouts**: a client sending headers one byte per minute holds a goroutine and FD forever (Slowloris).
```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,    // the most important one
    ReadTimeout:       30 * time.Second,   // whole request incl. body
    WriteTimeout:      30 * time.Second,   // from end of header read to end of response write
    IdleTimeout:       120 * time.Second,  // keep-alive connections
    MaxHeaderBytes:    1 << 20,
}
```
- `WriteTimeout` kills streaming/SSE/long downloads (checked: a 6-chunk stream over 1.2 s with `WriteTimeout` 700 ms was cut after 4 chunks and the client got `unexpected EOF`; a slow handler's response is dropped and the client sees `EOF`, not a 5xx); for those set it to 0 or extend it per response with `rc.SetWriteDeadline` (checked: the same stream then completed).
- Behind a load balancer, keep `IdleTimeout` above the LB's idle timeout to avoid races that cause 502s.

## 2. Per-handler deadlines
```go
mux.Handle("POST /reports", http.TimeoutHandler(reportHandler, 10*time.Second, "timeout"))
// or fine-grained, Go 1.20+
rc := http.NewResponseController(w)
rc.SetWriteDeadline(time.Now().Add(5 * time.Minute))   // extend for one streaming response
```
Inside handlers, use `r.Context()` for downstream calls so client disconnects and server shutdown cancel the work. Limit bodies: `r.Body = http.MaxBytesReader(w, r.Body, 1<<20)`.

## 3. Graceful shutdown
```go
func main() {
    ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
    defer stop()

    go func() {
        if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
            log.Fatalf("listen: %v", err)
        }
    }()

    <-ctx.Done()
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
    defer cancel()
    if err := srv.Shutdown(shutdownCtx); err != nil {    // stops listeners, waits for active requests
        log.Printf("forced shutdown: %v", err)
        srv.Close()
    }
    // then close DB pools, flush telemetry
}
```
- `Shutdown` polls for idle connections with a backoff of up to 500 ms, so it can return a few hundred ms after the last request ends (1.5 s request: returned at 1.6 s).
- `ListenAndServe` returns `ErrServerClosed` immediately when `Shutdown` starts; the main goroutine must wait for `Shutdown` to return, not exit early.
- `Shutdown` does not wait for hijacked connections (WebSockets); track and close them via `RegisterOnShutdown`.
- Use `BaseContext` to give handlers a context cancelled at shutdown start if long requests should abort.

## 4. Kubernetes
Shutdown timeout < `terminationGracePeriodSeconds`. Fail readiness (or `preStop` sleep 5-10 s) before shutting down so endpoints are removed first.

## Gotchas
- `log.Fatal` in the serve goroutine skips deferred cleanup; signal the main goroutine instead in complex programs.
- `TimeoutHandler` buffers the response and does not support `Flusher`/hijacking (checked: the wrapped writer is not an `http.Flusher`; it returns 503 with the given body at the deadline).
- Shutdown with HTTP/2: connections get GOAWAY; clients must retry idempotent requests.

## Verify
- `slowhttptest` or a raw socket sending headers slowly is disconnected after `ReadHeaderTimeout`; sending SIGTERM during a 10 s request lets it finish with 200 and the process exits 0.
## Checked
Run on Windows with Go 1.25.1 (real servers on loopback): a raw socket sending an incomplete header was closed after `ReadHeaderTimeout` (300 ms) with no response; `WriteTimeout` cut a stream and a slow response; `ResponseController.SetWriteDeadline` extended it; `TimeoutHandler` 503 and no Flusher; `MaxBytesReader` returns `*http.MaxBytesError`; `Shutdown` let a 1.5 s in-flight request finish with 200, `Serve` returned `ErrServerClosed`, and new connections were refused afterwards. Not run: SIGTERM delivery (the Windows build has no SIGTERM from the OS; `os.Interrupt` only via Ctrl-C/Ctrl-Break), hijacked connections, HTTP/2 GOAWAY, `IdleTimeout` behind a load balancer, Kubernetes advice, `slowhttptest`. On Linux, `kill -TERM` works as written.
Linux pass (Go 1.25.1 static binary in a WSL2 busybox distro): all timeout, `TimeoutHandler`, `MaxBytesReader` and `Shutdown` results matched Windows; additionally `kill -TERM` during a 2 s request let it finish with 200 and the process exited 0 after `Shutdown` returned.
