---
id: computing-software.firmware-embedded-development.platformio.library-json-dependency-resolution
name: library-json-dependency-resolution
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [platformio, library-json, library-properties, lib-deps, dependency-resolution, lib-ldf-mode, lib-compat-mode, version-pinning, semver-range, private-lib, lib-extra-dirs, header-only-detection, semver-requirements, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Control PlatformIO dependency resolution: lib_deps version requirements, pinned git refs, lib_ldf_mode and lib_compat_mode behaviour, library.json dependencies, storage order."
sources:
  - https://docs.platformio.org/en/latest/librarymanager/ldf.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_deps.html
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_install.html
  - https://docs.platformio.org/en/latest/manifests/library-json/fields/dependencies.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# library.json and dependency resolution in PlatformIO

**Goal:** make dependency resolution deterministic and debuggable instead of "it builds,
usually". It complements the version-pinning guidance in
`computing-software.firmware-embedded-development.platformio.multi-environment-builds-and-ci`
with the mechanics of how PlatformIO decides what to include.

## Version specifiers in `lib_deps`
```ini
lib_deps =
  bblanchon/ArduinoJson @ ^6.21.0                 ; semver range
  bblanchon/ArduinoJson @ 6.21.3                  ; exact version
  https://github.com/org/lib.git#v2.1.0           ; git tag
  https://github.com/org/lib.git#a1b2c3d4e5f6     ; git commit
```
Documented requirement forms: `^1.2.3` (compatible, recommended by the docs), `~1.2.3` (same major
and minor), `>1.2.3` / `>=` / `<` / `<=`, comma-combined ranges such as `>0.1.0,!=0.2.0,<0.3.0`,
and an exact `1.2.3`. A range means a clean CI checkout weeks later can resolve a newer matching
release than a developer's cached copy; use an exact version, tag or commit for release builds.

## Library Dependency Finder (LDF) modes
The LDF scans `#include` directives to decide which libraries a build needs (`lib_ldf_mode`,
default `chain`):
- `chain`: parses all project sources and follows nested includes from the libraries (it also
  parses `.c`/`.cc`/`.cpp` files of libraries named like an included header). Does not evaluate
  C preprocessor conditionals.
- `chain+`: same, but evaluates `#ifdef`, `#if`, `defined`, `#else`, `#elif`.
- `deep` / `deep+`: parses all sources of each found dependency recursively (with or without
  conditional evaluation). Not generally recommended by the docs; use it when a dependency is
  referenced only from a library source file, not its header (or list it explicitly instead).
- `off`: does not process project sources or dependencies; builds only libraries given in
  manifests or `lib_deps`. Most reproducible, at the cost of maintaining the list by hand.
Once the LDF picks a library, all sources per its manifest are built.

## `lib_compat_mode` and manifests
A library with `library.json`, `library.properties` or `module.json` is checked against the build
environment. `soft` (default) checks the framework; `strict` checks framework and platform;
`off` does not check. `strict` catches a wrong-platform library at resolution time instead of at
a compile or link error.

## Dependencies declared by a library
In `library.json`, `dependencies` (object or array) are installed automatically. Each entry can
have `owner`, `name`, `version` (a requirement or specification such as a git URL) and optional
`frameworks` and `platforms` filters.

## Local libraries and storage order
The LDF searches in this priority order: the project `lib` directory, the project `libdeps`
directory (managed by the library manager), the global core `lib` directory, then libraries built
into frameworks and SDKs. `lib_extra_dirs` adds storage folders but is deprecated since 6.0; the
docs point to `symlink://` dependencies instead. When "my patch has no effect", check which copy
compiled with `pio run -v`.

## Verify
- [ ] Release and CI builds pin every `lib_deps` entry to an exact version, tag or commit.
- [ ] `lib_ldf_mode` is `chain` or stricter deliberately; `deep` or `off` only after a confirmed miss.
- [ ] A build with an ambiguous library source was checked with `pio run -v`.
- [ ] `library.json` compatibility fields are accurate for in-house libraries.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): LDF guide, `lib_deps`,
`pio pkg install` specifications and requirements, `library.json` dependencies, `lib_extra_dirs`.
Confirmed: requirement syntax, LDF modes and defaults, compat modes, storage priority,
`lib_extra_dirs` deprecation, dependencies fields. Removed as unconfirmed: "project-local wins" as
a general rule beyond the documented storage order, the claim that `deep` "meaningfully slows
every build", and the unqualified `lib_compat_mode` platform description (corrected).
Method: documentation only; no commands were run.
