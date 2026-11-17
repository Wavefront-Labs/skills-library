---
id: computing-software.software-engineering.zig.build-steps-modules
name: build-steps-modules
category: computing-software
field: software-engineering
product: zig
tags: [zig, build-steps-modules, zig-build-system, addmodule, addimport, addlibrary, addsystemcommand, addwritefiles]
level: advanced
status: docs-checked
description: "Define Zig modules with b.addModule, link libraries, create custom steps, run system commands and generate files in build.zig."
sources:
  - https://ziglang.org/learn/build-system/
  - https://ziglang.org/documentation/master/std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom steps, modules, libraries and dependencies
**Goal:** structure multi-target builds.

```zig
const lib = b.addLibrary(.{
    .name = "mylib",
    .linkage = .static,
    .root_module = b.createModule(.{ .root_source_file = b.path("src/lib.zig"), .target = target, .optimize = optimize }),
});
b.installArtifact(lib);
exe.root_module.linkLibrary(lib);                         // link it into an executable

// build a tool for the host, run it, feed its output file in as an import
const tool = b.addExecutable(.{ .name = "gen", .root_module = b.createModule(.{ .root_source_file = b.path("tools/gen.zig"), .target = b.graph.host }) });
const run_tool = b.addRunArtifact(tool);
const out = run_tool.addOutputFileArg("table.zig");
exe.root_module.addAnonymousImport("table", .{ .root_source_file = out });

const docs = b.step("docs", "Build docs");
docs.dependOn(&install_docs.step);
```
- Steps form a DAG: `a.dependOn(&b.step)`.
- Build-time code generator pattern: build a Zig tool with `b.addExecutable`, run it with `b.addRunArtifact`, feed output via `addOutputFileArg` into an import.
- `b.addSystemCommand(&.{ "jq" })` runs an external program; `captureStdOut` and `addInstallFileWithDir` handle its output.
- `b.addTest(.{...})` produces a test executable (see testing skills).

## Gotchas
- The build script cannot hardcode output paths (this breaks caching and concurrency); pass generated files around as the values returned by `addOutputFileArg`.

## Self-check
Generate a Zig file with a build-time tool, import it, and confirm `zig build --summary all` reruns the generator only when its inputs change.

## Checked

2026-11-02. Checked against the Zig build system guide at ziglang.org/learn/build-system (addLibrary with .linkage and .root_module, createModule, addExecutable with root_module, linkLibrary, addRunArtifact, addOutputFileArg, addAnonymousImport, addSystemCommand, captureStdOut, addInstallFileWithDir, addTest, b.step and dependOn, no hardcoded output paths). Fixed: addStaticLibrary with root_source_file in its options is the pre-root_module form; replaced with the addLibrary form shown in the guide, and the build-time command example now follows the guide's tool pattern. Removed: addModule/addImport, addWriteFiles, addInstallDirectory, installBinFile, b.dependency and getEmittedBin (not in the guide).

Method: documentation only; no commands were run.
