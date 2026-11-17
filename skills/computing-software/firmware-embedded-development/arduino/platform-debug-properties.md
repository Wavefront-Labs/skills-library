---
id: computing-software.firmware-embedded-development.arduino.platform-debug-properties
name: platform-debug-properties
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [platform-debug, debug-properties, platform-txt-debug, openocd-scripts, svd-file, programmers-txt, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Add debugger support to an Arduino core: debug.* keys in platform.txt/boards.txt/programmers.txt, OpenOCD script lists, SVD files, optimisation flags, and testing with debug -I."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/UPGRADING.md
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/debug/debug.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform debug properties

The IDE 2 Debug button and `arduino-cli debug` are generic; the core tells them how to debug via
`debug.*` properties.

## Keys
```properties
# platform.txt
debug.executable={build.path}/{build.project_name}.elf
debug.toolchain=gcc
debug.toolchain.path={runtime.tools.<toolchain name>.path}/bin
debug.toolchain.prefix=arm-none-eabi
debug.server=openocd
debug.server.openocd.path={runtime.tools.<openocd name>.path}/bin/
debug.server.openocd.scripts_dir={runtime.tools.<openocd name>.path}/share/openocd/scripts/
debug.server.openocd.script={runtime.platform.path}/variants/{build.variant}/{build.openocdscript}
debug.svd_file=<absolute path to the SVD file>

# optimisation used with --optimize-for-debug / IDE "Optimize for Debugging"
compiler.optimization_flags=-Os
compiler.optimization_flags.release=-Os
compiler.optimization_flags.debug=<debug flags>
```
Then use `{compiler.optimization_flags}` in the compile recipes instead of hard-coded `-Os`.

## Per board / per programmer
- `boards.txt`: `myboard.debug.server.openocd.script=...`, `myboard.debug.svd_file=...`. Board values
  override platform values.
- `programmers.txt`: `cmsisdap.debug.server.openocd.scripts.0=interface/cmsis-dap.cfg` so the
  selected programmer chooses the interface script (programmer values override board and platform values).
- Extra Cortex-Debug fields: `debug.cortex-debug.custom.<key>=<value>` (e.g.
  `debug.cortex-debug.custom.overrideRestartCommands.0=monitor reset halt`), and
  `debug.additional_config` for advanced cases.

## Testing
```sh
arduino-cli debug -I -b acme:samd:sense -P cmsisdap --format json
```
Check `executable`, `toolchain_path`, `server_configuration.scripts` and `svd_file` resolve to real
files. Then run a session: `arduino-cli debug -b acme:samd:sense -P cmsisdap sketch/`.

## Gotchas
- A missing or empty `debug.executable` means debugging is not allowed.
- `{runtime.tools.<name>.path}` only resolves if the tool is in the platform's `toolsDependencies`
  (or installed); add OpenOCD as a dependency in the package index.

## Verify
- [ ] `debug -I` output complete for each board/programmer combination.
- [ ] IDE 2 Debug hits a breakpoint on a sample sketch.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs and source on master (commit 2026-10-22).

Confirmed: `debug.*` directive list and the requirement that `debug.executable` is non-empty; overlay order (platform.txt, boards.txt overrides platform, programmers.txt overrides both when the programmer is selected); `debug.cortex-debug.custom.*`; `debug.additional_config`; `compiler.optimization_flags.debug` and `.release` selected by `--optimize-for-debug`; `debug -I --format json` fields `executable`, `toolchain_path`, `server_configuration.scripts`, `svd_file`. Removed claims no document covers: concrete debug flags (`-Og -g3`), the `{programmer.protocol}` script path, the OpenOCD backslash remark and the board-specific script and SVD names.

Method: documentation only; no commands were run.
