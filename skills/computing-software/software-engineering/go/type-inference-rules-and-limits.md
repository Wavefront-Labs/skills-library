---
id: computing-software.software-engineering.go.type-inference-rules-and-limits
name: type-inference-rules-and-limits
category: computing-software
field: software-engineering
product: go
tags: [go, go-generics, go-type-inference, type-inference, generic-functions]
level: practitioner
status: docs-checked
description: "Understand when Go infers type arguments (function arguments, constraint types) and when you must instantiate explicitly."
sources:
  - https://go.dev/blog/type-inference
  - https://go.dev/ref/spec#Type_inference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Type inference rules and limits

**Goal:** write generic calls that compile without noise and fix "cannot infer T" errors.

Inference uses (1) typed function arguments, (2) assignment context for function values since Go 1.21, and (3) constraint type inference (core types).

```go
func Sum[S ~[]E, E int | float64](s S) E { var t E; for _, v := range s { t += v }; return t }
type IDs []int
Sum(IDs{1, 2})              // S=IDs, E inferred from S's core type

func Zero[T any]() T { var z T; return z }
_ = Zero[int]()              // explicit: no argument to infer from

var f func(int) string = Convert // Go 1.21: infers Convert's type arguments from f
```

Typed arguments take precedence over untyped constants; an untyped constant is considered only if its type parameter has no inferred type yet, and then its default type is used. If several untyped numeric constants compete for one type parameter, Go 1.21+ picks the later of the default types int, rune, float64, complex (so `foo(1, 2.0)` infers `float64`, like the constant expression `1 + 2.0`); before Go 1.21 this was an inference error.

## Gotchas
- Type inference only considers types that contain type parameters of the function involved; when there is nothing to infer from (as in `Zero[T any]()`), supply the type argument explicitly.
- A constraint like `~[]E` has a core type, which is what lets inference deduce `E` from the argument type; constraints such as `any` have none and are ignored for this.
- The tilde in `~[]E` allows named slice types; without it `IDs` would not satisfy the constraint.

## Verify
Compile with the toolchain pinned in `go.mod` and add a test calling the function with a named type to prove `~` works.

## Checked
2026-11-03. Confirmed on go.dev/blog/type-inference: typed-over-untyped precedence, default-type rule and the Go 1.21 change, assignment of generic functions to function-typed variables (Go 1.21), core-type constraint inference. Removed: "return types never drive inference", type-parameter ordering advice with `Cast`, the "cannot infer T" literal message, and "errors improve per release" note. The go.dev/ref/spec section was fetched but is a very large page; no claim here rests on it alone.
Method: documentation only; no commands were run.
