---
id: computing-software.software-engineering.go.unsafe-pointer-valid-patterns
name: unsafe-pointer-valid-patterns
category: computing-software
field: software-engineering
product: go
tags: [go, go-unsafe-reflect, go-unsafe-pointer, unsafe, unsafe-pointer]
level: sme
status: docs-checked
description: "Use unsafe.Pointer only in the six valid patterns of its documentation and avoid storing uintptr between conversions."
sources:
  - https://pkg.go.dev/unsafe#Pointer
  - https://go.dev/ref/spec#Package_unsafe
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# unsafe.Pointer: the valid patterns

**Goal:** bypass the type system for FFI, syscalls or layout tricks without creating GC-invisible or misaligned pointers.

The `unsafe.Pointer` docs list six valid patterns and warn that code outside them is likely invalid now or in future: (1) convert `*T1` to `*T2` via Pointer, provided T2 is no larger than T1 and the layouts are equivalent; (2) Pointer to `uintptr` but not back (for example to print an address); (3) Pointer to `uintptr` and back with arithmetic, with both conversions in the same expression and the result still inside the original allocated object; (4) Pointer to `uintptr` inside the argument list of a call such as `syscall.Syscall`; (5) the result of `reflect.Value.Pointer` or `UnsafeAddr` converted to Pointer immediately, in the same expression; (6) the `Data` field of `reflect.SliceHeader`/`StringHeader`, only when the header points at an actual slice or string.

```go
// pattern 1: the math.Float64bits implementation
func Float64bits(f float64) uint64 { return *(*uint64)(unsafe.Pointer(&f)) }

// pattern 3: same expression, pointer stays inside the object
f := unsafe.Pointer(uintptr(unsafe.Pointer(&s)) + unsafe.Offsetof(s.f))
```

`unsafe.Add(ptr, len)` (Go 1.17) returns `Pointer(uintptr(ptr) + uintptr(len))`, and the rules for valid uses of Pointer still apply.

Invalid, per the docs: storing the `uintptr` in a variable before converting back (`u := uintptr(p); p = unsafe.Pointer(u + offset)`); advancing a pointer just past the end of its allocation; doing arithmetic on a nil pointer; a directly declared `reflect.StringHeader` or `SliceHeader` variable. A `uintptr` is an integer, not a reference: the garbage collector neither updates it if the object moves nor treats it as keeping the object alive.

## Gotchas
- `unsafe.Offsetof` returns the byte offset of a field within its struct and `unsafe.Sizeof` the size; use them rather than hard-coded numbers.
- `go vet` can help find non-conforming uses of Pointer, but silence from `go vet` is not a guarantee that the code is valid.

## Verify
Run `go vet` on the package and review every conversion against the six patterns by hand; vet silence is not proof.

## Checked
2026-11-03. Confirmed on pkg.go.dev/unsafe: the six patterns and their invalid counterparts, `Add` (go1.17), `Offsetof`/`Sizeof`, the go vet caveat. Corrected: the old list omitted pattern 2 and wrongly counted `unsafe.Add` as one of the six. Removed: `-d=checkptr` and `-race` enabling it, the fuzzing advice, the compiler-release crash claim and the isolate-in-one-package advice (none appear on the fetched page). The go.dev/ref/spec section was not relied on.
Method: documentation only; no commands were run.
