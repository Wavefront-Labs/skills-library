---
id: computing-software.firmware-embedded-development.arduino.arduino-cli-debug
name: arduino-cli-debug
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-cli-debug, debug-optimize, gdb, openocd, debug-info, ide-2-debugger, arduino-cli, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug Arduino sketches on SAMD, RP2040, ESP32 and Portenta with arduino-cli debug: --optimize-for-debug builds, probe selection, debug -I info, GDB and IDE 2 integration."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/debug/debug.go
  - https://github.com/arduino/arduino-cli/blob/master/docs/UPGRADING.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# arduino-cli debug

Supported only where the platform defines the `debug.*` properties (see "Platform side");
`debug.executable` must be present and non-empty, otherwise debugging is not allowed. `arduino-cli debug check`
reports whether a board and programmer combination supports debugging.

## Build for debugging
```sh
arduino-cli compile -b arduino:samd:arduino_zero_edbg --optimize-for-debug \
  --output-dir build sketch/
```
`--optimize-for-debug` makes `compiler.optimization_flags` use the platform's
`compiler.optimization_flags.debug` value instead of `compiler.optimization_flags.release`.

## Start a session
```sh
arduino-cli debug -b arduino:samd:arduino_zero_edbg -p /dev/ttyACM0 --input-dir build sketch/
arduino-cli debug -b arduino:samd:mkr1000 -P atmel_ice sketch/   # -P selects the programmer/probe
arduino-cli debug -I -b <fqbn> --format json   # show metadata about the debug session instead of starting it
```
The command opens an interactive gdb session using the platform's `debug.*` settings
(`--interpreter mi` selects a machine interface for other front ends). Use the `-I` output to configure
other front ends with the same debug server configuration.

## IDE 2.x
The IDE uses the same platform configuration: select the board, enable Sketch > Optimize for Debugging,
pick the programmer, then use the Debug button. The IDE generates a `launch.json` for the cortex-debug
plugin; platform keys `debug.cortex-debug.custom.*` are converted to JSON and added to it as is.

## Platform side (for custom cores)
`platform.txt`/`boards.txt` keys: `debug.executable`, `debug.toolchain=gcc`,
`debug.toolchain.path`, `debug.toolchain.prefix`, `debug.server=openocd`, `debug.server.openocd.path`,
`debug.server.openocd.scripts_dir`, `debug.server.openocd.scripts.N` (or a single
`debug.server.openocd.script`), `debug.svd_file`, `debug.cortex-debug.custom.*`, and
`debug.additional_config` (use another configuration subtree to override `debug.*`).

## Gotchas
- If debugging is reported as unsupported, the platform lacks the `debug.*` keys (in particular
  `debug.executable`) or the chosen programmer has none; run `arduino-cli debug check`.

## Verify
- [ ] `arduino-cli debug -I` returns a complete config for the board/probe pair.
- [ ] Breakpoint in `loop()` hits and variables display in a `--optimize-for-debug` build.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs and source on master (commit 2026-10-22).

Confirmed: `debug` flags `--input-dir`, `--interpreter` (console, mi, mi1, mi2, mi3), `-I/--info`, `--debug-property`, programmer via `-P`, and the `debug check` subcommand; platform keys `debug.executable` (debugging not allowed when absent or empty), `debug.toolchain` (gcc), `debug.toolchain.path`, `debug.toolchain.prefix`, `debug.server` (openocd only), `debug.svd_file`, `debug.server.openocd.path`, `scripts_dir`, `scripts.N`, `script`, `debug.cortex-debug.custom.*` (JSON added to the IDE's launch.json), `debug.additional_config`; `compiler.optimization_flags.debug` and `.release` selected by `--optimize-for-debug` or the IDE's Sketch > Optimize for Debugging. Removed claims no document covers: the supported-board list, `-Og -g3`, the ESP32 JTAG remarks, the `debug_custom.json` file and the breakpoint tip.

Method: documentation only; no commands were run.
