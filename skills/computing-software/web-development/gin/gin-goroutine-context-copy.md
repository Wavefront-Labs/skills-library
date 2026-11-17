---
id: computing-software.web-development.gin.gin-goroutine-context-copy
name: gin-goroutine-context-copy
category: computing-software
field: web-development
product: gin
tags: [gin, middleware, goroutine, c-copy, sync-pool, race-condition, gin-context]
level: practitioner
status: docs-checked
description: "Use c.Copy() to give a goroutine a read-only copy of gin.Context, because the original context is pooled and reused by later requests."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/goroutines-inside-a-middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Goroutines inside a handler or middleware

Goal: run background work safely from a Gin handler.

Rule: when starting a goroutine inside a middleware or handler, do NOT use the original `*gin.Context` in it; use a read-only copy from `c.Copy()`.

## Why
Gin uses a `sync.Pool` to reuse `gin.Context` objects across requests. After the handler returns, the context goes back to the pool and may be assigned to a different request. A goroutine still holding the original would read or write fields belonging to another request, causing race conditions, data corruption or panics.

`c.Copy()` makes a snapshot (request, URL, keys and other read-only data) detached from the pool lifecycle, safe to use after the handler returns.

```go
router := gin.Default()

router.GET("/long_async", func(c *gin.Context) {
  // create copy to be used inside the goroutine
  cCp := c.Copy()
  go func() {
    // simulate a long task with time.Sleep(). 5 seconds
    time.Sleep(5 * time.Second)

    // note that you are using the copied context "cCp", IMPORTANT
    log.Println("Done! in path " + cCp.Request.URL.Path)
  }()
})

router.GET("/long_sync", func(c *gin.Context) {
  time.Sleep(5 * time.Second)

  // since we are NOT using a goroutine, we do not have to copy the context
  log.Println("Done! in path " + c.Request.URL.Path)
})

router.Run(":8080")
```

## Gotchas
- Call `c.Copy()` before the `go` statement, in the handler goroutine, and pass only the copy into the new goroutine.
- No copy is needed when the work is synchronous (the `/long_sync` route).

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Goroutines inside a middleware (sync.Pool reuse, c.Copy() snapshot, async and sync examples).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
