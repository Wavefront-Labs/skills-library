---
id: computing-software.software-engineering.go.comparable-types-and-map-keys
name: comparable-types-and-map-keys
category: computing-software
field: software-engineering
product: go
tags: [go, go-types-values, go-comparable-types, comparable, map-keys]
level: practitioner
status: docs-checked
description: "Know which Go types are comparable, what == does on structs, interfaces and arrays, and how to build safe composite map keys."
sources:
  - https://go.dev/ref/spec#Comparison_operators
  - https://go.dev/ref/spec#Map_types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Comparable types and map keys

**Goal:** pick map keys and use `==` without runtime panics or accidental identity semantics.

Comparable (per the spec): booleans, integers, floats, complex numbers, strings, pointers, channels, interfaces (equal when dynamic types are identical and dynamic values equal), arrays of comparable element types, and structs whose fields are all comparable. Not comparable: slices, maps, functions (except comparison to `nil`). Struct fields are compared in source order, skipping blank fields, stopping at the first difference.

A comparison of two interface values with identical dynamic types **panics at run time** if that type is not comparable; the same applies to arrays of interface values and structs with interface-valued fields. For maps, the key type must not be a function, map or slice; with an interface key type, a non-comparable dynamic key value causes a run-time panic.

```go
type Key struct {
    Tenant string
    ID     [16]byte
}
m := map[Key]int{}
m[Key{"acme", id}]++        // composite keys avoid string concatenation

var a, b any = []int{1}, []int{1}
_ = a == b                  // run-time panic: comparing uncomparable type []int
```

In generics use the predeclared constraint `comparable`, e.g. `func Index[T comparable](s []T, v T) int`. Interface types satisfy `comparable` but do not implement it, and the spec warns that comparing values of a type parameter may therefore still panic at run time.

## Gotchas
- A pointer key compares addresses (equal if they point to the same variable), not pointees.
- Pointers to distinct zero-size variables may or may not be equal.
- Adding a slice field to a struct later makes the struct non-comparable: a compile error where it is a map key, a run-time panic where it travels through interfaces.

## Verify
Add a test that inserts and looks up a representative key, and a `recover`-based test showing interface comparison of non-comparable values panics, so reviewers see the hazard.

## Checked
Checked 2026-11-08 against the Go specification (Comparison operators, Map types, Interface types and the `comparable` constraint), read on the single-page spec.
Removed as not in the spec: `slices.Equal` and `reflect.DeepEqual` remarks and the NaN map-key behaviour.
Method: documentation only; no commands were run.
