---
id: computing-software.software-engineering.crystal.flag-macro-platform
name: flag-macro-platform
category: computing-software
field: software-engineering
product: crystal
tags: [flag-macro-platform, compile-time-flags, flag-macro, platform, linux, darwin, win32, x86-64, aarch64, musl, gnu, predefined-flags, crystal]
level: practitioner
status: docs-checked
description: "Write portable Crystal with flag?(:linux), :darwin, :unix, :windows, :x86_64 and the other compiler-provided flags."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/compile_time_flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform flags: flag?(:linux), :darwin, :win32, :x86_64

Goal: write portable code.

Target flags derive from the target triple (`crystal --version` shows the default target; `--target` changes it). Within each group they are mutually exclusive except those marked derived.
- Architecture: `aarch64`, `avr`, `arm`, `i386`, `wasm32`, `x86_64`; derived `bits32`, `bits64`.
- OS: `darwin`, `dragonfly`, `freebsd`, `linux`, `netbsd`, `openbsd`, `solaris`, `windows`; derived `bsd` (DragonFlyBSD, FreeBSD, NetBSD, OpenBSD) and `unix` (BSD, Darwin, Linux, Solaris).
- ABI: `android`, `gnu`, `gnueabihf`, `msvc`, `musl`, `wasi`; derived `armhf`, `win32` (Windows API).
- Compiler options: `release` (`--release` or `-O3 --single-module`), `debug` (unless `--no-debug`), `static` (`--static`), `docs`, `interpreted`.
```crystal
{% if flag?(:unix) %}
  puts "UNIX-like"
{% elsif flag?(:windows) %}
  puts "Windows"
{% end %}
```

Gotchas:
- During cross-compilation `flag?` describes the target; use `host_flag?` for the host.
- Use the derived `unix` flag instead of enumerating Unixes.
- Currently all supported targets are UNIX or Windows.

Verify: print `{{ flag?(:linux) }}` in a macro on each OS.

## Checked
Checked 2026-11-02 against the crystal-book Compile-time flags page. Removed: `crystal build --verbose` as a way to see the triple (only `crystal --version` is documented), `--cross-compile`, and `preview_mt` as a platform flag.

Method: documentation only; no commands were run.
