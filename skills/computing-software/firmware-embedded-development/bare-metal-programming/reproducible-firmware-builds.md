---
id: computing-software.firmware-embedded-development.bare-metal-programming.reproducible-firmware-builds
name: reproducible-firmware-builds
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [reproducible-build, arm-none-eabi-gcc, build-determinism, file-prefix-map, toolchain-pinning, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make firmware builds bit-for-bit reproducible: pinned toolchain in a container, path prefix maps, no timestamps, sorted inputs, and a CI job that compares two builds."
sources:
  - https://reproducible-builds.org/docs/
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Overall-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/cpp/Environment-Variables.html
  - https://reproducible-builds.org/docs/source-date-epoch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible firmware builds

Same source + same toolchain = identical binary. It proves the shipped image came from the
tagged commit, makes signing reviews meaningful, and lets you rebuild an old release years later
to debug it.

## Sources of non-determinism and fixes
| Source | Fix |
|---|---|
| `__DATE__`, `__TIME__`, `__TIMESTAMP__` | remove; use the git hash. If you must keep `__DATE__`/`__TIME__`, GCC replaces the current date and time in them with the value of the `SOURCE_DATE_EPOCH` environment variable (a UNIX timestamp, set by the build process) |
| Absolute paths in `__FILE__`, debug info, asserts | `-ffile-prefix-map=old=new`: records references to files in directory `old` as if they were in `new`; equivalent to specifying all the individual `-f*-prefix-map` options (`-fdebug-prefix-map`, `-fmacro-prefix-map`, ...) |
| Toolchain version drift | pin the exact toolchain release in a container image or a checksum-verified download |
| Link order from unsorted globs | a glob can list files in a different order on another machine; list sources explicitly or sort them |
| Archive timestamps/UIDs | use the deterministic mode of your archiver and check the flag in its manual |
| Build-dir dependent names | build in the same container path, or use the prefix map above |
| Generated files (version.h) containing build host/user | strip; derive only from git |

`SOURCE_DATE_EPOCH` is the standard variable from reproducible-builds.org: the time of the last
modification of the source, in seconds since the Unix epoch, for build tools to use instead of
the current time.

## Container
Pin the base image by digest and the toolchain by version and checksum, and record both in the
release notes. A package-manager tag does not pin package versions.

## CI check
Build the same commit in two different directories (and on two machines), compare the resulting
`.bin` files byte for byte, and use a diff tool for binaries when they differ. Two directories
catch path leaks.

## Verify
- [ ] Two builds in different directories produce identical `.bin` hashes.
- [ ] The image contains no absolute build-machine paths (the prefix map works).
- [ ] Release notes record the toolchain image digest.

## Checked
2026-10-31. Confirmed in the GCC 14.2 manual: `-ffile-prefix-map` semantics (Overall Options) and
`SOURCE_DATE_EPOCH` replacing the date and time in `__DATE__`/`__TIME__` (preprocessor environment
variables). Confirmed on reproducible-builds.org: `SOURCE_DATE_EPOCH` definition.
Removed: the Dockerfile, toolchain version and download URL, `ar D` and CMake archive command, `file(GLOB)` and
`list(SORT)` claims, `-frandom-seed`, `diffoscope`, the "GCC honours it for `__TIMESTAMP__`" implication.
Method: documentation only; no commands were run.
