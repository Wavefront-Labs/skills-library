---
id: computing-software.software-engineering.zig.build-zig-basics
name: build-zig-basics
category: computing-software
field: software-engineering
product: zig
tags: [zig, build-zig-basics, zig-build-system, std-build, addexecutable, installartifact, addrunartifact, b-step]
level: practitioner
status: docs-checked
description: "Write a Zig 0.15.1 build.zig with addExecutable and root_module, installArtifact, a run step and argument forwarding."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/init/build.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# build.zig anatomy: executables, run and install steps
**Goal:** a minimal, correct build script.

```zig
const std = @import("std");
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "app",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });
    b.installArtifact(exe);                           // zig build => zig-out/bin/app

    const run = b.addRunArtifact(exe);
    run.step.dependOn(b.getInstallStep());
    if (b.args) |args| run.addArgs(args);             // zig build run -- a b
    b.step("run", "Run the app").dependOn(&run.step);
}
```
- `zig build` runs the default (install) step; `zig build --help` lists every option and top-level step; `zig build run` runs the `run` step.
- The default install prefix is `zig-out/` (override with `--prefix` or `-p`).
- `b.path("rel")` yields a `LazyPath`.
- In 0.15.1 `addExecutable` and `addTest` take `.root_module` (a `*Module` from `b.createModule`); the options struct has no `root_source_file` field. Pin the Zig version, since build API changes between releases.

## Gotchas
- The build system is ordinary Zig code run at build time, so review third-party build scripts.
- Missing `b.installArtifact` means nothing lands in `zig-out`.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `addExecutable`/`addTest` option structs (`root_module`, no `root_source_file`), `createModule`, `path`, `installArtifact`, `addRunArtifact`, `getInstallStep`, `step`, `args` and the `zig-out/` prefix comment against Build.zig and lib/init/build.zig. Removed: `-h`, `--verbose`, `--summary` and cache-directory claims (compiler/runner source not read).

Method: documentation only; no commands were run.

## Self-check
`zig init`, then `zig build run` prints output, and `zig build --help` lists `-Doptimize` and `-Dtarget`.
