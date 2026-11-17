---
id: computing-software.software-engineering.zig.build-cache-watch
name: build-cache-watch
category: computing-software
field: software-engineering
product: zig
tags: [zig, build-cache-watch, zig-build-system, zig-cache, build-summary, watch-mode, incremental-compilation, jobs]
level: practitioner
status: docs-checked
description: "Speed up and inspect Zig builds with the build cache, -j, --summary, --watch and incremental compilation, and clean artifacts."
sources:
  - https://ziglang.org/learn/build-system/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build cache, parallelism, summary and watch mode
**Goal:** fast iteration and visibility.

```bash
zig build --summary all          # show each step, cache hit/miss, timings
zig build -j8                    # limit concurrent jobs (default: all CPU cores)
zig build --watch                # continuously rebuild when source files change
zig build -fincremental --watch  # enable incremental compilation (-fno-incremental disables)
zig build --verbose              # print compiler invocations
zig build --verbose-link
zig build --cache-dir /tmp/zc    # override the local cache directory
zig build -p /opt/app            # install prefix instead of zig-out
zig build --prefix-lib-dir ...   # also --prefix-exe-dir; see -h
```
- Project cache: `.zig-cache/` holds files that make later builds faster; it is not for source control and can be deleted at any time with no consequences. `zig-out/` is the installation prefix chosen by the user with `--prefix` / `-p`.
- Add `.zig-cache/` and `zig-out/` to `.gitignore`.
- Other options: `--debug-log [scope]` for compiler debugging, `--seed [integer]` to shuffle dependency traversal order (default random), `-freference-trace[=num]` for reference-trace length per compile error, and `--summary [mode]` with all, new (omits cached steps), failures, line or none.

## Gotchas
- Running `zig build` from a subdirectory finds the nearest parent `build.zig`.

## Self-check
Run `zig build --summary new` twice and show the second run lists no steps (cached steps are omitted).

## Checked

2026-11-02. Checked against the Zig build system guide at ziglang.org/learn/build-system and its embedded `zig build --help` output (--summary modes, -j<N>, --watch, -fincremental, --cache-dir, -p/--prefix and --prefix-lib-dir, --seed, --debug-log, --verbose-link, -freference-trace, .zig-cache and zig-out roles). Removed: the zig-cache rename note, the no-zig-clean and global-cache advice, the cache-key description, --global-cache-dir and --debug-compile-errors (not in the help text), and the addFileInput gotcha (none stated in the guide).

Method: documentation only; no commands were run.
