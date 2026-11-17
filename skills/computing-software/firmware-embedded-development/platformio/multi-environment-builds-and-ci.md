---
id: computing-software.firmware-embedded-development.platformio.multi-environment-builds-and-ci
name: multi-environment-builds-and-ci
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [platformio, pio, platformio-ini, env, extends, build-flags, build-src-filter, lib-deps, dependency-pinning, platform-version, pio-run, pio-test, unity, unit-testing, native-env, on-target-testing, github-actions, ci, actions-cache, firmware-build, arduino, esp32, stm32, pio-github-actions, default-envs, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build one firmware for several boards with platformio.ini environments, extends and pinned lib_deps, run Unity tests natively and on target, and cache PlatformIO in CI."
sources:
  - https://docs.platformio.org/en/latest/projectconf/index.html
  - https://docs.platformio.org/en/latest/advanced/unit-testing/index.html
  - https://docs.platformio.org/en/latest/integration/ci/github-actions.html
  - https://docs.github.com/en/actions
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# PlatformIO multi-environment builds and CI — reproducible firmware for every board

**Goal:** one repository that builds identical firmware for several boards and build
variants, tests logic on the host in seconds, and produces the same binaries in CI next
month as today.

## 1. Structure platformio.ini with a shared base
```ini
[platformio]
default_envs = esp32dev, nucleo_f401re

[env]                              ; inherited by every env
framework = arduino
monitor_speed = 115200
build_flags = -Wall -Wextra -DFW_VERSION=\"1.4.0\"
lib_deps =
    bblanchon/ArduinoJson @ 7.2.0      ; exact version, not ^7
test_framework = unity

[env:esp32dev]
platform = espressif32 @ 6.9.0      ; pin the platform too
board = esp32dev
build_flags = ${env.build_flags} -DBOARD_ESP32

[env:esp32dev_debug]
extends = env:esp32dev
build_type = debug
build_flags = ${env:esp32dev.build_flags} -DLOG_LEVEL=4

[env:nucleo_f401re]
platform = ststm32 @ 17.6.0
board = nucleo_f401re

[env:native]
platform = native
framework =                        ; no Arduino on the host
build_src_filter = +<*> -<main.cpp>
```
The version numbers above are illustrative; pin whatever you have tested.

Gotchas:
- A key set in `[env:x]` **replaces** the inherited value. To append, interpolate:
  `build_flags = ${env.build_flags} -DFOO`.
- `extends = env:a` copies another environment; it is the clean way to make debug/release
  or feature variants.
- Unpinned `platform = espressif32` floats to the latest release and can change the
  framework/toolchain under you. Pin `platform` and every `lib_deps` entry (`@ 1.2.3`
  exact; `^1.2.3` allows minor updates).
- String macros need escaped quotes: `-DNAME=\"value\"`.

## 2. Everyday commands
```bash
pio run                       # build default_envs
pio run -e esp32dev -t upload # build + flash one env
pio device monitor -e esp32dev
pio run -t clean -e native
pio pkg outdated              # see which pinned packages have newer versions
```

## 3. Unit tests with Unity: native first, target second
Layout: `test/test_parser/test_main.cpp`, one folder per suite.
```cpp
#include <unity.h>
#include "parser.h"
void setUp(void) {} void tearDown(void) {}
void test_checksum(void) { TEST_ASSERT_EQUAL_HEX8(0x5A, checksum("ABC", 3)); }
int main(int, char**) { UNITY_BEGIN(); RUN_TEST(test_checksum); return UNITY_END(); }
```
On Arduino targets, put `UNITY_BEGIN()`/`UNITY_END()` in `setup()` after a ~2 s delay so the
serial port is ready.
- `pio test -e native` — runs on the host in seconds; ideal for parsers, state machines, maths.
  This only works if hardware access sits behind an interface you can fake.
- `pio test -e esp32dev` — builds, uploads and reads results over serial from a connected
  board (hardware-in-the-loop). Use `test_port` / `upload_port` when several boards are attached.
- `pio test -e native -f test_parser` filters to one suite; `--without-uploading` exists for
  remote setups.
Keep logic in `lib/` or `src/` modules without `Arduino.h` so the native env compiles it.

## 4. GitHub Actions
```yaml
name: firmware
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix: { env: [esp32dev, nucleo_f401re] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: |
            ~/.cache/pip
            ~/.platformio/.cache
          key: pio-${{ runner.os }}-${{ hashFiles('platformio.ini') }}
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install --upgrade platformio
      - run: pio test -e native
      - run: pio run -e ${{ matrix.env }}
      - uses: actions/upload-artifact@v4
        with:
          name: fw-${{ matrix.env }}
          path: .pio/build/${{ matrix.env }}/firmware.*
```
- Keying the cache on `platformio.ini` means a pin change refetches toolchains; caching all of
  `~/.platformio` (packages and platforms too) is faster but larger — either works.
- Pin the PlatformIO Core version too (`pip install platformio==<version>`) if you need
  bit-for-bit reproducibility.
- Run native tests once, not per matrix entry, in larger projects.

Related: computing-software.firmware-embedded-development.arduino.non-blocking-sketch-structure.

## Verify
- [ ] `pio run` builds every env in `default_envs` from a clean clone.
- [ ] Every `platform` and `lib_deps` line carries an explicit version.
- [ ] `pio test -e native` runs at least one Unity suite and fails CI when an assertion fails.
- [ ] A second CI run shows a cache hit and is noticeably faster than the first.
- [ ] CI uploads a firmware artifact per environment.

## Checked
2026-11-01. Confirmed in the platformio-docs repo: `pio pkg outdated`, `pio test` options (`--environment`, `--filter`,
`--without-uploading`, `--upload-port`, `--test-port`), `test_framework`, `build_src_filter`, `default_envs`, `extends`,
`@ ^x.y.z` version ranges, the Unity `UNITY_BEGIN`/`delay(2000)` pattern, and the cache paths and `pip install
--upgrade platformio` step of the official GitHub Actions page. Removed earlier: `pio pkg update --dry-run` and an
unconfirmed deprecation claim. Platform and library version numbers are illustrative, as the skill says.
Method: documentation only; no commands were run.
