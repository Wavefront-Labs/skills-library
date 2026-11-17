---
id: computing-software.web-development.gin.gin-redirects
name: gin-redirects
category: computing-software
field: web-development
product: gin
tags: [gin, c-redirect, redirect, handlecontext, http-301, http-302, http-307, http-308, internal-redirect]
level: intro
status: docs-checked
description: "Redirect clients in Gin with c.Redirect and status codes 301, 302, 307 or 308, or re-route internally with router.HandleContext."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/redirects.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin redirects

Goal: send a client elsewhere, or forward a request internally.

## HTTP redirects with c.Redirect
- 301 `http.StatusMovedPermanently`: permanent; browsers and search engines update caches.
- 302 `http.StatusFound`: temporary; not cached.
- 307 `http.StatusTemporaryRedirect`: like 302 but the original HTTP method must be preserved.
- 308 `http.StatusPermanentRedirect`: like 301 but the method must be preserved.

```go
router.GET("/old", func(c *gin.Context) {
  c.Redirect(http.StatusMovedPermanently, "https://www.google.com/")
})

// Redirect from POST: use 302 or 307
router.POST("/submit", func(c *gin.Context) {
  c.Redirect(http.StatusFound, "/result")
})
```

## Internal router redirect
Rewrite the path and call `router.HandleContext(c)`; no redirect response reaches the client:

```go
router.GET("/test", func(c *gin.Context) {
  c.Request.URL.Path = "/final"
  router.HandleContext(c)
})
router.GET("/final", func(c *gin.Context) {
  c.JSON(http.StatusOK, gin.H{"hello": "world"})
})
```

```sh
curl -I http://localhost:8080/old              # HTTP/1.1 301 Moved Permanently, Location: https://www.google.com/
curl -X POST -I http://localhost:8080/submit   # HTTP/1.1 302 Found, Location: /result
curl http://localhost:8080/test                # {"hello":"world"}
```

## Gotcha
From a POST handler use 302 or 307, not 301: some browsers may change the method from POST to GET on a 301.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: routing/redirects.md. Confirmed: the 301/302/307/308 descriptions, the POST redirect caution, the HandleContext internal redirect, and the curl results. Trimmed nothing. Fixed the source (bogus website/ segment).

Method: documentation only; no commands were run.
