---
id: computing-software.devops-ci-cd.bazel.bazel-toolchain-resolution-and-debugging
name: bazel-toolchain-resolution-and-debugging
category: computing-software
field: devops-ci-cd
product: bazel
tags: [toolchain-resolution, register-toolchains, extra-toolchains, toolchain-type, execution-platform, toolchain-resolution-debug, platforms-flag]
level: advanced
status: docs-checked
description: "Register toolchains, understand how Bazel matches them to target and execution platforms, and debug a wrong pick."
sources: ["https://bazel.build/extending/toolchains"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel toolchain resolution

Rules depend on a toolchain type (`toolchain_type(name = "toolchain_type")`), not on a tool. Concrete `toolchain(...)` targets declare `toolchain_type`, `exec_compatible_with`, `target_compatible_with` and the `toolchain` implementation. Bazel resolves the type to one toolchain based on the target platform (`--platforms`) and available execution platforms.

Register in `MODULE.bazel` with `register_toolchains("//bar_tools:all")` or on the command line with `--extra_toolchains` and `--extra_execution_platforms`. Target patterns register subpackages first, then names in lexicographic order.

Priority of available toolchains: `--extra_toolchains` first (the last one wins within it), then the root module's registrations, then the user WORKSPACE, then non-root modules (first mentioned wins). The host platform is always an available execution platform.

Resolution: a constraint list matches a platform if the platform has every listed `constraint_value`; extra constraints on the platform do not matter. Execution platforms are filtered by the target's `exec_compatible_with`; toolchains with non-matching `target_settings` are dropped; for each execution platform the first compatible toolchain per type is chosen; platforms missing a mandatory toolchain are ruled out and the first remaining platform runs all actions of the target. Execution groups resolve separately.

Debug:
```bash
bazel build //my:all --toolchain_resolution_debug='//my:target'
bazel build //my:all --toolchain_resolution_debug='.*'
bazel cquery 'deps(//cc:my_cc_lib, 1)'
```
The debug flag prints each toolchain checked and skipped. Some rules do not support toolchain resolution yet.

Verify: the selected toolchain appears as a dependency in the cquery output.

## Checked

2026-11-04. Read against the Bazel docs page(s): Toolchains (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: nothing further.
Method: documentation only; no commands were run.
