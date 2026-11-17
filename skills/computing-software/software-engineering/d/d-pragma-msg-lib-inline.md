---
id: computing-software.software-engineering.d.d-pragma-msg-lib-inline
name: d-pragma-msg-lib-inline
category: computing-software
field: software-engineering
product: d
tags: [d-pragma-msg-lib-inline, pragmas, pragma-msg, pragma-lib, pragma-inline, pragma, compile-time-print, d]
level: practitioner
status: docs-checked
description: "Use pragma(msg) for compile-time diagnostics, pragma(lib) to link libraries, and pragma(inline, true/false) to force or forbid inlining."
sources:
  - https://dlang.org/spec/pragma.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pragma(msg), pragma(lib), pragma(inline)

Goal: use the standard pragmas.

- `pragma(msg, "text", expr);` prints at compile time; the arguments are concatenated (`pragma(msg, "compiling...", 6, 1.0)` prints `compiling...61.0`).
- `pragma(lib, "curl");` takes one compile-time string literal naming a library file, which is inserted into the object file or passed to the linker (implementation defined; an implementation may ignore it). dub `libs` is the recipe-level equivalent.
- `pragma(inline, true)` always inlines (an error message is typical if the function cannot be inlined), `pragma(inline, false)` never inlines, bare `pragma(inline)` restores the implementation default; at declaration level it affects the block it controls, inside a function it affects that function. With several in one function the lexically last wins.
- `pragma(startaddress, fn)` sets the program start address (specialized systems work; the runtime handles it for applications).

Gotchas:
- All implementations must support these pragmas but may ignore them.

Verify: compile and check the `pragma(msg)` text appears in the compiler output.

## Checked

Date 2026-11-02. Confirmed pragma msg, lib, inline and startaddress semantics (Pragmas spec). Corrected msg argument concatenation and lib as implementation defined. Removed unknown-pragma, recursive inlining and quoting claims.

Method: documentation only; no commands were run.
