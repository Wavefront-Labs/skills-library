---
id: computing-software.software-engineering.zig.build-test-step
name: build-test-step
category: computing-software
field: software-engineering
product: zig
tags: [zig, build-test-step, zig-testing, addtest, test-step, test-filter, integration-tests, refalldecls]
level: practitioner
status: docs-checked
description: "Wire Zig tests into build.zig with b.addTest and a test step, add per-module tests, filters, and structure unit versus integration tests."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/testing.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test steps, filters and test organisation
**Goal:** one `zig build test` that covers everything.

```zig
const unit = b.addTest(.{ .root_module = b.createModule(.{ .root_source_file = b.path("src/main.zig"), .target = target, .optimize = optimize }) });
const run_unit = b.addRunArtifact(unit);
const test_step = b.step("test", "Run unit tests");
test_step.dependOn(&run_unit.step);

const itest = b.addTest(.{
    .root_module = b.createModule(.{ .root_source_file = b.path("tests/integration.zig"), .target = target, .optimize = optimize }),
    .filters = &.{"parser"},                  // optional: only tests whose name contains "parser"
});
itest.root_module.addImport("mylib", lib_mod);
test_step.dependOn(&b.addRunArtifact(itest).step);
```
```bash
zig build test
zig test src/main.zig --test-filter parser   # direct form, no build.zig
```
- `TestOptions` (0.15.1) has `name`, `root_module`, `filters: []const []const u8` and `use_llvm`.
- `std.testing.fuzz` exists in testing.zig (it forwards to the root file's `fuzz`).
- Use `std.testing.tmpDir(.{})` for filesystem tests and `defer tmp.cleanup()`.
- Each test executable tests one root module, so test the library and executable modules with separate `addTest` calls.

## Gotchas
- Tests in files not referenced from the root module never run; reference them (`_ = @import("x.zig");` or `std.testing.refAllDecls(@This())`).
- Global state shared across tests makes order matter; reset it.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `addTest` and `TestOptions` (`root_module`, `filters`), `b.step`, `addRunArtifact`, `testing.fuzz`, `testing.tmpDir`/`cleanup`, `--test-filter` (language reference). Removed: `--summary`, `-Dtest-filter`, `--fuzz` and `-fqemu` claims and the 'test per bug' advice.

Method: documentation only; no commands were run.

## Self-check
Add a failing test, see `zig build test` fail with a non-zero exit, then fix it and rerun.
