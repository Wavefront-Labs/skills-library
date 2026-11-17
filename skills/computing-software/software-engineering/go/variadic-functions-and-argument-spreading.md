---
id: computing-software.software-engineering.go.variadic-functions-and-argument-spreading
name: variadic-functions-and-argument-spreading
category: computing-software
field: software-engineering
product: go
tags: [go, go-functions-methods, go-variadic-functions, variadic]
level: practitioner
status: docs-checked
description: "Write and call variadic Go functions, spread slices with ..., and avoid aliasing and nil-versus-empty surprises."
sources:
  - https://go.dev/ref/spec#Passing_arguments_to_..._parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Variadic functions and spreading

**Goal:** accept "zero or more" arguments without aliasing bugs.

```go
func Join(sep string, parts ...string) string { /* parts is []string */ }
Join(",")                  // parts == nil
Join(",", "a", "b")        // new slice created for the call
xs := []string{"a", "b"}
Join(",", xs...)           // passes xs itself, NOT a copy
```

The spec: only the final parameter of a function may have a `...T` type; inside the function its type is `[]T`. With no arguments for it, the parameter is `nil`. With individual arguments, a new slice with a new underlying array is created per call. If the final argument is assignable to `[]T` and followed by `...`, it is passed unchanged and no new slice is created, so the function sees the same underlying array as the caller's slice. Mutating `parts[0]` therefore changes `xs[0]`, and slices sharing an array can change each other.

## Gotchas
- A `...` spread supplies the whole variadic parameter: you cannot mix individual values and a spread slice for the same `...T` parameter.
- `[]string` is not assignable to `[]any`, so `f(xs...)` with a `...any` parameter does not compile; convert element by element.
- Distinguish "none given" (`nil`) from "empty slice given" (non-nil, length 0) only if you really must.
- Copy before mutating or retaining the slice if the caller may have spread its own slice into the call.

## Verify
Test a function that mutates its variadic slice and assert the caller's slice is unchanged after you add a copy.

## Checked
Checked 2026-11-08 against the Go specification (Function types, Passing arguments to ... parameters, Slice types) on the single-page spec. The `[]string` to `[]any` point follows from the passed-unchanged rule (the slice type must be assignable to `[]T`).
Removed as not in the spec: the `go vet` printf-wrapper naming advice and `slices.Clone` usage.
Method: documentation only; no commands were run.
