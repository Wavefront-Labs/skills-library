---
id: computing-software.software-engineering.zig.target-triples
name: target-triples
category: computing-software
field: software-engineering
product: zig
tags: [zig, target-triples, zig-cross-compile, target-triple, mcpu, musl, glibc-version, cross-compile]
level: practitioner
status: docs-checked
description: "Cross-compile with Zig using -target arch-os-abi triples, -mcpu features, and glibc versioned targets without extra toolchains."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Target/Query.zig
  - https://github.com/ziglang/zig/blob/0.15.1/src/main.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Target triples, CPU features and ABIs
**Goal:** build for another platform from your machine.

```bash
zig build -Dtarget=x86_64-linux-musl                    # static Linux binary
zig build -Dtarget=aarch64-macos -Doptimize=ReleaseSafe
zig build -Dtarget=x86_64-linux-gnu.2.31 -Dcpu=baseline # glibc 2.31 version suffix on the ABI
zig build-exe main.zig -target thumb-freestanding-eabihf -mcpu=cortex_m4
zig build -Dcpu=native                                  # tune for this machine
zig targets                                             # list the targets the compiler knows
```
- Command-line form is `-target <arch><sub>-<os>-<abi>`; the ABI part may carry a glibc version (`Target.Query` parses `glibc_version`).
- With no target option the compiler targets the host, and the executable is unsuitable for copying to a different computer. A target is CPU architecture, CPU features, OS, OS version range, ABI and ABI version.
- `-mcpu` sets the CPU and feature set. In a build script, `b.standardTargetOptions` provides `-Dtarget` and `-Dcpu`, and `b.resolveTargetQuery(.{ .cpu_arch = .x86_64, .os_tag = .linux, .abi = .musl })` builds a fixed target (a release matrix loops over queries).
- `zig build` accepts `-fqemu`, `-fwine` and `-fwasmtime` (and `--sysroot`) so run steps can execute foreign binaries.
- Each tagged release's notes carry the support table per target.

## Gotchas
- Test on the real target: stdlib support differs per target.

## Self-check
Cross-build hello for `x86_64-windows` and `aarch64-linux-musl` and check the `file` output of each.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (Targets section), `lib/std/Build.zig` (`standardTargetOptions`, `resolveTargetQuery`), `lib/compiler/build_runner.zig` (`-fqemu`, `-fwine`, `-fwasmtime`, `--sysroot`) and `src/main.zig` (`-target`, `-mcpu`).
Removed: which libc sources Zig bundles (musl, mingw-w64, glibc stubs, macOS SDK stubs), "musl yields fully static / gnu dynamically links", "-Dcpu=baseline is portable" wording, the macOS SDK gotcha.
Method: documentation only; no commands were run.
