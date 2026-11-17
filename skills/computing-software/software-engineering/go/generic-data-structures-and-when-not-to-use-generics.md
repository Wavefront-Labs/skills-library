---
id: computing-software.software-engineering.go.generic-data-structures-and-when-not-to-use-generics
name: generic-data-structures-and-when-not-to-use-generics
category: computing-software
field: software-engineering
product: go
tags: [go, go-generics, go-generic-structures, generic-types, data-structures]
level: practitioner
status: docs-checked
description: "Build type-safe generic containers in Go, know their method limits, and decide when an interface or plain code is better."
sources:
  - https://go.dev/blog/when-generics
  - https://go.dev/ref/spec#Type_parameter_declarations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generic data structures (and when to skip generics)

**Goal:** use type parameters for containers and algorithms, not for polymorphic behaviour.

```go
type Stack[T any] struct{ items []T }

func (s *Stack[T]) Push(v T) { s.items = append(s.items, v) }
func (s *Stack[T]) Pop() (T, bool) {
    var zero T
    if len(s.items) == 0 { return zero, false }
    v := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return v, true
}

func Map[T, U any](xs []T, f func(T) U) []U { /* ... */ }
```

Rules from the spec: a generic type must be instantiated when used (`Stack[int]`); a generic function must be instantiated before it can be called or used as a value (inference usually does this). A method may use its receiver's type parameters; since Go 1.27 a method declaration may also declare its own type parameters (before 1.27 it could not, so check your toolchain version). Interface methods cannot declare type parameters, though they may use the interface's.

When to use them (go.dev "When to use generics"): write code first and add type parameters when they prove useful. They suit functions over slices, maps and channels that make no assumptions about element types, general purpose data structures (a tree, a linked list), and methods that look identical across types. Prefer an interface when you only call a method on a value (`io.Reader`), or when implementations differ per type; use reflection when types have no common methods and the operation differs per type (as `encoding/json` does). For a data structure that needs a comparison, take a comparison function rather than requiring a method in the constraint.

## Gotchas
- Zero values: return `var zero T` plus an ok flag instead of `nil`.
- The blog notes that in the Go 1.18 implementation values of a type-parameter type are often treated much like interface values, so do not move from interfaces to type parameters just for speed.
- Constraints on an exported API become part of its compatibility surface.

## Checked
2026-11-09. Confirmed on go.dev/blog/when-generics (guidelines above, function-over-method advice, no speed gain from replacing interfaces) and the Go spec (instantiation rules, interface methods cannot declare type parameters, generic methods added in Go 1.27 in the version-history list).
Corrected: the old rule "methods cannot declare their own type parameters" now carries the Go 1.27 caveat. Removed: GC-shape stenciling claim, the `-race` advice and the "no generic method on an interface value" wording.
Method: documentation only; no commands were run.

## Verify
Instantiate with `int`, `string` and a struct, and benchmark against a hand-written `[]int` stack if performance matters.
