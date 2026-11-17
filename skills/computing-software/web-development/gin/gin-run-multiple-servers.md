---
id: computing-software.web-development.gin.gin-run-multiple-servers
name: gin-run-multiple-servers
category: computing-software
field: web-development
product: gin
tags: [gin, errgroup, multiple-servers, http-server, listenandserve, gin-new, recovery]
level: practitioner
status: docs-checked
description: "Run several Gin routers on different ports in one process with golang.org/x/sync/errgroup and one http.Server per router."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/run-multiple-service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin: run multiple servers in one process

Goal: expose separate APIs (for example public on 8080 and admin on 8081) from one binary.

Use `errgroup.Group` from `golang.org/x/sync/errgroup`. Each server gets its own router, middleware stack and `http.Server` configuration.

```go
var g errgroup.Group

func router01() http.Handler {
  e := gin.New()
  e.Use(gin.Recovery())
  e.GET("/", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
      "code":    http.StatusOK,
      "message": "Welcome server 01",
    })
  })
  return e
}
// router02 is identical with "Welcome server 02"

func main() {
  server01 := &http.Server{
    Addr:         ":8080",
    Handler:      router01(),
    ReadTimeout:  5 * time.Second,
    WriteTimeout: 10 * time.Second,
  }
  server02 := &http.Server{
    Addr:         ":8081",
    Handler:      router02(),
    ReadTimeout:  5 * time.Second,
    WriteTimeout: 10 * time.Second,
  }

  g.Go(func() error { return server01.ListenAndServe() })
  g.Go(func() error { return server02.ListenAndServe() })

  if err := g.Wait(); err != nil {
    log.Fatal(err)
  }
}
```

Test it:

```sh
curl http://localhost:8080/
# Output: {"code":200,"message":"Welcome server 01"}
curl http://localhost:8081/
# Output: {"code":200,"message":"Welcome server 02"}
```

## Gotcha
If either server fails to start (for example a port already in use), `g.Wait()` returns the first error. Both servers must start successfully for the process to keep running.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: server-config/run-multiple-service.md. Confirmed: errgroup usage, one router and http.Server per port (8080 and 8081), the 5 s and 10 s timeouts, the curl outputs, and g.Wait() returning the first error. Trimmed nothing.

Method: documentation only; no commands were run.
