---
id: computing-software.software-engineering.d.d-invariants-and-assert-modes
name: d-invariants-and-assert-modes
category: computing-software
field: software-engineering
product: d
tags: [d-invariants-and-assert-modes, contracts, invariant, release-mode, boundscheck, checkaction, check-switch, assert-modes, d]
level: advanced
status: docs-checked
description: "Add invariant() blocks, understand when they run, and set -release, -check=assert/in/out/invariant, -boundscheck and -checkaction=halt/context to tune checks."
sources:
  - https://dlang.org/spec/class.html
  - https://dlang.org/spec/expression.html
  - https://dlang.org/dmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class and struct invariants, assert modes and -check/-release switches

Goal: pick checking levels per build.

- `invariant()` in a class runs at the exit of the constructor, the entry of the destructor, and the entry and exit of each public or exported non-static member function; public member functions cannot be called from inside a struct invariant.
- Switches: `-release` does not emit contract and assert checks and does bounds checking only in `@safe` functions; `-boundscheck=on|safeonly|off`.
- Fine control: `-check=in=on|off`, `-check=out=...`, `-check=invariant=...`, `-check=assert=...` (each `on|off|safeonly`; `-check=help` lists them).
- `-checkaction=D|C|halt|context`: `context` prints the error context as part of the `AssertError`; `halt` executes a halt instruction; `D` (default) throws `AssertError`; `C` calls the C runtime assert failure function.
- `assert(0)` marks unreachable code (it suppresses a missing-return error); the compiler may still generate a halt instruction for it when other asserts are ignored.
- dub build types: `debug` (contracts on), `release` (off), `release-nobounds`.

Gotchas:
- `-release` changes program behaviour if asserts hold side effects.
- Test with the same flags you ship, plus the checked ones.

Verify: build twice (`-debug`, `-release`) and trigger a violation; only the first should fail.

## Checked

Date 2026-11-02. Confirmed invariant timing (Class spec), assert semantics (Expressions spec) and -release/-check/-checkaction/-boundscheck (DMD switches). Corrected invariant timing and the -release and checkaction descriptions.

Method: documentation only; no commands were run.
