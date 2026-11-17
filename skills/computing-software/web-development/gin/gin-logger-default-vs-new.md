---
id: computing-software.web-development.gin.gin-logger-default-vs-new
name: gin-logger-default-vs-new
category: computing-software
field: web-development
product: gin
tags: [gin, logging, gin-default, gin-new, gin-logger, recovery, middleware]
level: intro
status: docs-checked
description: "Understand which middleware gin.Default() attaches versus gin.New(), and add the built-in Gin logger manually with router.Use(gin.Logger())."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/index.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/write-log.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/skip-logging.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/controlling-log-output-coloring.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/custom-log-format.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin built-in logger: Default vs New

Goal: control whether request logging is on, and attach it by hand when needed.

Gin's logger middleware records details about each HTTP request, including status code, HTTP method, path and latency.

## gin.Default()
Creates a router with the logger and recovery middleware already attached:

```go
router := gin.Default()
```

## gin.New()
Attaches no middleware. Use this for full control, then add the logger yourself:

```go
router := gin.New()
router.Use(gin.Logger())
```

## Default output
The default logger writes to `os.Stdout`. One entry per request looks like:

```
[GIN] 2025/06/01 - 15:04:05 | 200 |     512.345µs |       127.0.0.1 | GET      "/ping"
```

Each entry carries a timestamp, status code, latency, client IP, HTTP method and requested path.

## Related logging topics
- Redirect output to a file: set `gin.DefaultWriter`.
- Custom line format: `gin.LoggerWithFormatter`.
- Skip paths or conditions: `gin.LoggerWithConfig` with `LoggerConfig`.
- Colour control: `gin.DisableConsoleColor()` and `gin.ForceConsoleColor()`.

## Gotcha
`gin.New()` attaches no middleware, so without `router.Use(gin.Logger())` you get no request logs, and recovery is only present if you add `gin.Recovery()` yourself.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Logging index, Write log, Skip logging, Controlling log output coloring, Custom log format (Default vs New, default output, DefaultWriter, LoggerWithConfig, color functions).
Removed or corrected: nothing (added pages that confirm the related-topics list).

Method: documentation only; no commands were run.
