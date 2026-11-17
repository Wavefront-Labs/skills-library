---
id: computing-software.web-development.gin.gin-custom-recovery
name: gin-custom-recovery
category: computing-software
field: web-development
product: gin
tags: [gin, middleware, custom-recovery, gin-customrecovery, panic, abortwithstatus, gin-recovery]
level: practitioner
status: docs-checked
description: "Control what Gin does after a panic with gin.CustomRecovery(func(c *gin.Context, recovered any)) instead of the built-in gin.Recovery() 500 response."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/custom-recovery.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom recovery behaviour

Goal: handle panics your own way (tell the user, save to a database, send to an error tracker).

The built-in `gin.Recovery()` catches any panic while handling a request, writes a 500 and keeps the server running. Use `gin.CustomRecovery()` when you need control. Its handler has the signature `func(c *gin.Context, recovered any)`; `recovered` is whatever was passed to `panic()`. Respond, then call `c.AbortWithStatus()` (or another abort method) so remaining handlers are skipped.

```go
r := gin.New()

r.Use(gin.Logger())

r.Use(gin.CustomRecovery(func(c *gin.Context, recovered any) {
  if err, ok := recovered.(string); ok {
    c.String(http.StatusInternalServerError, fmt.Sprintf("error: %s", err))
  }
  c.AbortWithStatus(http.StatusInternalServerError)
}))

r.GET("/panic", func(c *gin.Context) {
  panic("foo")
})

r.GET("/", func(c *gin.Context) {
  c.String(http.StatusOK, "ohai")
})

r.Run(":8080")
```

## Try it
```bash
curl http://localhost:8080/panic
# => error: foo

curl http://localhost:8080/
# => ohai
```

## Gotchas
- Use `gin.New()` (no default middleware) so `gin.Recovery()` is not also attached.
- The docs' example only writes a message when the recovered value is a string; you decide how to handle other types.
- A comment in the example notes that the logger writes to `gin.DefaultWriter` even with `GIN_MODE=release`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Custom Recovery behavior (CustomRecovery signature, AbortWithStatus, curl outputs, Logger note).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
