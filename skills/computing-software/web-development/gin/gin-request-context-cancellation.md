---
id: computing-software.web-development.gin.gin-request-context-cancellation
name: gin-request-context-cancellation
category: computing-software
field: web-development
product: gin
tags: [gin, context, request-context, timeout, cancellation, copy, withcontext]
level: advanced
status: docs-checked
description: "Propagate c.Request.Context() in Gin for timeouts, DB and outbound calls, client disconnects, and use c.Copy() before goroutines; avoid writing after cancellation."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin context and cancellation

Goal: use the request's `context.Context` correctly so timeouts and client disconnects stop work.

The standard context is `c.Request.Context()`. Pass it to every downstream call (database, HTTP clients, gRPC, other I/O).

Timeout middleware that replaces the request with one carrying a deadline:

```go
func TimeoutMiddleware(timeout time.Duration) gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(c.Request.Context(), timeout)
		defer cancel()
		c.Request = c.Request.WithContext(ctx)
		c.Next()
	}
}
// r.Use(TimeoutMiddleware(5 * time.Second))
```

Context-aware calls:

```go
db.QueryRowContext(ctx, "SELECT name FROM users WHERE id = $1", id).Scan(&name)
req, err := http.NewRequestWithContext(ctx, http.MethodGet, "https://httpbin.org/delay/3", nil)
```

Long-running handlers can detect disconnects with `select` on `ctx.Done()` (the page's SSE example calls `c.SSEvent("message", gin.H{"count": i})` then `c.Writer.Flush()` each second).

## Goroutines
`gin.Context` is reused across requests. Inside a goroutine you must use a copy:

```go
cCopy := c.Copy()
go func() {
	time.Sleep(2 * time.Second)
	log.Printf("async work done for %s\n", cCopy.Request.URL.Path)
}()
```

## Gotchas
- Do not store `*gin.Context` in structs or pass it across goroutine boundaries; it is not safe for concurrent use.
- Handlers that ignore `ctx.Done()` keep running after the client disconnects.
- After cancellation avoid writing to `c.Writer`: the connection may already be closed. The page's example checks `ctx.Err()` when long-running work returns an error and, if it is non-nil, returns without writing.
- Prefer `c.Set()`/`c.Get()` over `context.WithValue` inside handlers.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: server-config/context.md. Confirmed: c.Request.Context(), the timeout middleware, QueryRowContext and NewRequestWithContext examples, the SSE disconnect example, c.Copy() in goroutines and the best-practice bullets. Reworded one gotcha: the page does not tell you to always check ctx.Err() first, it checks ctx.Err() when long-running work returns an error and then skips the write.

Method: documentation only; no commands were run.
