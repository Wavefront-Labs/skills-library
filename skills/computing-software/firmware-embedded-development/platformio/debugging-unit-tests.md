---
id: computing-software.firmware-embedded-development.platformio.debugging-unit-tests
name: debugging-unit-tests
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [debug-test, pio-debug-test, debug-a-failing-test, native-gdb, on-target-test-debugging, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Step through a failing PlatformIO unit test: the debug_test option, pio debug on target, GDB commands, and Unity failure breakpoints."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_test.html
  - https://docs.platformio.org/en/latest/plus/debugging.html
  - https://docs.platformio.org/en/latest/core/userguide/cmd_debug.html
  - https://github.com/ThrowTheSwitch/Unity/blob/master/src/unity.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging unit tests

## Point the debugger at a test
```ini
[env:nucleo_f401re]
platform = ststm32
board = nucleo_f401re
framework = stm32cube
test_framework = unity
debug_tool = stlink
debug_test = test_spi_flash       ; name of the test to debug
```
`debug_test` is the name of the unit test to be debugged. If the test's source file sits in the
root of the test directory, set `debug_test = *`. PlatformIO's debugger supports tests created with
PlatformIO's unit testing framework.

## On target
`pio debug -e nucleo_f401re` prepares the project for debugging, loads the firmware according to
`debug_load_mode`, and stops at `debug_init_break` (default `tbreak main`); continue to the
failing `RUN_TEST`. PlatformIO also publishes tutorials for debugging unit tests with ESP32
(Arduino and ESP-IDF), STM32Cube, nRF52 (Arduino and Zephyr) in its documentation.

## GDB from the command line
```sh
pio debug -e nucleo_f401re --interface=gdb -- -x .pioinit
```
A double hyphen skips the parsing of extra GDB options; `.pioinit` is the init file used in the
documented example. `piodebuggdb` is a shortcut for `pio debug --interface=gdb`.

## Tips
- Unity's `TEST_ABORT()` is `longjmp(Unity.AbortFrame, 1)` unless `UNITY_EXCLUDE_SETJMP_H` or
  `UNITY_TEST_ABORT` is defined (then it is a `return` or your own macro). After a failed
  assertion, execution jumps back into the test runner, so set the breakpoint before the failing
  assertion.
- `UnityFail` is called by `TEST_FAIL` and `TEST_FAIL_MESSAGE`; other assertion failures go
  through the static helper `UnityTestResultsFailBegin` in `unity.c`, which can be broken on if it
  was not inlined.
- The default debug flags are `-Og -g2 -ggdb2`; set `debug_build_flags = -O0 -g3` for awkward
  stepping.

## Verify
- [ ] Breakpoint in the code under test hits when running the selected test.
- [ ] A breakpoint on the Unity failure helper stops at a deliberately failing assertion with a
      useful backtrace.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `debug_test`, debugging
and `pio debug` pages, and Unity `unity.c` and `unity_internals.h` (master). Confirmed:
`debug_test` semantics and `*` rule, `--interface=gdb -- -x .pioinit`, default `tbreak main`,
default debug flags, the `TEST_ABORT` definition and `UnityFail` call path. Removed as
unconfirmed: the native-platform debugging section (host gdb, macOS lldb advice), the claim that
`pio debug` builds with `src/main` excluded, the VS Code `launch.json` "PIO Debug" behaviour, and
the original advice to `break UnityFail` for every failure (it only covers `TEST_FAIL`).
Method: documentation only; no commands were run.
