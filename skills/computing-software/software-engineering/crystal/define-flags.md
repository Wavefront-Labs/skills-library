---
id: computing-software.software-engineering.crystal.define-flags
name: define-flags
category: computing-software
field: software-engineering
product: crystal
tags: [define-flags, compile-time-flags, flags, -d, define-flag, feature-flag, compile-time-flag, conditional-compilation, crystal]
level: practitioner
status: docs-checked
description: "Toggle Crystal code at build time with -D flags, flag? queries, and user-provided flag values."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/compile_time_flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining flags with -D

Goal: toggle code at build time.

- User flags are not defined automatically; pass them with `--define` or `-D`: `crystal eval -Dfoo 'p {{ flag?(:foo) }}'` prints `true`.
- A flag can carry a string value: `-Dfoo=bar` makes `flag?(:foo)` return `"bar"` (a string literal instead of a bool).
- Query in code with the macro method `flag?(:name)` (symbol or string), e.g. `{% if flag?(:myflag) %} ... {% end %}`. `host_flag?` queries the host platform, which differs from the target when cross-compiling.
- Custom flags are for feature gates, previews, legacy behaviour or debugging. Do not collide with compiler flags or other user flags; for a shard-specific flag use the shard name as a prefix.
- Some stdlib and language flags are also user-provided: `gc_none` (disable garbage collection), `debug_raise`, `no_number_autocast`, `preview_overload_order`, `strict_multi_assign`, `preview_mt` (documented as the legacy multithreading runtime, deprecated since 1.21).

Verify: build with and without the flag and observe the different output.

## Checked
Checked 2026-11-02 against the crystal-book Compile-time flags page. Real error fixed: the skill said flags with values are not supported; `-Dfoo=bar` is documented. Removed: `crystal spec -D` / `crystal run -D` forms, unused-branch type-check, compiler-cache and shard.yml remarks, `env()` workaround.

Method: documentation only; no commands were run.
