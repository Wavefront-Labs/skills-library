---
id: computing-software.firmware-embedded-development.zephyr.board-flash-and-debug-runners
name: board-flash-and-debug-runners
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [board-porting, board-runners, board-cmake, board-runner-args, jlink-runner, openocd-runner, pyocd-runner, west-debug, runners-yaml, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Wire a Zephyr board to flash and debug tools in board.cmake (J-Link, OpenOCD, pyOCD, STM32CubeProgrammer, nrfutil), set runner args and pick a runner per invocation."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://docs.zephyrproject.org/latest/develop/flash_debug/host-tools.html
  - https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html
  - https://docs.zephyrproject.org/latest/build/sysbuild/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board flash and debug runners

**Goal:** `west flash`, `west debug` and `west attach` work for everyone on the team with the
probes they actually have.

## board.cmake
```cmake
board_runner_args(jlink "--device=nRF52840_xxAA" "--speed=4000")
board_runner_args(pyocd "--target=nrf52840" "--frequency=4000000")
include(${ZEPHYR_BASE}/boards/common/nrfutil.board.cmake)   # first include = default runner
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
include(${ZEPHYR_BASE}/boards/common/pyocd.board.cmake)
```
The order of the `include()` calls matters: the **first** include sets the default flash runner
if none is set. A runner that cannot debug is skipped for debugging, so the default debug runner
is the first included one that supports it (the porting guide's example: `nrfjprog` first makes
`jlink` the default debug runner). Runner option names such as `--speed` belong to the runner's
Python script, not to the wrapped tool. `west flash --context` lists runners that support
flashing, and `west flash --context -r <RUNNER>` shows one runner's options (likewise for
`west debug`).

## Choosing at the command line
```
west flash --runner jlink
west flash -r stm32cubeprogrammer
west debug -r jlink                      # GDB server + gdb with the ELF
west debugserver                         # just the server, attach from an IDE
west flash --erase                       # only runners that support it: mass-erase before flashing
west --verbose flash                     # print the host tool commands the runner uses
```
Some runners take a probe selector (for example `--dev-id` on the NXP S32 debug probe runner);
check the runner's options with `west flash --context -r <RUNNER>`. Each build system contains a
`runners.yaml`; with sysbuild these are packaged into `domains.yaml`.

## Gotchas
- The host tools a runner wraps must be installed and found; `west --verbose flash` shows the
  exact command.
- Multi-image (sysbuild) builds flash every image; `west flash --domain <name>` flashes one.
- Some runners flash `.hex`, some `.bin` with an offset: the board's flash partition and
  `CONFIG_FLASH_LOAD_OFFSET` must agree or the image lands in the wrong place.

## Verify
- [ ] `west flash` with each declared runner programs and resets the board.
- [ ] `west debug` stops at `main` with source-level stepping.

## Checked

Checked 2026-10-25 against the Zephyr documentation source (main, post-4.4; latest release v4.4.2): doc/hardware/porting/board_porting.rst, doc/develop/west/build-flash-debug.rst, doc/develop/flash_debug/host-tools.rst, doc/build/sysbuild/index.rst and the boards/common/*.board.cmake file list.
Confirmed: `board.cmake`, `board_runner_args(jlink "--device=..." "--speed=...")` and the pyocd args, the `boards/common/<runner>.board.cmake` include files (nrfutil, nrfjprog, jlink, pyocd, stm32cubeprogrammer), first-include default runner and default debug runner rule, `west flash --runner/-r`, `--erase`, `--domain`, `west debug`, `west debugserver`, `west --verbose flash`, `--context`, `runners.yaml`/`domains.yaml`, the STM32CubeProgrammer runner being the default for STM32 boards.

Method: documentation only; no commands were run.
