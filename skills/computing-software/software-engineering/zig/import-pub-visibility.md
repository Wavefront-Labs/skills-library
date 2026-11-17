---
id: computing-software.software-engineering.zig.import-pub-visibility
name: import-pub-visibility
category: computing-software
field: software-engineering
product: zig
tags: [zig, import-pub-visibility, zig-modules, import, pub, file-as-struct, root-source-file]
level: intro
status: docs-checked
description: "Organise Zig code into files with @import, pub visibility, and the fact that each file is a struct namespace."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref.html.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @import, pub and files as structs
**Goal:** structure a codebase across files.

```zig
// math.zig
pub fn add(a: i32, b: i32) i32 { return a + b; }
fn helper() void {}                  // private to the file
pub const Config = struct { debug: bool = false };

// main.zig
const std = @import("std");          // std lib module
const math = @import("math.zig");    // relative file path
const Config = math.Config;
const x = math.add(1, 2);
```
- `@import` of a Zig source file returns that file's struct type, as if the call were replaced by `struct { FILE_CONTENTS }`; a `.zon` file import returns the ZON literal's value. The path must end in `.zig` or `.zon`.
- A file with top-level fields is named like a struct (`TitleCase.zig`) by the style guide.
- Import by path relative to the importing file or by a module name registered in build.zig (the name refers to that module's root source file). Always available: `@import("std")`, `@import("builtin")`, `@import("root")`.
- `pub` marks a declaration for use by importers.
- `@embedFile("data.txt")` returns a comptime-known null-terminated array of the file's bytes; the path is absolute or relative to the current file, like `@import`.
- A file's `test` blocks only run if it is referenced from the test root: add `test { _ = @import("other.zig"); }` or `std.testing.refAllDecls(@This())`.

## Gotchas
- Container level declarations are lazily analyzed, so an unused declaration may never be checked.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the `@import`, `@embedFile` and Container Level Variables (lazy analysis) text and the Style Guide on file names in the language reference. Removed: circular/dedup claims, the quoted 'outside module path' error and the claim that `pub` is the only modifier.

Method: documentation only; no commands were run.

## Self-check
Split a program into two files, leave a helper without `pub`, and confirm importing it from the other file fails.
