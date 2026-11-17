---
id: computing-software.software-engineering.go.nil-interface-vs-nil-pointer-trap
name: nil-interface-vs-nil-pointer-trap
category: computing-software
field: software-engineering
product: go
tags: [go, go-interfaces, go-nil-interface-trap, nil-interface, typed-nil]
level: practitioner
status: docs-checked
description: "Avoid the Go typed-nil bug where a nil pointer stored in an error or interface compares non-nil."
sources:
  - https://go.dev/doc/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The typed-nil interface trap

**Goal:** never return a nil pointer wrapped in a non-nil interface.

An interface value is two elements, a type T and a value V (its dynamic value). It is nil only if T and V are both unset. Storing a nil pointer of type `*int` gives `(T=*int, V=nil)`, which is non-nil.

```go
func returnsError() error {
    var p *MyError = nil
    if bad() {
        p = ErrBad
    }
    return p // always a non-nil error
}
```

If all goes well, the caller still sees `(T=*MyError, V=nil)` and `err != nil` is true. Fix: return an explicit `nil`.

```go
func returnsError() error {
    if bad() {
        return ErrBad
    }
    return nil
}
```

Use the `error` type in function signatures rather than a concrete type such as `*MyError`, to help guarantee the error is created correctly; the FAQ's example is `os.Open`, which returns `error` although a non-nil value is always a `*os.PathError`. The same situation arises whenever any concrete value is stored in an interface.

## Gotchas
- A helper returning a concrete pointer type whose result is then assigned to `error` hits this.

## Checked
Date: 2026-11-09. Confirmed against the Go FAQ entry "Why is my nil error value not equal to nil?" (go.dev/doc/faq): the (type, value) model, the `*MyError` example and explicit-nil fix, the advice to return `error`, and the `os.Open` example. Removed unconfirmed claims: nil-receiver method remarks, `errors.As` and `reflect` notes, the `io.Writer` example, and the unit-test suggestion.
Method: documentation only; no commands were run.
