---
id: computing-software.web-development.gin.gin-skip-query-string-logging
name: gin-skip-query-string-logging
category: computing-software
field: web-development
product: gin
tags: [gin, logging, skipquerystring, loggerconfig, loggerwithconfig, privacy, pii]
level: practitioner
status: docs-checked
description: "Strip query strings such as tokens from Gin request logs by setting SkipQueryString: true in gin.LoggerConfig and installing it with gin.LoggerWithConfig."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/avoid-logging-query-strings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Avoid logging query strings

Goal: keep API tokens, passwords, session IDs or PII in query strings out of your logs (the docs mention GDPR and HIPAA as regulatory concerns).

Set `SkipQueryString` in `LoggerConfig`. A request to `/path?token=secret&user=alice` is then logged simply as `/path`.

```go
func main() {
  router := gin.New()

  // SkipQueryString indicates that the logger should not log the query string.
  // For example, /path?q=1 will be logged as /path
  loggerConfig := gin.LoggerConfig{SkipQueryString: true}

  router.Use(gin.LoggerWithConfig(loggerConfig))
  router.Use(gin.Recovery())

  router.GET("/search", func(c *gin.Context) {
    q := c.Query("q")
    c.String(200, "searching for: "+q)
  })

  router.Run(":8080")
}
```

## Compare the output
```bash
curl "http://localhost:8080/search?q=gin&token=secret123"
```

Without the option:
```
[GIN] 2025/06/01 - 15:04:05 | 200 |     102.4µs |       127.0.0.1 | GET      "/search?q=gin&token=secret123"
```

With `SkipQueryString: true`:
```
[GIN] 2025/06/01 - 15:04:05 | 200 |     102.4µs |       127.0.0.1 | GET      "/search"
```

## Gotcha
Only the log output changes: your handlers still read parameters through `c.Query()`. This matters most when logs are forwarded to third-party services or stored long term.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: logging/avoid-logging-query-strings.md. Confirmed: SkipQueryString in LoggerConfig, the GDPR and HIPAA mention, the before and after log lines, and that c.Query still works. Trimmed nothing.

Method: documentation only; no commands were run.
