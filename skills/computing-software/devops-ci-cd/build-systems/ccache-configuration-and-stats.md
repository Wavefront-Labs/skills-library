---
id: computing-software.devops-ci-cd.build-systems.ccache-configuration-and-stats
name: ccache-configuration-and-stats
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, ccache-config, ccache, compiler-caches]
level: practitioner
status: docs-checked
description: "Configure ccache for high hit rates in CI and dev: base_dir and path normalisation, max_size, compiler_check, sloppiness, and reading ccache -s stats to diagnose misses."
sources: ["https://ccache.dev/manual/latest.html", "https://github.com/ccache/ccache/blob/master/doc/manual.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ccache configuration and stats

## Wire it in
- CMake: `-DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache`.
- Make/autotools: `CC="ccache gcc" CXX="ccache g++"`, or put ccache symlinks first in PATH.

## Key settings (ccache.conf or env)
```ini
# $CCACHE_DIR/ccache.conf
max_size = 5G                      # default 5 GiB
base_dir = <workspace-root>        # rewrite absolute paths below this to relative: hits across checkouts
hash_dir = false                   # do not hash the current directory (matters with -g)
compiler_check = content           # hash compiler binary content; default is mtime and size
sloppiness = pch_defines,time_macros,include_file_mtime,include_file_ctime
compression = true                 # default is true
```
Env equivalents: `CCACHE_BASEDIR`, `CCACHE_MAXSIZE`, `CCACHE_DIR`, `CCACHE_COMPILERCHECK`, `CCACHE_NOHASHDIR`.

## Stats
```bash
ccache -z          # zero stats before build
make -j"$(nproc)"
ccache -s -v       # --show-stats --verbose: hits, misses, uncacheable reasons
```
| Symptom | Likely cause |
|---|---|
| Near-zero hits across CI runs | absolute paths differ per run: set `base_dir` |
| Misses after the compiler is reinstalled | default `compiler_check = mtime` sees a new mtime: use `content` |
| `__DATE__`/`__TIME__` uncacheable | `sloppiness = time_macros` or remove the macros |
| Precompiled-header misses | `sloppiness = pch_defines,time_macros` (see the manual's precompiled header section) |
| Cache evictions | raise `max_size` |

Debug a single miss: set `CCACHE_DEBUG=1`; ccache writes `<objectfile>.<timestamp>.ccache-input-text` files next to the object. Compare the files of two compilations that should have matched.

## Verify
- [ ] A second clean build in a fresh checkout reports hits for (almost) every compilation in `ccache -s`.

## Checked
Date: 2026-10-25. Documentation: ccache `doc/manual.adoc` on the default branch (ccache/ccache).
Confirmed: `max_size` default 5 GiB; `base_dir`/`CCACHE_BASEDIR` path rewriting; `hash_dir` and `CCACHE_NOHASHDIR`; `compiler_check` values (`mtime` default, `content`, `none`, `string:`); `compression` default true; sloppiness names `pch_defines`, `time_macros`, `include_file_mtime`, `include_file_ctime`; `-s`/`-v` options; `CCACHE_DEBUG` and the `.ccache-input-text` file name.
Removed: the unqualified ">90% hits" target and the "could not use precompiled header" counter name.
Method: documentation only; no commands were run.
