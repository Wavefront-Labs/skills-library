---
id: computing-software.software-engineering.d.d-version-debug-conditional-compilation
name: d-version-debug-conditional-compilation
category: computing-software
field: software-engineering
product: d
tags: [d-version-debug-conditional-compilation, pragmas, version, debug, static-if, conditional-compilation, -version, d_betterc, predefined-versions, d]
level: practitioner
status: docs-checked
description: "Compile code conditionally with version(), debug(), static if, predefined versions (linux, Windows, D_BetterC, unittest, assert) and -version/-debug switches."
sources:
  - https://dlang.org/spec/version.html
  - https://dlang.org/dmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# version, debug and static if conditional compilation

Goal: platform and build-specific code without a preprocessor.

- `version (linux) {...} else version (Windows) {...} else static assert(0, "unsupported");`
- Predefined: `Windows`, `linux`, `OSX`, `Posix`, `X86_64`, `LittleEndian`, `DigitalMars`, `LDC`, `GNU`, `D_BetterC`, `D_InlineAsm_X86_64`, `unittest`, `assert`, `D_Coverage`.
- Custom: `version (Foo)` set by `-version=Foo` (dub `versions "Foo"`). `version` identifiers cannot be assigned inside code, only at module level with `version = Foo;`.
- `debug { }` is active with `-debug`; `debug(ident)` is active when the identifier matches (`-debug=ident`).
- `static if (cond)` tests compile-time expressions, usable in templates and aggregates; does not introduce a scope.
- `version (none)` always false, `version (all)` true.

Gotchas:
- Both branches must parse even when disabled, so syntax errors inside them still fail.
- `version` cannot be negated with `!`; use an `else` branch or `version (D_X) {} else {...}`.

Verify: `dmd -version=Foo -c m.d` toggles the branch; add `pragma(msg, "foo on");` inside.

## Checked

Date 2026-11-02. Confirmed version and debug conditions, predefined version identifiers, version=X at module scope, and static if (Conditional Compilation spec). Removed debug(1) level syntax, which the spec does not document.

Method: documentation only; no commands were run.
