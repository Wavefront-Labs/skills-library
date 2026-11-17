---
id: computing-software.firmware-embedded-development.platformio.test-filtering-and-hierarchy
name: test-filtering-and-hierarchy
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-test, pio-test-filter, test-filter, test-ignore, test-build-src, native-tests, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Organise PlatformIO tests into a hierarchy (native vs embedded, per module), select them with -f/-i and test_filter/test_ignore, and share helper files between tests."
sources:
  - https://docs.platformio.org/en/latest/advanced/unit-testing/structure/hierarchy.html
  - https://docs.platformio.org/en/latest/core/userguide/cmd_test.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/test/test_filter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test filtering and hierarchy

## Hierarchy
PlatformIO looks for tests in the project `test_dir`. A folder whose name starts with `test_`
is a test suite: an independent test application with its own `main()` (`setup()`/`loop()`
for Arduino, `app_main()` for ESP-IDF). Nested folders are allowed for grouping:
```
test/
├── native/
│   ├── test_ringbuf/test_main.c
│   └── test_protocol/test_main.cpp
├── embedded/
│   ├── unity_config.cpp          # shared by the suites below
│   ├── test_i2c_sensor/test_main.cpp
│   └── test_flash/test_main.cpp
```
A suite is identified by its path relative to `test_dir`, e.g. `native/test_ringbuf`. A single
test application may sit directly in `test_dir`.

## Selecting
Patterns match the suite path relative to `test_dir`. Pattern syntax: `*` matches everything,
`?` any one character, `[seq]` any character in seq, `[!seq]` any not in seq.

Command line (`-f/--filter`, `-i/--ignore`, both repeatable):
```bash
pio test -e native -f "native/*"                 # only native suites
pio test -e nucleo_l476rg -f "embedded/*" -i "embedded/test_flash"
pio test -e native -f "*/test_protocol" -v       # one suite, show raw framework output
```
Per environment in `platformio.ini`, so the wrong suites never run on the wrong target:
```ini
[env:native]
platform = native
test_filter = native/*

[env:nucleo_l476rg]
platform = ststm32
board = nucleo_l476rg
test_ignore = native/*
```
`test_filter` accepts several patterns (one per line), and `pio test --filter` overrides the
`test_filter` option.

## Sharing code between suites
- The root `test_dir` and the active test's folder are added to the C preprocessor search
  path, and C/C++ files in the root of `test_dir` are compiled together with the active test.
  Put shared configuration and helper files there (the docs use `unity_config.h/.cpp` in a
  shared folder for a group of embedded suites).
- A suite can include its local headers by relative path, e.g. `#include <include/cheese.h>`.

## Running parts of the pipeline
```bash
pio test -e nucleo_l476rg --without-uploading     # skip the uploading stage
pio test -e nucleo_l476rg --without-building      # skip the building stage
pio test --junit-output-path reports/             # JUnit XML report (parent folder must exist)
pio test --list-tests                             # list suites without running them
```
`--test-port` and `--upload-port` select the serial ports; both are auto-detected when omitted.

## Embedded test entry
If the board has no software reset via DTR/RTS, add more than 2 seconds of delay before
`UNITY_BEGIN()` so the serial link with the host is up.

## Verify
- [ ] `pio test -e native` runs only native suites.
- [ ] Each env's `test_filter`/`test_ignore` prevents cross-target suites from building.

## Checked
2026-10-31. Confirmed on the PlatformIO Test Hierarchy, `pio test` and `test_filter` pages:
suite naming and nesting, filter/ignore semantics and pattern syntax, CLI override of
`test_filter`, root `test_dir` handling, the stage-skipping and report options, `--test-port`,
and the 2 second reset delay. Removed: the claim that CLI `-f` narrows `test_filter` (the page
says it overrides it), `test_build_src`, `build_src_filter` and `-I test/common` advice,
and LDF auto-linking of `lib/` modules.
Method: documentation only; no commands were run.
