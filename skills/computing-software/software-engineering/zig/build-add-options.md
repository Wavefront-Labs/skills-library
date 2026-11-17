---
id: computing-software.software-engineering.zig.build-add-options
name: build-add-options
category: computing-software
field: software-engineering
product: zig
tags: [zig, build-add-options, zig-build-options, addoptions, build-options-module, comptime-config, version-string]
level: practitioner
status: docs-checked
description: "Pass build-time configuration into Zig code via b.addOptions and @import of the generated options module."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Step/Options.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Module.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compile-time configuration with addOptions
**Goal:** bake values (version, flags, git hash) into the binary at compile time.

```zig
// build.zig
const opts = b.addOptions();
opts.addOption([]const u8, "version", "1.4.2");
opts.addOption(bool, "enable_tracing", b.option(bool, "trace", "Enable tracing") orelse false);
exe.root_module.addOptions("config", opts);

// src/main.zig
const config = @import("config");
pub fn main() void {
    if (config.enable_tracing) trace();
    std.debug.print("v{s}\n", .{config.version});
}
```
- The options module is generated source, so the values are comptime-known.
- Git hash: `b.run(&.{ "git", "rev-parse", "--short", "HEAD" })` returns the output as `[]u8` (a build.zig helper, not for step `make()`), then pass it via `addOption`.
- `Step.Options.addOption(comptime T, name, value)` renders `T` as Zig source; the 0.15.1 type printer handles pointers/slices, optionals and enums among others (see Options.zig).
- In 0.15.1 the hook is `Module.addOptions(module_name, options)`, called on `exe.root_module`.

## Gotchas
- `b.run` executes while the build script runs, so keep it fast.
- Options are attached per module with `Module.addOptions`; a test with a different root module needs its own call (`tests.root_module.addOptions`).

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `b.addOptions`, `Step.Options.addOption(T, name, value)`, `Module.addOptions(module_name, options)`, `Build.run` and `addSystemCommand`, `b.option(bool, ...)`. Removed: the supported-type list, the cached-step advice and the dead-branch and older-release claims.

Method: documentation only; no commands were run.

## Self-check
Print the baked version and flip the trace flag with `-Dtrace=true`, confirming a different binary behaviour.
