---
id: computing-software.software-engineering.nim.importc-header-exportc
name: importc-header-exportc
category: computing-software
field: software-engineering
product: nim
tags: [importc-header-exportc, ffi-c-interop, importc, exportc, header, cdecl, ffi, c-interop, nodecl, nim]
level: advanced
status: docs-checked
description: "Call C functions and use C types with importc and header, export Nim procs with exportc, and map names and calling conventions."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# importc, header and exportc

Goal: bridge Nim and C.

```nim
proc c_sqrt(x: cdouble): cdouble {.importc: "sqrt", header: "<math.h>".}
proc add(a, b: cint): cint {.exportc: "my_add", cdecl.} = a + b
```
- `importc` imports a proc or variable from C. The optional string is the C identifier; without it the C name is the Nim identifier exactly as spelled. On a `let` it may omit the value, to import a C `const` (`let cconst {.importc, nodecl.}: cint`).
- `header` is very similar to `nodecl`: the symbol is not declared and the generated code contains an `#include`. The argument is a string constant; a system header is written in angle brackets (`"<stdio.h>"`), otherwise Nim encloses the header name in `""`. It does not work with the LLVM backend.
- `exportc` exports a type, variable or procedure to C, with an optional C name; enums and constants cannot be exported. To export from a dynamic library, add `dynlib` (see the manual's dynlib pragma for export).
- A format string is allowed: `{.importc: "prefix$1".}` gives the external name `prefixp` for `p`; only `$1` exists and a literal dollar sign is `$$`. `exportc` and `extern` accept the same form.
- `varargs` allows a variable number of parameters after the last specified one, and Nim string values are converted to C strings automatically: `proc printf(formatstr: cstring) {.header: "<stdio.h>", varargs.}`.
- For C structs, `bycopy` passes an object or tuple type by value and `byref` by reference (hidden pointer); `byref` on a parameter wins over `bycopy` on the type. The compiler otherwise chooses by the type's size.
- `importcpp`, `importobjc` and `importjs` are the pragmas for other target languages.
- `union` and `packed` pragmas on an object type produce a C union or back-to-back fields; avoid ref/GC'ed memory in both.

Verify: calling c_sqrt(9.0) returns 3.0.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): Header pragma, Foreign function interface through Dynlib pragma for import (Importc, Exportc, Exportcpp, Extern, Bycopy, Byref, Varargs, Union, Packed). Removed because not in the pages read: the `std/ctypes` and C type alias list, the `nodecl` use for macros, the `{.size: sizeof(cint).}` enum rule, the NUL-termination advice for `cstring(s)`, `allocCStringArray` and the `int` versus `cint` width remark. `cdecl` appears only in examples; its semantics were not read. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
