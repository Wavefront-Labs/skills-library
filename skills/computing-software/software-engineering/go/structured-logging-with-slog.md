---
id: computing-software.software-engineering.go.structured-logging-with-slog
name: structured-logging-with-slog
category: computing-software
field: software-engineering
product: go
tags: [go, go-stdlib, slog, structured-logging, log-slog, context-logging, observability, go-logging-observability, go-slog-handlers]
level: practitioner
status: verified
description: "Log in Go with log/slog: JSON handlers, levels, attributes and groups, request-scoped loggers, LogValuer for redaction, performance and integrating with tracing."
sources:
  - https://pkg.go.dev/log/slog
  - https://go.dev/blog/slog
  - https://github.com/golang/example/blob/master/slog-handler-guide/README.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Structured logging with log/slog

**Goal:** machine-parseable logs with consistent keys, request context and no secrets, using only the standard library.

## 1. Setup
```go
level := new(slog.LevelVar)                       // changeable at runtime
level.Set(slog.LevelInfo)
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level:     level,
    AddSource: false,
    ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
        if a.Key == slog.TimeKey { a.Value = slog.StringValue(a.Value.Time().UTC().Format(time.RFC3339Nano)) }
        return a
    },
}))
slog.SetDefault(logger)                           // also routes the old log package through slog
```
`TextHandler` for local development, `JSONHandler` in production.

## 2. Logging calls
```go
slog.Info("order placed", "order_id", id, "amount", amt)               // alternating key/values
logger.LogAttrs(ctx, slog.LevelInfo, "order placed",                     // typed, zero-alloc fast path
    slog.String("order_id", id), slog.Int64("amount", amt))
logger.Error("charge failed", "err", err, "order_id", id)
```
`go vet` checks for mismatched key/value pairs (`slog` analyzer). Agree on key names (`err`, `user_id`, `trace_id`) team-wide.

## 3. Child loggers and groups
```go
reqLog := logger.With("request_id", rid, "route", r.Pattern)
dbLog := logger.WithGroup("db")                 // keys nested: {"db": {"query_ms": 12}}
dbLog.Info("slow query", "query_ms", 12)
```
Pass loggers explicitly or store one in the context in middleware:
```go
type ctxKey struct{}
func FromContext(ctx context.Context) *slog.Logger {
    if l, ok := ctx.Value(ctxKey{}).(*slog.Logger); ok { return l }
    return slog.Default()
}
```

## 4. Redaction with LogValuer
```go
type Token string
func (Token) LogValue() slog.Value { return slog.StringValue("REDACTED") }
type User struct { ID, Email string }
func (u User) LogValue() slog.Value { return slog.GroupValue(slog.String("id", u.ID)) }   // omit email
```
LogValue is resolved lazily, only when the record is actually emitted.

## 5. Tracing correlation
A handler wrapper can add `trace_id`/`span_id` from the context's OpenTelemetry span to every record (`otelslog` bridge), as long as you call the `...Context` variants (`InfoContext(ctx, ...)`).

## Gotchas
- `slog.Info("msg", err)` with an odd argument count logs `!BADKEY`; always use key/value pairs or Attrs.
- Expensive values computed before the call run even if the level is disabled; check `logger.Enabled(ctx, level)` or use LogValuer.
- Do not log full request bodies or headers (Authorization, cookies); log IDs.
- Duplicate keys are emitted twice by the JSON handler; avoid adding the same key in `With` and the call.

## Verify
- Pipe output through `jq` in tests or locally: every line is valid JSON with `time`, `level`, `msg`, request IDs present on request logs, and secrets appear as REDACTED.

## Checked
- Go 1.25.1: the JSON handler setup with `LevelVar` (debug hidden then visible after `Set`), `ReplaceAttr`, `SetDefault` routing the old `log` package through slog, `LogAttrs`, `With`, `WithGroup` (`"db":{"query_ms":12}`), `LogValuer` redaction (`REDACTED`, group without email), lazy `LogValue` resolved only when the record is emitted, `!BADKEY` for a lone error and an odd trailing key, duplicate keys emitted twice (also between `With` and the call), `Enabled`, the context logger helper, `TextHandler`, `http.Request.Pattern`; `go vet` reports `call to slog.Info missing a final value`. The OpenTelemetry `otelslog` bridge and the `jq` pipe were not run.
