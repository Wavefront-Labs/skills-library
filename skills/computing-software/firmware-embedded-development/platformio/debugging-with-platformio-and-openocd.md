---
id: computing-software.firmware-embedded-development.platformio.debugging-with-platformio-and-openocd
name: debugging-with-platformio-and-openocd
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [platformio, pio-debug, debug-tool, openocd, debug-init-break, debug-server, launch-json, vscode-debug, svd-file, peripheral-view, debug-extra-cmds, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Set up PlatformIO's integrated debugger: debug_tool, debug_init_break, debug_svd_path, custom servers, and when to drop to a hand-run OpenOCD and GDB session."
sources:
  - https://docs.platformio.org/en/latest/plus/debugging.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_tool.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_init_break.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_svd_path.html
  - https://docs.platformio.org/en/latest/plus/debug-tools/custom.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with PlatformIO and OpenOCD

**Goal:** get `pio debug` (or the VS Code PlatformIO debug button) working reliably, and know when
to drop to a hand-run OpenOCD and GDB session. It builds on the probe fundamentals in
`computing-software.firmware-embedded-development.hardware-debugging.jtag-swd-probe-setup-and-troubleshooting`,
which apply underneath PlatformIO's wrapping either way.

## How `pio debug` is structured
Boards are pre-configured with a debug server compatible with their on-board debugging tool
(adapter or probe), and PlatformIO dynamically configures the back-end debugger (GDB) for the
debug environment. For many boards and tools the server is OpenOCD, started with arguments
generated from the board manifest (see `board-manifest-debug-configuration`). When something
goes wrong the error is therefore usually in the server layer (wrong target config, probe not
attaching) even though it surfaces in the IDE: the troubleshooting steps from the JTAG/SWD skill
apply unchanged. `pio debug -v` shows detailed information while processing.

## `debug_init_break` and where execution stops
`debug_init_break` defaults to `tbreak main`: a temporary breakpoint at `main`, deleted after the
first stop. An empty value (`debug_init_break =`) disables the initial breakpoint. Each probe has
a limited number of hardware breakpoints; put additional initial breakpoints in
`debug_extra_cmds`. An empty `debug_init_break` alone does not guarantee an attach without a
reset: the default init commands also reset and halt, so for attach-only sessions review
`debug_init_cmds` and `debug_load_mode = manual`.

## `debug_tool = custom` for non-default probes and configs
`debug_tool` selects among the tools a board supports; `custom` is for your own configuration
(see the Custom debug tool page). It is paired with an explicit `debug_server` (first line is the
executable, following lines are its arguments), usually `debug_port`, and often your own
`debug_init_cmds`. For a custom board, see
`computing-software.firmware-embedded-development.platformio.custom-board-definitions-and-partition-tables`.
Use verbose output to see what PlatformIO runs for the closest preset and adapt it rather than
guessing OpenOCD argument syntax.

## SVD files for peripheral register views
`debug_svd_path` is a path to an SVD file with information about the device peripherals, which the
IDE debug view uses to show decoded registers. Use the vendor SVD for the exact part number: a
generic family-level file can mislabel bitfields that differ between sub-variants.

## When to drop to a hand-run session
The documented `pio debug --interface=gdb -- <gdb options>` starts GDB with the project's
configuration, and a hand-run OpenOCD with the same configuration files isolates whether an issue
is in the probe and target connection or in PlatformIO's integration, a useful triage before
reporting a PlatformIO bug.

## Verify
- [ ] `debug_tool` and `debug_server` match the actual probe and target.
- [ ] `debug_init_break` is set deliberately for the session's goal.
- [ ] The SVD file matches the exact MCU part number, spot-checked against the reference manual.
- [ ] A debugging issue was reproduced (or ruled out) with a hand-run OpenOCD and GDB session
      before blaming PlatformIO.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): debugging overview,
`debug_tool`, `debug_init_break`, `debug_svd_path`, `debug_server` and Custom tool pages, and the
platform-ststm32 `platform.py` for the OpenOCD server arguments. Confirmed: dynamic GDB
configuration and pre-configured servers, `tbreak main` default and empty-value behaviour,
hardware breakpoint note, `debug_server` format, `debug_svd_path` purpose. Removed as unconfirmed:
the `.pioinit`/`extra-linux.gdbinit` generation claim, "generated config lives in
`.pio/build/<env>`", the claim that an empty init break attaches without reset, and the VS Code
button behaviour.
Method: documentation only; no commands were run.
