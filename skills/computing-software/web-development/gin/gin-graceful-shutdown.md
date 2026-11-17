---
id: computing-software.web-development.gin.gin-graceful-shutdown
name: gin-graceful-shutdown
category: computing-software
field: web-development
product: gin
tags: [gin, graceful-shutdown, shutdown, errserverclosed, signal-notify, endless, http-server]
level: practitioner
status: docs-checked
description: "Shut a Gin server down gracefully with http.Server.Shutdown, a SIGINT/SIGTERM channel and a 5 second timeout context, or fvbock/endless as an alternative."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/graceful-restart-or-stop.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin graceful restart or stop

Goal: on a termination signal, let in-flight requests finish, stop accepting new connections and clean up before exit.

The page lists the benefits: complete in-flight requests, drain connections, release resources (database connections, file handles, background workers) and enable zero-downtime deployments behind a load balancer.

## Go 1.8+ approach: http.Server.Shutdown
```go
router := gin.Default()
router.GET("/", func(c *gin.Context) {
  time.Sleep(5 * time.Second)
  c.String(http.StatusOK, "Welcome Gin Server")
})

srv := &http.Server{
  Addr:    ":8080",
  Handler: router.Handler(),
}

go func() {
  if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
    log.Fatalf("listen: %s\n", err)
  }
}()

quit := make(chan os.Signal, 1)
// kill (no params) sends syscall.SIGTERM; kill -2 is SIGINT;
// kill -9 is SIGKILL and cannot be caught
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit
log.Println("Shutdown Server ...")

ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
if err := srv.Shutdown(ctx); err != nil {
  log.Println("Server Shutdown:", err)
}
log.Println("Server exiting")
```

## Library alternative
fvbock/endless replaces the default `ListenAndServe`:

```go
router := gin.Default()
router.GET("/", handler)
endless.ListenAndServe(":4242", router)
```

Other libraries named: manners, graceful, grace.

## Gotchas
- With Go 1.8 and later you may not need these libraries; prefer the built-in `Shutdown()`.
- The shutdown wait here is a 5 second context timeout.
- A full example lives in the gin-gonic/examples graceful-shutdown folder.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Graceful restart or stop (Shutdown with signal channel and 5 s context, endless, alternatives, Go 1.8 note).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
