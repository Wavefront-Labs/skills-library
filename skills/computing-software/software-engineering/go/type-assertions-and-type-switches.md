---
id: computing-software.software-engineering.go.type-assertions-and-type-switches
name: type-assertions-and-type-switches
category: computing-software
field: software-engineering
product: go
tags: [go, type-switch, type-assertion, interfaces, nil-interface, optional-interfaces, effective-go, go-switch-forms]
level: practitioner
status: docs-checked
description: "Use Go type assertions and switches safely: comma-ok form, type switches, optional interface upgrades (io.WriterTo), the typed-nil-in-interface trap, and errors.As instead."
sources: ["https://go.dev/ref/spec#Type_assertions", "https://go.dev/ref/spec#Type_switches", "https://go.dev/doc/effective_go#type_switch", "https://go.dev/doc/faq#nil_error"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Type assertions and type switches

**Goal:** recover concrete types from interfaces without panics, and avoid the famous
non-nil nil interface bug.

## Assertions
```go
var v any = getValue()
s := v.(string)            // panics if v is not a string
s, ok := v.(string)        // comma-ok: never panics; ok=false, s=""
if w, ok := out.(io.StringWriter); ok {
    w.WriteString(msg)     // optional fast path
}
```
Asserting to an interface type checks whether the dynamic type implements it.

## Type switches
```go
func describe(v any) string {
    switch x := v.(type) {
    case nil:
        return "nil"
    case int, int64:
        return fmt.Sprintf("integer %v", x)     // x is `any` in multi-type cases
    case string:
        return "string of len " + strconv.Itoa(len(x))
    case fmt.Stringer:
        return x.String()
    case error:
        return "error: " + x.Error()
    default:
        return fmt.Sprintf("unknown %T", x)
    }
}
```
Cases are checked in order: put specific types before broad interfaces.

## Optional interface upgrades
The stdlib pattern: accept a small interface, check for a richer one. `io.Copy` uses
`io.WriterTo`/`io.ReaderFrom` when available; `http.ResponseWriter` may implement
`http.Flusher`. Wrappers (middleware response writers) hide these unless they forward them -
use `http.ResponseController` (Go 1.20) which unwraps.

## Errors: use errors.As
```go
var pe *fs.PathError
if errors.As(err, &pe) { log.Println(pe.Path) }    // walks the wrap chain
```
`err.(*fs.PathError)` fails on wrapped errors (`fmt.Errorf("...: %w", err)`).

## The typed nil trap
An interface is nil only if both its type and value are nil:
```go
func find() error {
    var e *MyErr = nil
    if notFound { e = &MyErr{} }
    return e              // returns a non-nil error interface holding (*MyErr)(nil)!
}
if err := find(); err != nil { ... }   // always true
```
Return a literal `nil` for the interface: `if e == nil { return nil }`. Same issue with any
interface-typed return (io.Reader, etc.).

## Generics instead of any
If a function only switches on a closed set of types to do the same thing, a type parameter
with a constraint (`[T int | int64 | float64]`) is clearer and checked at compile time.

## Verify
- [ ] No single-value assertions on untrusted values (use comma-ok or a switch).
- [ ] Functions returning error interfaces return untyped `nil` on success.

## Checked

- Date: 2026-10-28
- Confirmed on go.dev (language spec type assertions and type switches, Effective Go, FAQ nil error) and pkg.go.dev (errors.As, net/http ResponseController added in Go 1.20, io, net/http Flusher): comma-ok form, typed-nil interface trap, errors.As walking the chain.
- Removed: staticcheck check number.
Method: documentation only; no commands were run.
