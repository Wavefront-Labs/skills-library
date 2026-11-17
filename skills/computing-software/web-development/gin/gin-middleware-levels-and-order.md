---
id: computing-software.web-development.gin.gin-middleware-levels-and-order
name: gin-middleware-levels-and-order
category: computing-software
field: web-development
product: gin
tags: [gin, middleware, router-use, group-use, per-route-middleware, c-next, c-abort, gin-new, gin-default]
level: intro
status: docs-checked
description: "Attach Gin middleware globally, per group or per route, understand c.Next ordering, and choose between gin.Default and gin.New."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/using-middleware.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/without-middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin middleware levels, ordering, and Default vs New

Goal: attach middleware at the right scope and know what a router starts with.

## Router choice
- `gin.Default()` returns a router with Logger (method, path, status, latency to stdout) and Recovery (recovers panics, returns a 500) already attached.
- `gin.New()` returns a blank router with no middleware. Use it for a structured logger (slog, zerolog), custom panic recovery, or a minimal microservice stack.

## Three attachment levels
- Global: `router.Use(...)`
- Group: `group.Use(...)` or pass middleware to `router.Group("/path", mw)`
- Per route: extra arguments before the handler, e.g. `router.GET("/benchmark", MyBenchLogger(), benchEndpoint)`

```go
router := gin.New()
router.Use(gin.Logger())
router.Use(gin.Recovery())
router.GET("/benchmark", MyBenchLogger(), benchEndpoint)

authorized := router.Group("/")
authorized.Use(AuthRequired())
{
  authorized.POST("/login", loginEndpoint)
  testing := authorized.Group("testing")
  testing.GET("/analytics", analyticsEndpoint)
}
router.Run(":8080")
```

## Execution order
Middleware runs in registration order. A middleware that calls `c.Next()` hands control onward and resumes after it returns, so the first registered starts first and finishes last. If it does not call `c.Next()`, later middleware and the handler are skipped (short-circuit with `c.Abort()`).

## Gotcha
`gin.Logger()` writes to `gin.DefaultWriter` (stdout by default) even when `GIN_MODE=release` is set.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Using middleware and Without middleware by default (three levels, order, Default vs New, Logger note).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
