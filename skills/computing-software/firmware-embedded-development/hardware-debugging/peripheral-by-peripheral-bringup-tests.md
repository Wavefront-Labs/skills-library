---
id: computing-software.firmware-embedded-development.hardware-debugging.peripheral-by-peripheral-bringup-tests
name: peripheral-by-peripheral-bringup-tests
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [peripheral-test, board-bringup, bringup-shell, zephyr-shell, uart-console, factory-test, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Bring up a board peripheral by peripheral through a device shell: Zephyr shell command groups, OK/FAIL output, stable test commands and locking it down."
sources:
  - https://interrupt.memfault.com/blog/firmware-shell
  - https://docs.zephyrproject.org/latest/services/shell/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Peripheral-by-peripheral bring-up tests

**Goal:** prove each part of a new board in isolation, interactively, through a small command shell
on the UART, so application bugs are not hardware bugs in disguise. The same commands later serve
factory and automated tests.

## Why a shell
Memfault's article gives three uses: inspecting, validating and overriding state while developing
(bringing up a peripheral or file system without the cloud or phone layers being ready); assembly
line provisioning and testing (stations talk to the unit over UART, which works on Windows, Linux
and macOS and needs no network; commands return pass or fail); and integration tests on real
hardware, where commands return a status such as a factory reset giving OK or FAIL.

Their caution: a shell bypasses the production interface, so keep the end-to-end flows covered by
QA. Reasons not to build one: an unreliable link, a shell grown so large that parsing belongs host
side, a need for multiple connections on one port, or consumers that will use a binary protocol.

## Zephyr shell
- Features: multiple instances, static and dynamic commands, Tab completion, history, help, built-in
  commands (aliases, clear, shell, colors, echo, history, resize), wildcards and getopt.
- Backends: MQTT, Segger RTT, SMP, Telnet, UART, USB, Bluetooth LE (NUS), RPMSG and a dummy one.
- Some features cost RAM and flash; `CONFIG_SHELL_MINIMAL` selects the lean defaults, then enable
  only what you need.
- Ready-made command groups, each needing the driver option plus its shell option:
  `CONFIG_GPIO` + `CONFIG_GPIO_SHELL`, `CONFIG_I2C` + `CONFIG_I2C_SHELL`, `CONFIG_SENSOR` +
  `CONFIG_SENSOR_SHELL`, `CONFIG_FLASH` + `CONFIG_FLASH_SHELL`, `CONFIG_FILE_SYSTEM` +
  `CONFIG_FILE_SYSTEM_SHELL`, `CONFIG_ADC` + `CONFIG_ADC_SHELL`.
- RTT backend: `CONFIG_USE_SEGGER_RTT` and `CONFIG_SHELL_BACKEND_RTT`.
- Custom commands use the `SHELL_STATIC_SUBCMD_SET_CREATE`, `SHELL_SUBCMD_DICT_SET_CREATE` and
  `SHELL_DYNAMIC_CMD_CREATE` macros; see the page for the registration examples.

Use these groups to test each bus or device in turn, simplest first, and add commands of your own for
board specific checks (for example a rail or reset line).

## Output and stability (Memfault)
- Output must suit both a person and a machine: every command ends with `> OK` or `> FAIL,<code>`.
- Use CSV for tabular dumps; use base64 or hexdump for binary buffers.
- Factory and automated tests parse the output, so arguments, behaviour and formatting must not
  change between builds. Cover this with unit tests that assert the exact output, run in CI.
- Production builds should carry only the commands the automated tests need; mark them with a
  "do not change" comment.

## Securing the shell
Before shipping, lock down the port. Options discussed: a password (weak; visible with `strings` on
the firmware unless obfuscated), a knock pattern, a signed unlock phrase checked with the device key,
or not including the shell in production firmware at all (safest, but you lose it for diagnosing
returned units).

## Record
Keep a bring-up log per board serial with pass or fail for each command and any rework.

## Verify
- [ ] Each peripheral on the schematic has a shell command that passes on the board.
- [ ] Commands used by factory tests print only `> OK` or `> FAIL,<code>` and are covered by output tests.
- [ ] The production build either omits the shell or requires an unlock.

## Checked
Confirmed from the Memfault firmware shell article and the Zephyr shell documentation: use cases,
output format, stability and securing advice, Zephyr features, backends and command group options.
Removed as unconfirmed: the bring-up order, per-bus procedures (I2C address scan range, device ID
register values, SPI JEDEC IDs, UART module AT tests, ADC checks), the example command syntax, and
the TI slva704 source (not read).

Method: docs-checked 2026-11-09 against the Memfault firmware shell article and the Zephyr shell documentation page.
