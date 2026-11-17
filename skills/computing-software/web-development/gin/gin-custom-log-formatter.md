---
id: computing-software.web-development.gin.gin-custom-log-formatter
name: gin-custom-log-formatter
category: computing-software
field: web-development
product: gin
tags: [gin, logging, loggerwithformatter, logformatterparams, gin-defaultwriter, middleware]
level: practitioner
status: docs-checked
description: "Define your own request log line in Gin with gin.LoggerWithFormatter and LogFormatterParams fields such as ClientIP, TimeStamp, Method, Path and Latency."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/custom-log-format.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom log format with LoggerWithFormatter

Goal: replace Gin's default request log line with your own string.

`gin.LoggerWithFormatter` takes a function receiving `gin.LogFormatterParams` and returning the line to write. The middleware writes to `gin.DefaultWriter` (by default `os.Stdout`).

```go
func main() {
  router := gin.New()
  router.Use(gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
    return fmt.Sprintf("%s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
        param.ClientIP,
        param.TimeStamp.Format(time.RFC1123),
        param.Method,
        param.Path,
        param.Request.Proto,
        param.StatusCode,
        param.Latency,
        param.Request.UserAgent(),
        param.ErrorMessage,
    )
  }))
  router.Use(gin.Recovery())
  router.GET("/ping", func(c *gin.Context) {
    c.String(200, "pong")
  })
  router.Run(":8080")
}
```

## Fields used in the example
`param.ClientIP`, `param.TimeStamp`, `param.Method`, `param.Path`, `param.Request` (for `Proto` and `UserAgent()`), `param.StatusCode`, `param.Latency`, `param.ErrorMessage`.

## Sample output (from the docs)
```
::1 - [Fri, 07 Dec 2018 17:04:38 JST] "GET /ping HTTP/1.1 200 122.767µs "Mozilla/5.0 (...) Safari/537.36" "
```

## Gotcha
The docs example builds the router with `gin.New()` and adds `gin.Recovery()` itself.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Custom log file/format (LoggerWithFormatter, LogFormatterParams fields, sample output, gin.DefaultWriter).
Removed or corrected: inference that the formatter replaces the default logger.

Method: documentation only; no commands were run.
