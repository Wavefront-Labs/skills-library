---
id: computing-software.software-engineering.nim.nimscript-limits-and-hooks
name: nimscript-limits-and-hooks
category: computing-software
field: software-engineering
product: nim
tags: [nimscript-limits-and-hooks, nimscript, nimscript-limits, vm, hooks, before-install, after-build, nimble-hooks, staticexec, nim]
level: advanced
status: docs-checked
description: "NimScript limits for config.nims and .nimble files: no FFI, unsupported features, exec and gorgeEx, before/after hooks, and --maxLoopIterationsVM."
sources:
  - https://nim-lang.org/docs/nimscript.html
  - https://nim-lang.org/docs/nims.html
  - https://nim-lang.org/docs/nimc.html
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NimScript limits and hooks

Goal: know what config scripts can do.

- NimScript runs in the compiler's VM: no FFI, so modules relying on `importc` are unavailable. The docs also list known limits: bugs with `ptr`/`var T` returns, more than one level of `ref` unsupported, no multimethods, and `random.randomize()` needs an explicit int64 seed. The page lists the stdlib modules that are available (httpclient is not among them).
- `exec` runs a shell command and raises `OSError` on failure; `gorgeEx` (system) returns the output and exit code.
- In a .nimble file, `before <cmd>:` and `after <cmd>:` hooks run around Nimble commands and user tasks; returning `false` stops further execution.
- The VM loop limit is raised with the compiler option `--maxLoopIterationsVM:N`.

Gotchas:
- Code that works in normal Nim may fail in the VM for the reasons above.

Verify: `nim e script.nims` runs the script.

## Checked

2026-11-03. Confirmed in the NimScript and nims pages, compiler guide and Nimble guide. Removed: socket/thread claims, a specific list of hook names, "non-zero quit fails a hook", and the example loop value 10000000.
Method: documentation only; no commands were run.
