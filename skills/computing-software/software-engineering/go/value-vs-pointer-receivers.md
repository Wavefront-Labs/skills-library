---
id: computing-software.software-engineering.go.value-vs-pointer-receivers
name: value-vs-pointer-receivers
category: computing-software
field: software-engineering
product: go
tags: [go, golang, pointer-receivers, method-sets, value-receivers, addressability, copylocks, interface-satisfaction]
level: practitioner
status: docs-checked
description: "Choose value or pointer receivers in Go, understand method sets and why *T satisfies an interface that T does not, and avoid copying mutexes."
sources: ["https://go.dev/doc/faq#methods_on_values_or_pointers", "https://go.dev/ref/spec#Method_sets", "https://go.dev/wiki/CodeReviewComments#receiver-type", "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/copylock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Value vs pointer receivers

**Goal:** methods that mutate what you think they mutate, types that satisfy the
interfaces you expect, and no silently copied locks.

## Rules for choosing
Use a **pointer receiver** `func (s *Server) ...` when:
- the method modifies the receiver;
- the struct contains a `sync.Mutex` or other no-copy field;
- the struct is large (copying per call is waste);
- for consistency: if ANY method needs a pointer receiver, make them all pointers.

Use a **value receiver** `func (p Point) ...` for small immutable values (time.Time,
coordinates), maps/funcs/chans types, and basic named types (`type Celsius float64`).

## Method sets
- Type `T` has methods with value receivers.
- Type `*T` has methods with value AND pointer receivers.
Consequence:
```go
type Saver interface{ Save() error }
func (d *Doc) Save() error { ... }

var s Saver = Doc{}    // compile error: Doc does not implement Saver (Save has pointer receiver)
var s Saver = &Doc{}   // OK
```
Calling `d.Save()` on an addressable variable `d Doc` works (Go takes `&d` for you), but
values stored in interfaces or map entries are not addressable, so that shortcut does
not apply there.

## The silent-mutation bug
```go
func (c Counter) Inc() { c.n++ }   // increments a copy; caller sees no change
```
Code review and tests catch this.

## Copying locks
```go
type Cache struct { mu sync.Mutex; m map[string]string }
func (c Cache) Get(k string) string { c.mu.Lock(); ... }   // locks a COPY: no protection
```
The copylocks analyzer of `go vet` reports locks copied by value. Just always use
`*Cache`. Also never copy a struct containing a mutex after first use.

## Nil receivers
Pointer-receiver methods can be called on nil pointers; design for it where useful
(`func (t *Tree) Len() int { if t == nil { return 0 } ... }`).

## Checked
2026-10-28: Confirmed in the Go FAQ (methods on values or pointers), the language specification (method sets, addressability), Code Review Comments (receiver type) and the copylocks analyzer page. Removed the claim that go vet never flags a value-receiver mutation and the quoted vet message.
Method: documentation only; no commands were run.

## Verify
- [ ] `go vet ./...` clean (copylocks).
- [ ] Each type's receivers are consistently all-pointer or all-value.
- [ ] Interface conformance asserted with `var _ I = (*T)(nil)`.
