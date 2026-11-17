---
id: computing-software.web-development.gin.gin-custom-http-server
name: gin-custom-http-server
category: computing-software
field: web-development
product: gin
tags: [gin, http-server, readtimeout, writetimeout, maxheaderbytes, listenandserve, handler]
level: practitioner
status: docs-checked
description: "Run Gin through your own http.Server to set ReadTimeout, WriteTimeout and MaxHeaderBytes, since gin.Engine implements http.Handler."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/custom-http-config.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin custom http.Server configuration

Goal: control timeouts and header limits instead of using the basic server started by `router.Run()`.

`gin.Engine` implements `http.Handler`, so the router can be handed straight to Go's `net/http`.

Minimal form:

```go
router := gin.Default()
router.GET("/ping", func(c *gin.Context) {
  c.String(http.StatusOK, "pong")
})
http.ListenAndServe(":8080", router)
```

With custom settings, build an `http.Server` and set `Handler` to the router:

```go
s := &http.Server{
  Addr:           ":8080",
  Handler:        router,
  ReadTimeout:    10 * time.Second,
  WriteTimeout:   10 * time.Second,
  MaxHeaderBytes: 1 << 20,
}
s.ListenAndServe()
```

Test it:

```sh
curl http://localhost:8080/ping
# Output: pong
```

## Notes
- For production you may need to customize timeouts, header limits or TLS settings; all of that lives on the `http.Server` struct.
- You keep all of Gin's routing and middleware while gaining full access to Go's server configuration.
- Related topics in the same docs section: graceful restart or stop, and running multiple services in one process.

## When to use which
`router.Run()` starts a basic HTTP server. `http.ListenAndServe(":8080", router)` is the smallest step away from it and works because the engine is an `http.Handler`. Reach for a full `&http.Server{...}` as soon as you need `ReadTimeout`, `WriteTimeout`, `MaxHeaderBytes` or TLS settings. For graceful stop and running multiple services see the related pages in the same docs section.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Custom HTTP configuration and Server Configuration (http.Server fields, Handler: router, ListenAndServe).
Removed or corrected: unconfirmed advice about reusing the struct for graceful shutdown.

Method: documentation only; no commands were run.
