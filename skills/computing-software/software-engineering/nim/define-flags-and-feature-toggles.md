---
id: computing-software.software-engineering.nim.define-flags-and-feature-toggles
name: define-flags-and-feature-toggles
category: computing-software
field: software-engineering
product: nim
tags: [define-flags-and-feature-toggles, configuration-files, define, d-flag, intdefine, strdefine, booldefine, feature-flag, build-config, defined, nim]
level: practitioner
status: docs-checked
description: "Set compile-time defines with -d/--define and -u/--undef, read them with defined() and the intdefine, strdefine and booldefine pragmas, and know the documented compiler defines."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/manual.html
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compile-time defines and feature toggles

Goal: configure behaviour at compile time.

- Set: `-d:foo` / `--define:foo`, optionally with a value (`-d:FooBar=42`); `-d:flag` is a shortcut for `-d:flag=true`. Undefine with `-u:foo` / `--undef:foo`. Define names are case insensitive and ignore underscores, so `--define:FOO` and `--define:foo` are identical.
- Read: `when defined(foo):`. Typed reads use the compile-time define pragmas: `const FooBar {.intdefine.}: int = 5`, `{.strdefine.}` (string) and `{.booldefine.}` (bool); the command-line value overrides the default, and `defined(FooBar)` tells whether a value was provided. A qualified name is possible: `{.intdefine: "package.FooBar".}` is set with `-d:package.FooBar=42`.
- Documented defines include `release` (optimizer on), `danger` (no runtime checks, optimizer on), `useMalloc` (with `--mm:none`, `arc` or `orc`), `ssl`, `useRealtimeGC`, `noSignalHandler`, `lto`, `strip`, `useNimRtl`. Symbols starting with `nim` are reserved for the implementation.
- The default build is a debug build; `nim c -d:release` and `nim c -d:danger` select the other two.
- `nimble build -d:release` forwards compiler flags (Nimble guide: flags given to `nimble build` are forwarded to the compiler); persistent flags go in config files.

Gotchas:
- Don't reuse the reserved `nim` prefix for your own defines; prefix your own with the app name.
- Changing defines changes the generated program; rebuild (`-f` / `--forceBuild`) if in doubt.

Verify: build with and without `-d:verbose` changes the output.

## Checked

2026-11-03. Confirmed in the compiler guide (define/undef options, case insensitivity, switch table, reserved `nim` prefix, release/danger) and the manual ("compile-time define pragmas", including the qualified name and `-d:flag` = `true`). Removed: `static: echo level` inspection tip, `nimStrictMode`, `nimv2`, `gcOrc`/`gcArc` (not in the pages), "nimble backend/switch defaults" and the flags-hashing remark.
Method: documentation only; no commands were run.
