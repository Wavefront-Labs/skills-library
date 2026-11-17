---
id: computing-software.software-engineering.go.servemux-pattern-routing-and-middleware
name: servemux-pattern-routing-and-middleware
category: computing-software
field: software-engineering
product: go
tags: [go, go-stdlib, net-http, servemux, go-middleware, routing, path-values, go-http-middleware]
level: practitioner
status: verified
description: "Route with Go 1.22+ http.ServeMux method and wildcard patterns, PathValue, precedence rules, and compose standard-library middleware without a framework."
sources:
  - https://pkg.go.dev/net/http#ServeMux
  - https://go.dev/blog/routing-enhancements
  - https://go.dev/doc/go1.22#enhanced_routing_patterns
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ServeMux pattern routing and middleware

**Goal:** a REST API on the standard library alone: method-aware routes, path parameters and a middleware chain.

## 1. Patterns (Go 1.22+)
```go
mux := http.NewServeMux()
mux.HandleFunc("GET /orders", listOrders)
mux.HandleFunc("POST /orders", createOrder)
mux.HandleFunc("GET /orders/{id}", getOrder)
mux.HandleFunc("DELETE /orders/{id}", deleteOrder)
mux.HandleFunc("GET /files/{path...}", serveFile)     // remainder wildcard
mux.HandleFunc("GET /{$}", home)                       // exactly "/", not a catch-all
mux.Handle("GET /static/", http.StripPrefix("/static/", http.FileServerFS(staticFS)))

func getOrder(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    ...
}
```
- `GET` patterns also match `HEAD`.
- Wrong method on a known path returns **405** with an `Allow` header automatically.
- A pattern ending in `/` matches the whole subtree; `{$}` anchors.
- Host-specific patterns: `"api.example.com/v1/..."`.

## 2. Precedence
The **most specific** pattern wins regardless of registration order: `/orders/{id}` vs `/orders/new` both register fine, `/orders/new` wins for that path. Two patterns that overlap with neither more specific (e.g. `/{a}/x` and `/x/{b}`) **panic at registration**, surfacing conflicts at startup.

## 3. Middleware: plain functions
```go
type Middleware func(http.Handler) http.Handler

func Chain(h http.Handler, mws ...Middleware) http.Handler {
    for i := len(mws) - 1; i >= 0; i-- { h = mws[i](h) }
    return h
}

func Logging(log *slog.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            sw := &statusWriter{ResponseWriter: w, status: 200}
            next.ServeHTTP(sw, r)
            log.Info("http", "method", r.Method, "path", r.URL.Path, "status", sw.status, "dur", time.Since(start))
        })
    }
}
type statusWriter struct { http.ResponseWriter; status int }
func (s *statusWriter) WriteHeader(c int) { s.status = c; s.ResponseWriter.WriteHeader(c) }
func (s *statusWriter) Unwrap() http.ResponseWriter { return s.ResponseWriter }   // keeps Flusher etc. reachable via ResponseController

handler := Chain(mux, Recover(log), RequestID, Logging(log), Auth(verifier))
```
Route-specific middleware: wrap individual handlers, or mount a sub-mux: `mux.Handle("/admin/", Chain(adminMux, RequireAdmin))`.

## 4. Context values
Pass request-scoped data (user, request ID) through `r.WithContext(context.WithValue(ctx, userKey{}, u))` with an unexported key type and a typed accessor function.

## Gotchas
- `r.Pattern` (1.23) gives the matched pattern, useful for metrics labels (do not label by raw path: cardinality explosion).
- Path matching is on the unescaped path segment by segment; `%2F` in a wildcard stays inside that segment.
- `GODEBUG=httpmuxgo121=1` restores old behaviour (method and wildcard patterns then stop matching: the test routes all returned 404); check for it when upgrading old services.
- Frameworks (chi, echo) still add conveniences (route groups, regex constraints); chi is a thin compatible layer if you need groups.

## Verify
- Table tests with `httptest.NewRecorder()` cover each route, a 405 for a wrong method with the `Allow` header, and the middleware order (recover outermost catches panics in auth).

## Checked
2026-10-21 on Go 1.27.3 (Windows) with `httptest`: `GET /orders/{id}` and `GET /orders/new` coexisted and `/orders/new` won; HEAD matched a GET pattern; PUT on a known path gave 405 with `Allow: DELETE, GET, HEAD`; `{path...}` captured `a/b/c`; `GET /{$}` matched only `/`; `/orders/a%2Fb` bound `id` to `a/b`; `GET /{a}/x` plus `GET /x/{b}` panicked at registration with 'neither is more specific'; `Chain` ran middlewares outermost first; `r.Pattern` was visible to a logging middleware after routing; `http.NewResponseController(w).Flush()` worked through the `Unwrap` on `statusWriter`; with `GODEBUG=httpmuxgo121=1` the same method patterns returned 404 (old matching). `Request.Pattern` is listed in https://go.dev/doc/go1.23. A follow-up test ran `GET /static/` with `StripPrefix` + `http.FileServerFS` over an `fstest.MapFS` (200 with the file body) and showed a `Recover` middleware outermost turning a panic in an inner `Auth` middleware into a 500; Recover and Auth bodies in that test were written for the check, the skill only names them.
