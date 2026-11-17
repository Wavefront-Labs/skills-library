---
id: computing-software.software-engineering.go.cgo-basics-costs-and-pitfalls
name: cgo-basics-costs-and-pitfalls
category: computing-software
field: software-engineering
product: go
tags: [go, go-build-toolchain, go-cgo, cgo, c-interop]
level: advanced
status: docs-checked
description: "Call C from Go with cgo: pointer passing rules, cgocheck, build flags and cross-compiling, and freeing C memory."
sources:
  - https://pkg.go.dev/cmd/cgo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cgo basics, costs and pitfalls

**Goal:** use C libraries safely and know what you pay.

```go
/*
#cgo LDFLAGS: -lm
#include <math.h>
#include <stdlib.h>
*/
import "C"
import "unsafe"

func Sqrt(x float64) float64 { return float64(C.sqrt(C.double(x))) }

func Dup(s string) *C.char { return C.CString(s) } // caller must C.free(unsafe.Pointer(p))
```

Rules (cmd/cgo docs, "Passing pointers"): a Go pointer passed to C must point to pinned Go memory, which is implicitly pinned for the duration of the call, and the memory must not contain Go pointers to unpinned memory. C code may not keep a copy of a Go pointer after the call returns unless the memory is pinned with `runtime.Pinner` (strings, slices and channels cannot be pinned, so C may not keep them). Use `runtime/cgo.Handle` to safely pass Go values between Go and C.
The rules are checked at run time under `GODEBUG=cgocheck`: the default `cgocheck=1` is reasonably cheap, `cgocheck=0` disables the checks, and `GOEXPERIMENT=cgocheck2` at build time gives complete checking at some run-time cost.
The `#cgo noescape` directive tells the compiler that no Go pointers escape via a named C function; if the C function does not handle the pointer safely, the program may crash or see memory corruption.

Build: `#cgo` directives in the comment set `CFLAGS`, `CPPFLAGS`, `CXXFLAGS`, `FFLAGS` and `LDFLAGS` (or use `#cgo pkg-config:`); prefer directives to the `CGO_*` environment variables so builds work in unmodified environments. When cross-compiling you must give cgo a C cross-compiler, for example by setting the `CC` environment variable when running the go tool, or `CC_FOR_TARGET` / `CC_FOR_${GOOS}_${GOARCH}` when building the toolchain.

## Gotchas
- Memory from `C.CString` is allocated by C and must be freed by the caller, for example with `C.free(unsafe.Pointer(p))` (include `stdlib.h`).
- Zero out C memory in C before passing it to Go code that will store pointers in it: the docs note an implementation bug that can cause a runtime error if uninitialised C memory looks like a Go pointer.

## Checked
2026-11-09. Confirmed on pkg.go.dev/cmd/cgo: `#cgo` flag directives, pkg-config, cross-compiler note, `C.CString`/`C.free`, pointer passing rules, `runtime.Pinner`, `cgocheck` settings, `runtime/cgo.Handle`, `noescape` and the uninitialised-memory note.
Removed unconfirmed claims: per-call cost in nanoseconds, thread locking and thread exhaustion, `CGO_ENABLED` defaults and the `net`/`os/user` fallback, sanitizer and race detector requirements, and the `ldd` check. The go.dev/blog/cgo source was not read and was dropped.
Method: documentation only; no commands were run.

## Verify
Run the tests with the default `GODEBUG=cgocheck=1` and confirm no cgo pointer-check panics.
