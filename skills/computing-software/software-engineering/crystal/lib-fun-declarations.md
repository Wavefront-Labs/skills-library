---
id: computing-software.software-engineering.crystal.lib-fun-declarations
name: lib-fun-declarations
category: computing-software
field: software-engineering
product: crystal
tags: [lib-fun-declarations, c-bindings, lib, fun, ffi, c-function, libc, lib-declaration, external-function, crystal]
level: practitioner
status: docs-checked
description: "Declare C functions, valid C types, renamed and variadic funs, global variables and out parameters in a Crystal lib block, and call them."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/fun.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/lib.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/out.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/to_unsafe.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lib and fun declarations

Goal: call a C function.

```crystal
lib C
  # In C: double cos(double x)
  fun cos(value : Float64) : Float64
  fun getch : Int32
  fun srand(seed : UInt32)
end

C.cos(1.5)
C.getch
C.srand(1_u32)
```
- Parentheses may be omitted when there are no parameters (in the call too); a void return type may be omitted.
- Valid types: primitive numbers, pointers (`Int32*`), static arrays (`Int32[8]`), function types (`Int32 -> Int32`), previously declared `struct`, `union`, `enum`, `type` or `alias`, `Void`, `NoReturn`, and Crystal structs marked `@[Extern]`.
- The C `char` is `UInt8`, so `char*` is `UInt8*`; Crystal's `Char` is a four-byte codepoint. The `LibC` lib defines aliases such as `LibC::SizeT` and `LibC::Char`.
- Rename: `fun init = SDL_Init(flags : UInt32) : Int32` binds C `SDL_Init` as `LibSDL.init`; a quoted C name is allowed (`fun ceil_f32 = "llvm.ceil.f32"(value : Float32) : Float32`). Variadic: `fun variadic(value : Int32, ...) : Int32`.
- Types implementing `to_unsafe` convert automatically when passed to C; `String#to_unsafe` returns `UInt8*`, so `C.printf "%d\n", 1` works with `fun printf(format : UInt8*, ...) : Int32`.
- Conversions: `Nil` matches any pointer or proc type, any pointer matches `Void*`, number literals autocast, and primitive numbers convert unsafely via `#to_*!` methods.
- Out params: for a pointer parameter, `C.waitpid(pid, out status_ptr, options)` declares `status_ptr` automatically; the long form is `uninitialized Int32` plus `pointerof(status_ptr)`.
- Global variables: `$errno : Int32` inside `lib` is read and set as `C.errno`; `@[ThreadLocal]` marks one thread local.

Gotchas:
- Function names in a `lib` may start with an upper-case letter.
- Prefer the existing `LibC` names over redeclaring.

Verify: print the result of a harmless call.

## Checked

2026-11-03. Confirmed against the Crystal book C bindings pages (fun, lib, out, to_unsafe, variables, struct).
Removed: `getpid`/`strlen`/`write` prototypes and the `Void` return means nil claim, "Crystal does not check C signatures; a wrong prototype crashes", the `ptr.null?` check and `String.new(ptr)` examples (not in these pages). Changed the `cos` example to the book's.
Method: documentation only; no commands were run.
