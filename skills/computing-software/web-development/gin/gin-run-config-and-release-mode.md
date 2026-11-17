---
id: computing-software.web-development.gin.gin-run-config-and-release-mode
name: gin-run-config-and-release-mode
category: computing-software
field: web-development
product: gin
tags: [gin, gin-mode, port, release-mode, router-run, settrustedproxies, deployment, environment-variables]
level: practitioner
status: docs-checked
description: "Configure a Gin server for deployment: PORT and GIN_MODE env vars, router.Run bind forms, SetMode release, SetTrustedProxies, and the 405 option."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/deployment/index.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/faq/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin deployment configuration

Goal: set the listen address and run mode for a deployed Gin app.

| Environment variable | Effect |
|---|---|
| `PORT` | TCP port used by `router.Run()` when called with no arguments |
| `GIN_MODE` | `debug`, `release` or `test`; controls things like when debug output is emitted |

```sh
export GIN_MODE=release
# or
GIN_MODE=release ./your-app
```

In code:

```go
gin.SetMode(gin.ReleaseMode)   // or gin.TestMode

router := gin.Default()
router.Run()                      // all interfaces, port 8080 (or PORT)
router.Run("192.168.1.100:8080")  // explicit address and port
router.Run(":8080")               // port only, all interfaces
router.SetTrustedProxies([]string{"192.168.1.2"})
```

`SetTrustedProxies` sets which IPs or CIDRs are trusted for headers that carry the real client IP.

Release mode disables debug logging and improves performance. For high traffic the FAQ also suggests `gin.New()` instead of `gin.Default()` for manual middleware control, and a reverse proxy (nginx, HAProxy) for load balancing.

## Return 405 instead of 404
By default Gin answers 404 for a route that exists with a different method. Enable 405:

```go
r := gin.Default()
r.HandleMethodNotAllowed = true
```

Then `curl -X POST localhost:8080/ping` on a GET-only route gives `HTTP/1.1 405 Method Not Allowed` with `Allow: GET`.

## Gotcha
The deployment page lists managed hosts (Railway, Seenode, Koyeb, Qovery, Render, Google App Engine). On App Engine the standard environment prevents syscalls; the flexible environment can run any framework or library.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: deployment/index.md and faq/index.md. Confirmed: the PORT and GIN_MODE table (debug, release, test), SetMode, the three Run() forms, SetTrustedProxies comment, release mode disabling debug logging, gin.New() and a reverse proxy for high traffic, the HandleMethodNotAllowed 405 behaviour with Allow: GET, and the hosting list with the App Engine standard versus flexible note. Trimmed nothing.

Method: documentation only; no commands were run.
