---
id: computing-software.software-engineering.nim.pragma-reference-inventory
name: pragma-reference-inventory
category: computing-software
field: software-engineering
product: nim
tags: [pragma-reference-inventory, effects-and-pragmas, pragma-reference, callconv, importc, exportc, threadvar, align, packed, bycopy, nim]
level: practitioner
status: docs-checked
description: "Know the pragma families (calling convention, FFI, memory, threading, codegen) and the declaration forms they attach to."
sources:
  - https://github.com/nim-lang/Nim/blob/devel/doc/manual.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pragma inventory and where each goes

Goal: find the right pragma quickly.

- Calling conventions: `nimcall` (default for a proc), `closure` (default for a procedural type; two machine words), `stdcall`, `cdecl`, `safecall`, `fastcall`, `thiscall`, `syscall`, `noconv`, `inline` (a hint; Nim leaves inlining to the C compiler) and `noinline`. Most conventions exist only for 32-bit Windows.
- FFI: `importc`, `exportc`, `exportcpp`, `header`, `nodecl`, `dynlib` (import and export), `importcpp`, `importjs`, `importobjc`, `varargs` (procedures only).
- Layout: `packed` and `union` (object types), `align(n)` (variables and object fields; n a constant power of 2), `bycopy` / `byref` (object or tuple types, or proc parameters), `size` on enums (only 1, 2, 4 or 8) or on `importc` incomplete object types.
- Memory and concurrency: `threadvar` (variables), `gcsafe`, `guard` (annotation for variables and object fields) with `locks`, `noalias` (maps to C `restrict`; unchecked and unsafe).
- Codegen: `emit` (unportable to other backends, highly discouraged), `codegenDecl`, `compile`, `passC`, `passL`, `localPassC`, `link`.
- Others in the same chapter: `deprecated`, `compileTime`, `noreturn`, `acyclic`, `final`, `pure`, `used`, `volatile`, `global`, `experimental`.

Gotchas:
- `align` has no effect on the JavaScript backend; `nodecl` does not work with the LLVM backend.
- `emit` code is backend-specific, so it is unportable across code generators.
- `compile` recompiles a file only when its SHA1 checksum changed; `-f` forces a rebuild.

Verify: `{.size: 1.}` on an enum gives `sizeof` 1.

## Checked

2026-11-08. Searched doc/manual.md from nim-lang/Nim by section (calling conventions list, size, align, noalias, nodecl, compile, link, passc, passl, emit, pragma section headings, bycopy/byref, varargs, union, packed, threadvar, guard/locks); the 290 KB manual was not read end to end. Removed: the "pragma placement shows allowed kinds in the error message" gotcha and the advice to check `nim --version` against a docs index (not in the manual); tut1 and lib.html dropped from sources.
Method: documentation only; no commands were run.
