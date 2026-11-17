---
id: computing-software.firmware-embedded-development.platformio.test-port-and-test-speed
name: test-port-and-test-speed
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [test-port, test-speed, on-target-testing, test-testing-command, without-uploading, unity-output-char, pio-test, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Run pio test on real hardware: test_port and test_speed, skipping stages, DTR/RTS and reset options, Unity output via unity_config.h, and test_testing_command for simulators."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/test/test_port.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/test/test_speed.html
  - https://docs.platformio.org/en/latest/core/userguide/cmd_test.html
  - https://docs.platformio.org/en/latest/advanced/unit-testing/frameworks/unity.html
  - https://github.com/ThrowTheSwitch/Unity/blob/master/src/unity_internals.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# test_port and test_speed

On embedded envs `pio test` builds each test, uploads it, then gathers results from the target
(by default over a serial connection).

## Options
```ini
[env:nucleo_l476rg]
platform = ststm32
board = nucleo_l476rg
framework = stm32cube
test_port = /dev/ttyACM0      ; same value forms as monitor_port; auto-detected if omitted
test_speed = 115200           ; baud rate, default 115200
test_filter = test_hw_*
test_ignore = test_native_only
```
`test_port` is the communication interface between the test runner and the target; list ports with
`pio device list`. `pio test` flags: `--test-port`, `--upload-port`, `--without-building`,
`--without-uploading`, `--without-testing`, `--no-reset` (disables the software reset via
DTR/RTS before testing; press reset manually after upload), `--monitor-rts` and `--monitor-dtr`
(initial line state for gathering results over serial, default 1), `-v`. If the board does not
support software reset via DTR/RTS, add a delay of more than 2 seconds before `UNITY_BEGIN()` so
the serial connection can be established.

## Getting Unity output out of the target
PlatformIO's Unity runner defines `UNITY_INCLUDE_CONFIG_H` and looks for a `unity_config.h` in the
test folder, then up the test hierarchy to the test directory root. If none is found it generates
one that routes results to the framework's interface: standard input/output on `native`, the
first available Serial interface on embedded platforms. To route output elsewhere (a HAL UART,
for example) provide your own `unity_config.h` (Unity ships a template) that defines Unity's
output hooks `UNITY_OUTPUT_CHAR(c)`, `UNITY_OUTPUT_START()`, `UNITY_OUTPUT_FLUSH()` and
`UNITY_OUTPUT_COMPLETE()`:
```c
/* test/unity_config.h */
#define UNITY_OUTPUT_CHAR(c)    unity_putc(c)
#define UNITY_OUTPUT_START()    unity_uart_init()
#define UNITY_OUTPUT_FLUSH()    unity_uart_flush()
#define UNITY_OUTPUT_COMPLETE() unity_uart_flush()
void unity_putc(int c); void unity_uart_init(void); void unity_uart_flush(void);
```
and implement the three functions in a `unity_config.c` or `unity_config.cpp` next to it (hardware
specific; PlatformIO publishes an STM32Cube example with a custom `unity_config.h`). Tests in a
shared folder in the hierarchy can all use the same config.

## No serial available
Use `test_testing_command` (a multiline option: first line the program, further lines its
arguments) to run a program that writes test output to standard output, such as a simulator:
SimAVR and Renode are documented examples (see the custom test runner skill), both run with
`pio test --without-uploading`. Another route is a custom runner whose `stage_testing()` collects
results from any source.

## Gotchas
- Results never arrive: wrong baud, or the target's UART not initialised at `test_speed`.
- Boards that need a manual reset: use `--no-reset` and press reset after upload.
- Several boards: pin `upload_port` and `test_port` per env.

## Verify
- [ ] `pio test -e <target>` reports per-test PASS or FAIL from hardware.
- [ ] CI hardware runner uses fixed ports and fails on missing output.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `test_port`, `test_speed`,
`pio test` reference, Unity framework page, and Unity `unity_internals.h` (master). Confirmed:
option semantics and default speed, flags and the 2-second note, `unity_config.h` lookup and
generated default, output hook macro names. Removed as unconfirmed: the HAL UART implementation
sample, the Nucleo ST-LINK VCP and USART2 statement, RTT reader and QEMU semihosting command
lines, Wokwi, the Native USB CDC re-enumeration remark, the `-vv` flag, and the `test_port` "defaults
to the upload port" claim (the docs say it is auto-detected).
Method: documentation only; no commands were run.
