---
id: computing-software.software-engineering.zig.zig-fmt
name: zig-fmt
category: computing-software
field: software-engineering
product: zig
tags: [zig, zig-fmt, zig-fmt-style, fmt-check, formatter, ci-format]
level: intro
status: docs-checked
description: "Format Zig code with zig fmt, check formatting in CI with --check, format from stdin and know what the formatter will and will not change."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/src/fmt.zig
  - https://ziglang.org/documentation/0.15.1/#Style-Guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zig fmt usage and CI checks
**Goal:** one canonical format, enforced.

```bash
zig fmt src/ build.zig             # rewrite in place (files or dirs, searched recursively)
zig fmt --check src/ build.zig     # list non-conforming files; exit with an error if the list is non-empty (CI)
zig fmt --stdin < in.zig > out.zig # format stdin to stdout (editor integration)
zig fmt --ast-check file.zig       # run zig ast-check on every file
zig fmt --exclude vendor/ src/     # exclude a file or directory
zig fmt --zon file.txt             # treat input as ZON regardless of extension
```
- Options in 0.15.1: `-h/--help`, `--color [auto|off|on]`, `--stdin`, `--check`, `--ast-check`, `--exclude [file]`, `--zon`.
- The style guide specifies 4 space indentation; the language reference says running `zig fmt` implements all style-guide recommendations about formatting.
- Naming conventions are in the style guide, not enforced by the formatter.
- Pin the compiler version in CI: formatter output can change between releases.

## Self-check
Add misaligned code, run `zig fmt --check` (fails), `zig fmt` (fixed), `--check` (passes).

## Checked
2026-11-02. Confirmed in 0.15.1 `src/fmt.zig` usage text and the language reference Style Guide ("4 space indentation", "running zig fmt ... will implement all recommendations").
Removed: "no options" (there are several), trailing-comma wrapping rules, comment-placement rules, "tabs are rejected/converted", "ZLS invokes zig fmt on save", examples of formatter version drift.
Method: documentation only; no commands were run.
