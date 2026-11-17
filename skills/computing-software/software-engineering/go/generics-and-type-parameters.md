---
id: computing-software.software-engineering.go.generics-and-type-parameters
name: generics-and-type-parameters
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-generics, type-parameters, constraints, type-sets, comparable, cmp-ordered, slices-package, maps-package, iterators, go-type-constraints]
level: practitioner
status: verified
description: "Use Go generics where they pay off: type parameters and constraints, type sets with ~, comparable, the slices/maps/cmp packages, and when an interface is better."
sources: ["https://go.dev/doc/tutorial/generics", "https://go.dev/blog/when-generics", "https://go.dev/ref/spec#Type_parameter_declarations", "https://pkg.go.dev/slices"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Generics and type parameters

**Goal:** remove copy-pasted per-type helpers and `any` casts, without turning Go into
a template-metaprogramming language.

## Syntax
```go
func Map[T, U any](s []T, f func(T) U) []U {
    out := make([]U, 0, len(s))
    for _, v := range s { out = append(out, f(v)) }
    return out
}

type Number interface { ~int | ~int64 | ~float64 }   // type set; ~ includes named types like `type Cents int64`
func Sum[N Number](xs []N) N { var s N; for _, x := range xs { s += x }; return s }

type Set[K comparable] map[K]struct{}
func (s Set[K]) Add(k K) { s[k] = struct{}{} }
```
Type inference usually lets callers write `Map(users, User.Name)`.

## Use the standard library first
- `slices`: `Sort`, `SortFunc`, `Contains`, `Index`, `BinarySearch`, `Compact` (zeroes the freed tail of the original slice), `Max`, `Sorted` (collect an iterator).
- `maps`: `Keys`, `Values` (iterators since 1.23), `Clone`, `Equal`.
- `cmp`: `cmp.Ordered`, `cmp.Compare`, `cmp.Or` (first non-zero value).
- Range-over-func iterators (1.23): `iter.Seq[T]`, `for v := range seq`.
Old `golang.org/x/exp/constraints` is mostly superseded by `cmp.Ordered`.

## When to use generics (from "When To Use Generics")
- Functions over slices, maps, channels of any element type.
- General-purpose data structures (sets, trees, caches).
- When the implementation is identical for every type.

## When not to
- When you only call methods on the value: use an interface parameter
  (`func Write(w io.Writer)`), not `func Write[W io.Writer](w W)`.
- When implementations differ per type: interfaces/methods.
- Premature: write the concrete version first; generify on the second copy.

## Limitations to know
- Methods may declare their own type parameters only from Go 1.27 (`func (g G[T]) M[U any](u U) U`); before that (go.mod `go` 1.26 or lower) use a function taking the receiver as a parameter. Interface methods still cannot have type parameters.
- No specialisation or operator overloading; `==` requires `comparable`.
- `comparable` includes interfaces, whose `==` can panic at runtime if the dynamic types
  are not comparable.
- Generic code can be slower than hand-written concrete code in hot paths; benchmark before and after.

## Verify
- [ ] `go vet` clean; each generic function has a test with at least two type arguments.
- [ ] No generic function whose type parameter is used only as an interface method receiver.

## Checked
2026-10-21 on Go 1.27.3 (Windows): every snippet (`Map`, `Sum` over a named `Cents` type, `Set[K comparable]`) plus `slices.Sort/SortFunc/Contains/Index/BinarySearch/Compact/Max`, `slices.Sorted(maps.Keys(m))`, `maps.Values/Clone/Equal`, `cmp.Compare/Or`, `iter.Seq` ran; `==` on two `any` holding slices panicked with `comparing uncomparable type []int`. Generic methods compile on Go 1.27 (`func (g G[T]) M[U any](u U) U` ran) and fail on a go.mod of 1.26 with `generic method requires go1.27 or later`; confirmed in https://go.dev/doc/go1.27 (interface methods still cannot have type parameters). `slices.Compact` zeroes the tail of the original slice (observed `[1 2 3 0]`). The dictionary/stenciling performance remark was replaced with a plain 'benchmark hot paths' since it was not measured.
