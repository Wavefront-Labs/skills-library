---
id: computing-software.software-engineering.go.method-values-and-method-expressions
name: method-values-and-method-expressions
category: computing-software
field: software-engineering
product: go
tags: [go, go-functions-methods, go-method-values, method-value, method-expression]
level: practitioner
status: docs-checked
description: "Use bound method values and method expressions in Go, and know when the receiver is copied."
sources:
  - https://go.dev/ref/spec#Method_values
  - https://go.dev/ref/spec#Method_expressions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Method values and method expressions

**Goal:** pass methods as functions correctly.

A **method value** `x.M` is a function value callable like the method call `x.M`. The expression `x` is evaluated and saved when the method value is created, and the saved copy is the receiver of every later call. A **method expression** `T.M` or `(*T).M` yields a function whose first parameter is the receiver.

```go
type Counter struct{ n int }
func (c Counter) Value() int { return c.n }
func (c *Counter) Inc()      { c.n++ }

c := Counter{}
f := c.Value      // receiver COPIED now
c.Inc()
fmt.Println(f())  // 0, not 1
g := c.Inc        // same as (&c).Inc: c is addressable, so g() mutates c
g()
h := (*Counter).Inc  // func(*Counter)
h(&c)
http.HandleFunc("/x", srv.handle) // method value as a callback
```

For a value receiver the receiver value is copied when the method value is created; for a pointer receiver the pointer is saved. With a pointer receiver, `t.Mp` is allowed only when `t` is addressable: `makeT().Mp` is invalid because the result of `makeT()` is not addressable. A method value may also be taken from an interface value (`f := i.M`). Evaluating a method value from a nil interface value causes a run-time panic at that point, not when the function is later called.

Method expressions: `T.Mv` has the signature `func(tv T, a int) int` (receiver first); `(*T).Mv` is legal for a value-receiver method and indirects through the pointer without modifying the pointee; `T.Mp` for a pointer-receiver method is illegal because pointer-receiver methods are not in the method set of `T`. Calls use `f(t, 7)`, not `t.f(7)`.

## Gotchas
- Because the receiver is saved when the method value is evaluated, a method value used later (stored, passed as a callback) sees the state at that moment for value receivers; use a function literal `func() int { return c.Value() }` for late evaluation.
- To bind a receiver from a method expression, use a function literal or a method value.

## Verify
Write the test above and assert `f()` stays 0 while `c.Value()` becomes 2.

## Checked
Checked 2026-11-08 against the Go specification (Method values, Method expressions, Selectors) on the single-page spec.
Removed as not in the spec: the GC-retention remark, the `go vet` comment, and the claim about goroutine and `defer` capture timing.
Method: documentation only; no commands were run.
