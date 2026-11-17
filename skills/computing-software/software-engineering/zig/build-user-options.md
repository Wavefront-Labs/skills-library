---
id: computing-software.software-engineering.zig.build-user-options
name: build-user-options
category: computing-software
field: software-engineering
product: zig
tags: [zig, build-user-options, zig-build-options, b-option, standardoptimizeoption, standardtargetoptions, dflag]
level: practitioner
status: docs-checked
description: "Add -D command-line options to build.zig with b.option, standardOptimizeOption and standardTargetOptions, and list them with zig build -h."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/init/build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# -D options with b.option and standard options
**Goal:** make builds configurable from the CLI.

```zig
const strip = b.option(bool, "strip", "Strip debug info") orelse false;
const name = b.option([]const u8, "name", "Binary name") orelse "app";
const level = b.option(u8, "level", "Level 0-3") orelse 1;
const backend = b.option(enum { sdl, glfw }, "backend", "Window backend") orelse .sdl;
const target = b.standardTargetOptions(.{});          // -Dtarget=x86_64-linux-musl -Dcpu=...
const optimize = b.standardOptimizeOption(.{});       // -Doptimize=Debug|ReleaseSafe|ReleaseFast|ReleaseSmall (OptimizeMode enum)
```
```bash
zig build -Dstrip=true -Dname=tool -Dbackend=glfw -Dtarget=aarch64-linux-musl -Doptimize=ReleaseSafe
zig build --help      # lists every option (including target and optimize) and top-level step
```
- With `standardOptimizeOption(.{ .preferred_optimize_mode = .ReleaseSafe })` there is no `-Doptimize`: the option becomes `-Drelease` (bool), which selects the preferred mode, and the default is Debug.
- Without a preferred mode, `-Doptimize=<mode>` is read; if absent the result follows `--release=` (off gives Debug; `--release=any` prints an error asking you to choose fast, safe or small).
- `standardTargetOptions(.{ .whitelist = &.{...} })` restricts targets (a slice of `Target.Query`); `.default_target` sets the default.
- To build several targets from one invocation, call `b.resolveTargetQuery(.{ .cpu_arch = .aarch64, .os_tag = .linux })` in `build.zig`.

## Gotchas
- Boolean options accept `-Dflag` (true), `-Dflag=true` and `-Dflag=false`; other values are an error.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `b.option` (bool parsing), `standardOptimizeOption` logic (`preferred_optimize_mode`, `-Drelease`, `-Doptimize`, `--release=`), `StandardTargetOptionsArgs` (`whitelist`, `default_target`), `resolveTargetQuery`, `-Dtarget`/`-Dcpu` option names. Fixed: `whitelisted_targets` is `whitelist`; `-Doptimize` does not exist when a preferred mode is set. Removed: unknown-flag and help-listing claims, `-Dname` self-check.

Method: documentation only; no commands were run.

## Self-check
Run `zig build --help` and see your option descriptions; pass `-Dstrip=true` and read the value in `build.zig`.
