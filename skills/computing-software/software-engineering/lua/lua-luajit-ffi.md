---
id: computing-software.software-engineering.lua.lua-luajit-ffi
name: lua-luajit-ffi
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-luajit, luajit-ffi]
level: advanced
status: docs-checked
description: "Call C from LuaJIT with ffi.cdef and write code that the tracing JIT compiles."
sources:
  - https://luajit.org/ext_ffi.html
  - https://luajit.org/ext_ffi_api.html
  - https://luajit.org/ext_jit.html
  - https://luajit.org/running.html
  - https://luajit.org/extensions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LuaJIT FFI and JIT-friendly code
- `local ffi = require("ffi"); ffi.cdef[[ int printf(const char *fmt, ...); ]]; ffi.C.printf("Hello %s!", "world")`. `ffi.C` is the default C library namespace; `ffi.load("z")` loads `libz.so` on POSIX or a `.dll` on Windows and returns another namespace.
- `ffi.new("int[?]", n)` makes a variable-length array (zero-filled by default); `ffi.string(ptr, len)` copies bytes into a Lua string (passing `len` is faster and allows embedded zeros); `ffi.cast`; `ffi.gc(ptr, finalizer)`, e.g. `ffi.gc(ffi.C.malloc(n), ffi.C.free)`, and `ffi.gc(p, nil)` removes the finalizer.
- `ffi.cdef` takes plain C declarations but no pre-processor: no `#define`, only `#pragma pack`. Replace macros with `enum`, `static const` or `typedef`, or run headers through an external pre-processor once.
- To create many objects of one kind, get the ctype once with `ffi.typeof()` and call it as a constructor. Each anonymous struct in `ffi.new` is a new distinct type and can cause excessive JIT traces; use a named struct or typedef.
- C arrays are zero-based. FFI arrays of structs use far less memory than tables of small tables (the manual's example drops from 22 MB to 640 KB).
- Diagnose with `luajit -jv script.lua` (verbose JIT progress), `-jdump` (compiler stages) and `-jp` (integrated profiler). `jit.off()` / `jit.off(true, true)` in a module main chunk disables compilation for debugging; `jit.flush()` clears compiled code.
- LuaJIT is fully upwards-compatible with Lua 5.1 and adds some Lua 5.2 extensions, including `goto` and `::labels::`.
Verify: `luajit -jv script.lua` shows traces compiled.

## Checked
2026-11-08. Confirmed in luajit.org FFI introduction, ffi.* API page, jit.* library, Running LuaJIT and Extensions pages (read in full). Removed: unverified claims that wrong prototypes crash, the list of not-yet-implemented functions (`pairs`, `string.format`, `os.*`), and that LuaJIT receives only maintenance updates.
Method: documentation only; no commands were run.
