---
id: computing-software.software-engineering.zig.zig-subcommands
name: zig-subcommands
category: computing-software
field: software-engineering
product: zig
tags: [zig, zig-subcommands, zig-cli-tooling, zig-run, build-exe, build-lib, zig-init, zig-env, zig-version]
level: intro
status: docs-checked
description: "Use the core Zig subcommands run, build-exe, build-lib, test, init, env and version with common flags for quick programs."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/src/main.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zig run, build-exe, build-lib, test and init
**Goal:** know the CLI surface.

```bash
zig version                         # print version number
zig env                             # prints zig_exe, lib_dir, std_dir, global_cache_dir, version, target, env
zig init                            # scaffold a build.zig project; -m / --minimal uses the minimal template
zig run main.zig -- arg1 arg2       # compile + run a single file; args after --
zig build-exe main.zig -O ReleaseFast -femit-bin=out/app
zig build-lib lib.zig -dynamic      # or -static
zig test main.zig --test-filter "name"
zig fmt src/                        # format files or dirs in place
zig ast-check main.zig              # look for simple compile errors
zig targets                         # list available compilation targets
zig libc                            # display native libc paths file or validate one
zig build --help                    # build-system flags
```
- Command list from `zig --help`: build, fetch, init, build-exe, build-lib, build-obj, test, run, ast-check, fmt, reduce, translate-c, ar, cc, c++, dlltool, lib, ranlib, objcopy, rc, env, help, std, libc, targets, version, zen.
- `-h, --help` prints command-specific usage; `zig <cmd> --help` is authoritative for your version.
- Single-file commands are good for scripts and examples; real projects use `zig build`.
- Per-module options: `-O Debug|ReleaseSafe|ReleaseFast|ReleaseSmall` (Debug is the default), `-target`, `-mcpu`, `-I[dir]`, `-l[lib]`, `-fstrip`. Output: `-femit-bin[=path]`. Link: `-static`, `-dynamic`.
- `zig cc` / `zig c++` are drop-in C and C++ compilers (see the zig-cc-compiler skill).

## Gotchas
- Building without `-O` is Debug: optimizations off, safety on.
- `zig env` and `zig targets` print Zig object notation (ZON) in 0.15.1, not JSON.

## Self-check
Run `zig env`, `zig run hello.zig`, and `zig targets`.

## Checked
2026-11-02. Confirmed against the 0.15.1 compiler source (`src/main.zig` usage text, `src/print_env.zig`, `src/print_targets.zig`) and the 0.15.1 language reference: command list, `zig init --minimal`, build-generic option names, `-O` modes and Debug default, `zig env` field names.
Removed or fixed: "dev builds look like 0.15.0-dev.NNN+hash" (unstated), "unconfirmed" init hedge (now confirmed), `zig targets` was described as JSON (it is ZON), `-lc`, `-fno-sanitize` style claims and the Go/Rust/Make `CC=` recipe (not in these pages), "zig run is not a script interpreter" cache claim.
Method: documentation only; no commands were run.
