---
id: computing-software.web-development.gin.gin-structured-logging
name: gin-structured-logging
category: computing-software
field: web-development
product: gin
tags: [gin, logging, structured-logging, slog, zerolog, request-id, x-request-id, json-logs]
level: practitioner
status: docs-checked
description: "Emit JSON request logs from Gin with a log/slog or zerolog middleware, add an X-Request-ID correlation ID, and follow the docs' structured logging best practices."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/structured-logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Structured logging in Gin

Goal: machine-readable (JSON) request logs for ELK, Datadog or Grafana Loki instead of Gin's plain-text default.

## slog middleware (Go 1.21+)
```go
func SlogMiddleware(logger *slog.Logger) gin.HandlerFunc {
  return func(c *gin.Context) {
    start := time.Now()
    path := c.Request.URL.Path
    query := c.Request.URL.RawQuery

    c.Next()

    logger.Info("request",
      slog.String("method", c.Request.Method),
      slog.String("path", path),
      slog.String("query", query),
      slog.Int("status", c.Writer.Status()),
      slog.Duration("latency", time.Since(start)),
      slog.String("client_ip", c.ClientIP()),
      slog.Int("body_size", c.Writer.Size()),
    )
    for _, err := range c.Errors {
      logger.Error("request error", slog.String("error", err.Error()))
    }
  }
}

logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
r := gin.New()
r.Use(SlogMiddleware(logger))
r.Use(gin.Recovery())
```

## Request ID
Reuse an incoming `X-Request-ID` or create one with `github.com/google/uuid`, store it with `c.Set("request_id", id)`, echo it with `c.Header("X-Request-ID", id)`, then read it in the logger with `c.Get("request_id")` after `c.Next()`. The page's example registers `RequestIDMiddleware` before `SlogMiddleware`.

## zerolog middleware
```go
log.Info().
  Str("method", c.Request.Method).
  Str("path", c.Request.URL.Path).
  Int("status", c.Writer.Status()).
  Dur("latency", time.Since(start)).
  Str("client_ip", c.ClientIP()).
  Msg("request")
```
For development the docs switch to pretty output when `gin.Mode() == gin.DebugMode`: `log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})`.

## Best practices stated
- JSON in production, human-readable in development.
- Propagate `X-Request-ID` across services.
- `Info` for normal requests, `Warn` for 4xx, `Error` for 5xx.
- Exclude passwords, tokens and PII.
- Set `GIN_MODE=release` to disable Gin's default debug logging in production.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: logging/structured-logging.md. Confirmed: slog on Go 1.21+, the slog and zerolog middleware, the X-Request-ID middleware with google/uuid, the DebugMode ConsoleWriter, and the five best-practice bullets. Reworded one claim: the page registers the request-ID middleware first in its example but does not state it as a rule.

Method: documentation only; no commands were run.
