---
id: computing-software.software-engineering.zig.translate-c-cimport
name: translate-c-cimport
category: computing-software
field: software-engineering
product: zig
tags: [zig, translate-c-cimport, zig-build-c, cimport, cinclude, translate-c, c-bindings, zig-translate-c]
level: advanced
status: docs-checked
description: "Call C from Zig with @cImport and @cInclude, inspect output with zig translate-c, and know which C constructs do not translate."
sources:
  - https://ziglang.org/documentation/0.15.1/#Import-from-C-Header-File
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Step/TranslateC.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @cImport, translate-c and bindings
**Goal:** use a C API from Zig safely.

```zig
const c = @cImport({
    @cDefine("_GNU_SOURCE", {});
    @cInclude("stdio.h");
});
pub fn main() void {
    _ = c.puts("hi");
}
```
```bash
zig translate-c -target x86_64-linux-gnu header.h > header.zig   # prints the translation to stdout
```
- `@cImport(expression)` parses C code and imports functions, types, variables and compatible macros into a new empty struct type. The builtins `@cInclude`, `@cDefine` and `@cUndef` work only inside its expression.
- The reference recommends usually one `@cImport` in the whole application (clang is invoked once and inline functions are not duplicated); reasons for several are avoiding symbol collisions and using different preprocessor defines.
- `zig translate-c` takes a single file, forwards optional flags to clang and writes to stdout. Flags: `-I`, `-D`, `-cflags [flags] --`, `-target`. The current directory is not on the include path (use `-I.`).
- Use the same `-target` and `-cflags` for translation as for compiling the translated code; otherwise parse failures or ABI mismatches can result.
- `@cImport` and `translate-c` share the same translation; use `translate-c` when you need cflags or want to edit the output (for example `[*c]T` to `[*]T`).
- Not everything translates: `goto`, structs with bitfields and token-pasting macros are demoted to `opaque`, `extern` or `@compileError`. Function-like macros are translated best effort.
- Translation is cached; `--verbose-cimport` shows the cache location of `cimport.h`, `cimport.h.d` and `cimport.zig`.
- The build system has `b.addTranslateC(.{ .root_source_file, .target, .optimize })` with `createModule()` and `addModule(name)`.

## Self-check
Call `strlen` via `@cImport` on a literal and compare to the Zig length.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (Import from C Header File, C Translation CLI, C Translation Caching, Translation failures, C Macros) and `lib/std/Build/Step/TranslateC.zig`.
Removed: sqlite example and `SQLITE_OK` usage, `[*:0]const u8`/`std.mem.span` advice, "multiple @cImport blocks produce incompatible types" (the reference only lists collisions and different defines), char signedness claim, "newer releases replace @cImport" hedge.
Method: documentation only; no commands were run.
