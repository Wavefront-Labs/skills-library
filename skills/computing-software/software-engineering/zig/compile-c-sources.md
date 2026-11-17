---
id: computing-software.software-engineering.zig.compile-c-sources
name: compile-c-sources
category: computing-software
field: software-engineering
product: zig
tags: [zig, compile-c-sources, zig-build-c, addcsourcefile, linksystemlibrary, linklibc, addincludepath, c-flags]
level: advanced
status: docs-checked
description: "Compile C and C++ files and link libc, libc++ and system libraries from build.zig using addCSourceFile, addIncludePath and linkSystemLibrary."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Step/Compile.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Module.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiling C sources and linking system libraries
**Goal:** mix C into a Zig project.

```zig
exe.addCSourceFile(.{ .file = b.path("vendor/sqlite3.c"), .flags = &.{ "-std=c99", "-DSQLITE_THREADSAFE=0" } });
exe.addIncludePath(b.path("vendor"));
exe.root_module.link_libc = true;      // exe.linkLibC() is deprecated in 0.15.1
exe.linkSystemLibrary("z");            // needs the library and headers installed
exe.root_module.link_libcpp = true;    // exe.linkLibCpp() is deprecated in 0.15.1
exe.addCSourceFiles(.{ .root = b.path("src"), .files = &.{ "a.c", "b.c" }, .flags = &.{"-Wall"} });
```
- `Step.Compile` has `addCSourceFile` (`file: LazyPath`, `flags`, optional `language`), `addCSourceFiles` (`root`, `files`, `flags`, optional `language`), `addIncludePath`, `linkSystemLibrary`, `linkSystemLibrary2`, `linkLibrary` and `addLibraryPath`.
- `linkLibC` and `linkLibCpp` carry the doc comment "Deprecated; use `compile.root_module.link_libc = true`" (and `link_libcpp`).
- A static library built with `b.addLibrary(.{ .linkage = .static, .name = ..., .root_module = ... })` is linked into an executable with `exe.linkLibrary(lib)`; `addStaticLibrary` and `addSharedLibrary` do not exist in 0.15.1.
- Compiling C files needs the Clang backend ("requires LLVM extensions" in the CLI file-type table). C undefined-behavior detection is controlled by `-fsanitize-c[=trap|full]` / `-fno-sanitize-c`.
- Linker options on the CLI: `-l[lib]`, `-L[dir]`, `-I[dir]`, `--sysroot [path]`, `-cflags [flags] --`.

## Self-check
Compile a one-file C library and call it from Zig, then cross-compile with `-Dtarget=x86_64-windows-gnu`.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/Build/Step/Compile.zig`, `lib/std/Build/Module.zig` (`AddCSourceFilesOptions`, `CSourceFile`), `lib/std/Build.zig` (`LibraryOptions` with `linkage`; no `addStaticLibrary`/`addSharedLibrary`) and `src/main.zig` help text.
Fixed: `b.addStaticLibrary` (removed in 0.15.1) replaced by `addLibrary`; `linkLibC` shown as deprecated. Removed: "unconfirmed" hedges, pkg-config behaviour of `linkSystemLibrary`, bundled-headers list, "Zig as C build system" pattern, `illegal instruction` and `libc not linked` error-text claims.
Method: documentation only; no commands were run.
