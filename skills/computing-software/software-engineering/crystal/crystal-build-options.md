---
id: computing-software.software-engineering.crystal.crystal-build-options
name: crystal-build-options
category: computing-software
field: software-engineering
product: crystal
tags: [crystal-build-options, cli-build-run, crystal-build, -o, --release, --debug, --stats, --progress, --error-trace, --no-debug, link-flags, opt-level, crystal]
level: practitioner
status: docs-checked
description: "Use crystal build flags: -o output, --release, -O levels, --debug and --no-debug, --stats, --progress, --time, --threads, --no-codegen, --link-flags and warning options."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
  - https://github.com/crystal-lang/shards/blob/master/docs/shards.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal build options

Goal: control builds.

- `crystal build [<options>] <programfile>`: the binary is named after the source file minus `.cr`, in the current directory. `-o <path>` / `--output <path>` sets the output; if it is a directory, the name is derived from the first source file.
- `--release` is equivalent to `-O3 --single-module`. `-O LEVEL` takes `0` (default), `1`, `2`, `3`, `s` or `z`. A release build compiles slower but is meant for production and benchmarks.
- `-d` / `--debug` adds full symbolic debug info; `--no-debug` skips it, reducing file size.
- `-s` / `--stats` prints statistics; `-p` / `--progress` shows progress; `-t` / `--time` prints execution time; `--error-trace` shows the full error trace.
- `--threads NUM` sets the maximum number of threads for code generation; `--single-module` generates one LLVM module; `--no-codegen` skips code generation (type-checking only).
- `--link-flags FLAGS` passes extra flags to the linker; `-D FLAG` defines a compile-time flag; `--static` links statically; `--verbose` displays executed commands.
- Warnings: `--warnings all|none` (default all), `--error-on-warnings`, `--exclude-warnings <path>` (default `lib`).

Gotchas:
- Compiling without `--release` is much faster and the binaries still perform reasonably well.
- `shards build` delegates its options after the command to `crystal build` and writes to `bin`.

Verify: `crystal build --stats app.cr` prints stage statistics.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`crystal build`, Optimizations sections) and the command source (every option above, `-O` values, warning options, output-path rule) and shards(1) (`build` delegates to `crystal build`).
Removed: the default of 8 for `--threads` (it depends on the platform and version), "`--debug` is the default", "release builds disable the incremental cache", "`--no-codegen` takes a fraction of the time" and the `-O0..-O3`/`-Os` spelling without `z`.
Method: documentation only; no commands were run.
