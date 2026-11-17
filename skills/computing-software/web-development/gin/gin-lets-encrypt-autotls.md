---
id: computing-software.web-development.gin.gin-lets-encrypt-autotls
name: gin-lets-encrypt-autotls
category: computing-software
field: web-development
product: gin
tags: [gin, autotls, lets-encrypt, autocert, runwithmanager, hostwhitelist, dircache, https]
level: practitioner
status: docs-checked
description: "Serve Gin over automatic HTTPS with gin-gonic/autotls: autotls.Run for domains, or RunWithManager with an autocert.Manager, HostWhitelist and DirCache."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/support-lets-encrypt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin automatic HTTPS with Let's Encrypt

Goal: serve HTTPS with automatic certificate issuance and renewal using the `github.com/gin-gonic/autotls` package.

## Quick start
```go
import (
  "log"

  "github.com/gin-gonic/autotls"
  "github.com/gin-gonic/gin"
)

func main() {
  router := gin.Default()
  router.GET("/ping", func(c *gin.Context) {
    c.String(200, "pong")
  })
  log.Fatal(autotls.Run(router, "example1.com", "example2.com"))
}
```

## Custom autocert manager
Use `autotls.RunWithManager` when you need a certificate cache directory or restricted hostnames:

```go
import "golang.org/x/crypto/acme/autocert"

m := autocert.Manager{
  Prompt:     autocert.AcceptTOS,
  HostPolicy: autocert.HostWhitelist("example1.com", "example2.com"),
  Cache:      autocert.DirCache("/var/www/.cache"),
}

log.Fatal(autotls.RunWithManager(router, &m))
```

## Gotcha
Let's Encrypt requires the server to be reachable on ports 80 and 443 from the public internet. It will not work on localhost or behind a firewall that blocks inbound connections.

## How to choose
- `autotls.Run(router, domains...)` is the simplest path: pass your router and one or more domain names, and certificate issuance and renewal are handled for you.
- `autotls.RunWithManager(router, &m)` takes an `autocert.Manager` (from `golang.org/x/crypto/acme/autocert`) when you need control: `Prompt: autocert.AcceptTOS` accepts the terms of service, `HostPolicy: autocert.HostWhitelist(...)` restricts which hostnames are served, and `Cache: autocert.DirCache(dir)` sets the certificate cache directory.
- Both calls return an error, so wrap them in `log.Fatal(...)` as in the examples.
- Related: if you only need custom timeouts on a plain HTTP server, see the custom http.Server configuration instead.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Support Let's Encrypt (autotls.Run, RunWithManager, autocert.Manager fields, ports 80 and 443 note).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
