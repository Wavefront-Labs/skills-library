---
id: computing-software.software-engineering.zig.static-release-builds
name: static-release-builds
category: computing-software
field: software-engineering
product: zig
tags: [zig, static-release-builds, zig-cross-compile, releasesmall, strip, static-binary, lto, release-matrix]
level: practitioner
status: docs-checked
description: "Produce small static release binaries in Zig with ReleaseSmall or ReleaseFast, musl, strip, LTO and a CI matrix over targets."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Module.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release builds, static linking and strip
**Goal:** ship portable binaries.

```zig
const targets = [_]std.Target.Query{
    .{ .cpu_arch = .x86_64, .os_tag = .linux, .abi = .musl },
    .{ .cpu_arch = .aarch64, .os_tag = .linux, .abi = .musl },
    .{ .cpu_arch = .x86_64, .os_tag = .windows },
    .{ .cpu_arch = .aarch64, .os_tag = .macos },
};
for (targets) |q| {
    const t = b.resolveTargetQuery(q);
    const exe = b.addExecutable(.{
        .name = "app",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = t,
            .optimize = .ReleaseSafe,
            .strip = true,
        }),
    });
    const install = b.addInstallArtifact(exe, .{
        .dest_dir = .{ .override = .{ .custom = try t.result.zigTriple(b.allocator) } },
    });
    b.getInstallStep().dependOn(&install.step);
}
```
- In 0.15.1 `addExecutable` takes `name` and `root_module`; target, optimize and `strip` live on the module (`b.createModule`), not on `addExecutable`.
- Optimize modes (CLI help): Debug (default, optimizations off, safety on), ReleaseFast (performance, safety off), ReleaseSafe (performance, safety on), ReleaseSmall (small binary, safety off).
- CLI equivalents: `-fstrip` / `-fno-strip`, `-flto` / `-fno-lto` (LTO "requires LLVM extensions"), `-static`.
- `Step.Compile` has a `want_lto: ?bool` field.
- `Target.zigTriple(allocator)` returns an error union, hence the `try`.

## Self-check
Run the matrix and check each `zig-out/<triple>/` holds a file for that platform.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/Build.zig` (`ExecutableOptions` has `root_module`, no `root_source_file`, `target`, `optimize` or `strip`; `createModule`; `resolveTargetQuery`; `addInstallArtifact`), `lib/std/Build/Module.zig` (`strip`), `lib/std/Build/Step/Compile.zig` (`want_lto`) and `src/main.zig` help text.
Fixed: the old snippet passed `.root_source_file`, `.target`, `.optimize` and `.strip` straight to `addExecutable`, which 0.15.1 does not accept. Removed: "musl gives static" generalisation, "ReleaseSafe is a good default for services", CI packaging/signing advice, the Windows `.exe` naming claim, "keep unstripped copies" advice.
Method: documentation only; no commands were run.
