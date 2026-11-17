---
id: computing-software.web-development.gin.gin-middleware-flow-and-custom
name: gin-middleware-flow-and-custom
category: computing-software
field: web-development
product: gin
tags: [gin, middleware, c-next, c-abort, abortwithstatusjson, c-set, c-mustget, group]
level: practitioner
status: docs-checked
description: "Write Gin middleware with before/after c.Next() phases, abort with c.AbortWithStatusJSON, and attach it globally, per group or per route."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/index.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/custom-middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin middleware: execution flow and custom middleware

Goal: write a middleware and know when it runs.

A middleware is a function returning `gin.HandlerFunc` (same signature as a route handler). Gin uses an onion model: code before `c.Next()` runs before the route handler, code after it runs after the handler returns. The first middleware attached is the outermost layer.

```go
func Logger() gin.HandlerFunc {
  return func(c *gin.Context) {
    t := time.Now()

    // Set example variable
    c.Set("example", "12345")

    // before request
    c.Next()

    // after request
    latency := time.Since(t)
    log.Print(latency)

    // access the status we are sending
    status := c.Writer.Status()
    log.Println(status)
  }
}

r := gin.New()
r.Use(Logger())
r.GET("/test", func(c *gin.Context) {
  example := c.MustGet("example").(string) // "12345"
  log.Println(example)
})
```

## Stop the chain
Call `c.Abort()` instead of `c.Next()` to prevent remaining handlers from running, e.g. when authentication fails. Combine with a response: `c.AbortWithStatusJSON(401, gin.H{"error": "unauthorized"})`.

## Attaching middleware
```go
// 1. Global
router := gin.New()
router.Use(Logger(), Recovery())

// 2. Group
v1 := router.Group("/v1")
v1.Use(AuthRequired())
{
  v1.GET("/users", listUsers)
}

// 3. Per-route
router.GET("/benchmark", BenchmarkMiddleware(), benchHandler)
```

Broader scope runs first: for `GET /v1/users` the order is Logger, Recovery, AuthRequired, listUsers.

## Gotcha
Execution pauses at `c.Next()` until all downstream handlers have completed, so post-handler code sees the final `c.Writer.Status()`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Middleware index and Custom Middleware (onion model, c.Next phases, c.Abort, AbortWithStatusJSON, three attachment levels and order).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
