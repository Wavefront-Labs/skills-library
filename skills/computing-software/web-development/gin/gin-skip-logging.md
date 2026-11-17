---
id: computing-software.web-development.gin.gin-skip-logging
name: gin-skip-logging
category: computing-software
field: web-development
product: gin
tags: [gin, logging, loggerconfig, skippaths, skip, loggerwithconfig, health-check]
level: practitioner
status: docs-checked
description: "Exclude health checks or successful responses from Gin logs using LoggerConfig SkipPaths and a Skip func(c *gin.Context) bool passed to gin.LoggerWithConfig."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/skip-logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Skip logging for paths or conditions

Goal: keep noisy requests (health checks, metrics) out of the Gin log.

- `SkipPaths` excludes specific routes.
- `Skip` is a function receiving `*gin.Context` that returns `true` to skip logging, for conditional logic such as skipping successful responses.

```go
router := gin.New()

loggerConfig := gin.LoggerConfig{SkipPaths: []string{"/metrics"}}

// skip anything that is not a server-side error
loggerConfig.Skip = func(c *gin.Context) bool {
  return c.Writer.Status() < http.StatusInternalServerError
}

router.Use(gin.LoggerWithConfig(loggerConfig))
router.Use(gin.Recovery())

// skipped: path is in SkipPaths
router.GET("/metrics", func(c *gin.Context) { c.Status(http.StatusNotImplemented) })
// skipped: status < 500
router.GET("/ping", func(c *gin.Context) { c.String(http.StatusOK, "pong") })
// not skipped: status is 501 (>= 500)
router.GET("/data", func(c *gin.Context) { c.Status(http.StatusNotImplemented) })
```

## Try it
```sh
curl http://localhost:8080/data     # logged (status 501 >= 500)
curl http://localhost:8080/metrics  # NOT logged (path in SkipPaths)
curl http://localhost:8080/ping     # NOT logged (200 < 500); output: pong
```

## Gotcha
Both options are fields of `gin.LoggerConfig`, and the docs install them with `gin.LoggerWithConfig(loggerConfig)`. The example's `Skip` func returns true for any status below 500, so only server-side errors are logged there.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: logging/skip-logging.md. Confirmed: SkipPaths and the Skip func on LoggerConfig, the example that skips status below 500, and the three curl expectations. Trimmed nothing.

Method: documentation only; no commands were run.
