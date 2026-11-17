---
id: computing-software.web-development.gin.gin-quickstart-first-app
name: gin-quickstart-first-app
category: computing-software
field: web-development
product: gin
tags: [gin, go, gin-default, quickstart, r-run, ping-endpoint, install]
level: intro
status: docs-checked
description: "Import Gin, build a router with gin.Default(), serve a JSON /ping endpoint with r.Run() on port 8080, and know the Go version Gin requires."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/index.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/introduction/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin first application

Goal: get a minimal Gin HTTP server answering with JSON.

Prerequisite: Gin requires Go 1.25 or above. With Go modules, just import Gin and Go fetches it during build:

```go
import "github.com/gin-gonic/gin"
```

## Minimal server

```go
package main

import (
  "net/http"

  "github.com/gin-gonic/gin"
)

func main() {
  // Router with default middleware (logger and recovery)
  r := gin.Default()

  r.GET("/ping", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
      "message": "pong",
    })
  })

  // Start server on port 8080 (default)
  r.Run()
}
```

## Run it
1. Save as `main.go`.
2. `go run main.go`
3. Visit `http://localhost:8080/ping`; you should see `{"message":"pong"}`.

## Notes from the docs
- `gin.Default()` attaches the logger and recovery middleware.
- `r.Run()` listens on 0.0.0.0:8080 (localhost:8080 on Windows).
- Gin is built on httprouter and describes its router as zero allocation. Its stated features include middleware chains, panic recovery, JSON validation, route grouping, error management and built-in JSON/XML/HTML rendering.
- Gin v1 is described as stable with a frozen API.
- Further runnable examples live in the gin-gonic/examples repository.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: docs/index.md, introduction/index.md and quickstart/index.md. Confirmed: Go 1.25 or above, gin.Default() with logger and recovery, r.Run() on 0.0.0.0:8080 (localhost:8080 on Windows), the /ping example and output, httprouter and zero allocation router, the feature list, and Gin v1 stable with a frozen API. Trimmed nothing. The linked examples repository was not opened.

Method: documentation only; no commands were run.
