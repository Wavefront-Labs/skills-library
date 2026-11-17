---
id: computing-software.software-engineering.zig.export-c-library
name: export-c-library
category: computing-software
field: software-engineering
product: zig
tags: [zig, export-c-library, zig-interop, export-fn, extern-struct, c-header, shared-library, emit-h]
level: advanced
status: docs-checked
description: "Build a Zig static or shared library with a C ABI, export functions and extern structs, generate a header and call it from C."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/src/main.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting a C ABI library from Zig
**Goal:** ship Zig code to C or other languages.

```zig
// lib.zig
const Point = extern struct { x: f64, y: f64 };
export fn point_len(p: *const Point) f64 { return @sqrt(p.x * p.x + p.y * p.y); }
export fn buf_fill(ptr: [*]u8, len: usize, v: u8) void { @memset(ptr[0..len], v); }
```
```bash
zig build-lib lib.zig -dynamic -femit-h      # shared library plus a C header (-femit-h[=path])
zig build-lib lib.zig -static
```
- `-femit-h[=path]` generates a C header file; `-fno-emit-h` is the default. `-dynamic` and `-static` force the link mode.
- Use `callconv(.c)` for function pointers passed to C (0.15.1 spelling, as in the language reference examples).
- Convert errors to status codes at the boundary rather than exporting error unions.
- In `build.zig`, build the library with `b.addLibrary(.{ .linkage = .dynamic, .name = "lib", .root_module = ..., .version = .{ .major = 1, .minor = 0, .patch = 0 } })` and `b.installArtifact(lib)`; `LibraryOptions` has `linkage` (default `.static`) and `version`. `addSharedLibrary` is not in 0.15.1.

## Self-check
Build the shared lib and call `point_len` from a short C program linked against it.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (`export`, `callconv(.c)` examples) and `src/main.zig` help text (`-femit-h`, `-dynamic`, `-static`), `lib/std/Build.zig` (`LibraryOptions`, `installArtifact`).
Fixed: `addSharedLibrary` removed in 0.15.1 (use `addLibrary` with `.linkage = .dynamic`); the `-femit-h` hedge is now confirmed. Removed: extern-compatible type list, `c_allocator` ownership advice, "panics abort the host process", bool ABI claim, `callconv(.C)` spelling.
Method: documentation only; no commands were run.
