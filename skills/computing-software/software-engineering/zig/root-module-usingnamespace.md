---
id: computing-software.software-engineering.zig.root-module-usingnamespace
name: root-module-usingnamespace
category: computing-software
field: software-engineering
product: zig
tags: [zig, root-module-usingnamespace, zig-modules, usingnamespace, root-source-file, std-options, root-decls]
level: advanced
status: docs-checked
description: "Understand the Zig root source file, root-level declarations the std reads (main, panic, std_options), and usingnamespace deprecation."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/std.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/start.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/debug.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# root module, usingnamespace and std_options
**Goal:** know what lives at the root and which features are fading.

- The root source file (the root module's `root_source_file` in build.zig) is where `std/start.zig` looks for `main` (via `@hasDecl(root, "main")`), and where std reads `pub const std_options` (std.zig: `if (@hasDecl(root, "std_options")) root.std_options else .{}`).
- `@import("root")` accesses the root file from any module; library code can query hooks: `if (@hasDecl(root, "my_hook"))`.
- In 0.15.1 the panic handler is customised with `std.debug.FullPanic(fn ([]const u8, ?usize) noreturn)` (see debug.zig); `std.debug.defaultPanic` is the default.
- The 0.15.1 language reference does not document `usingnamespace`. Use explicit re-exports: `pub const foo = other.foo;` or `pub const Impl = switch (builtin.os.tag) { .windows => @import("win.zig"), else => @import("posix.zig") };`.
- `const builtin = @import("builtin");` gives `builtin.os.tag` and `builtin.mode` (both used in the language reference) and `builtin.is_test`.

## Gotchas
- Conditional compilation is just comptime `if`/`switch` on `builtin`; both branches must parse but only the taken one is analysed.
- `std_options` is read from the root file only (`@hasDecl(root, "std_options")`).

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `std_options` lookup in std.zig, `main` lookup in start.zig, `FullPanic`/`defaultPanic` in debug.zig, `builtin.os.tag`/`mode`/`is_test` in the language reference; `usingnamespace` is absent from the 0.15.1 language reference. Removed: `pub const os`, `zig_version` and version-shim claims, the 'slated for removal' history.

Method: documentation only; no commands were run.

## Self-check
Print `builtin.os.tag` and `builtin.mode` in a test and check they match your host and optimize mode.
