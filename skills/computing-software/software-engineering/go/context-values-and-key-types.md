---
id: computing-software.software-engineering.go.context-values-and-key-types
name: context-values-and-key-types
category: computing-software
field: software-engineering
product: go
tags: [go, go-context, go-context-values, context-value, request-scoped]
level: practitioner
status: docs-checked
description: "Store request-scoped values in context safely with unexported key types, typed accessors, and clear limits on what belongs there."
sources:
  - https://pkg.go.dev/context
  - https://go.dev/blog/context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# context values and key types

**Goal:** carry request-scoped metadata (request ID, auth principal, trace span) without polluting function signatures.

```go
type ctxKey int
const requestIDKey ctxKey = iota   // unexported type: no collisions across packages

func WithRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, requestIDKey, id)
}
func RequestID(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(requestIDKey).(string)
    return id, ok
}
```

`WithValue` returns a derived context that points to the parent; in the derived context the value for `key` is `val`, and the parent is unchanged. The `context` package docs say to use context values only for request-scoped data that transits processes and APIs, not for passing optional parameters to functions. The Go blog adds that data stored in a context must be safe for simultaneous use by multiple goroutines.

Keys: the key must be comparable and should not be a `string` or other built-in type, to avoid collisions between packages; define your own key type. Packages should define keys as an unexported type and expose typed accessors (the docs' `NewContext`/`FromContext` pattern). Keys often use a concrete `struct{}` type to avoid allocating when assigned to an interface; exported key variables should have a pointer or interface static type.

## Gotchas
- A plain `string` key can collide with keys from other packages.
- Do not store mutable shared state in a context value; values must be safe for concurrent use.
- `context.WithoutCancel` (added in Go 1.21) returns a derived context that is not canceled when the parent is, with no `Deadline` or `Err` and a nil `Done` channel; it keeps the values.

## Verify
Test that `RequestID(context.Background())` returns `ok=false` and that a child derived through `WithTimeout` still sees the ID.

## Checked

Checked 2026-11-09 against pkg.go.dev/context (package overview, `WithValue`, `WithoutCancel`, the key-type example comments) and the go.dev blog post "Go Concurrency Patterns: Context" (Value and key-collision sections).
Confirmed: every point above.
Removed as unconfirmed: linear lookup cost, the staticcheck SA1029 reference, W3C `traceparent` propagation advice, the "do/do not put in context" lists beyond the documented optional-parameters rule, and the statement that values do not cross processes (the package overview says the types carry values across API boundaries and between processes).

Method: documentation only; no commands were run.
