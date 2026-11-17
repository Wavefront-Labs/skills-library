---
id: computing-software.firmware-embedded-development.platformio.debug-load-mode-and-init-commands
name: debug-load-mode-and-init-commands
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [debug-load-mode, debug-init-break, debug-init-cmds, debug-extra-cmds, debug-server, debug-load-cmds, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Tune PlatformIO debug sessions: debug_load_mode (always/modified/manual), debug_load_cmds, debug_init_break, init and extra commands, and a custom debug_server."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_load_mode.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_init_cmds.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_load_cmds.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_server.html
  - https://docs.platformio.org/en/latest/plus/debug-tools/custom.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# debug_load_mode and init commands

## debug_load_mode
- `always` (default): load firmware for each debugging session.
- `modified`: load only when the firmware was modified.
- `manual`: do not load automatically; you must pre-flash the target with the debugging firmware.

`pio debug --load-mode <mode>` overrides the option for one run.

## Commands
```ini
[env:app]
debug_tool = jlink
debug_load_mode = modified
debug_init_break = tbreak loop            ; default is "tbreak main"; empty value = no initial break
debug_load_cmds =
    monitor flash erase_sector 0 0 11     ; server-side monitor command before loading
    load
debug_extra_cmds =
    break main.cpp:13
    source .gdbinit
```
- `debug_load_cmds` (default `load`): `load [address]` loads at an address; `preload` loads with
  the platform's upload method (for devices with locked flash that the debug client cannot
  program, such as some Freescale Kinetis and NXP LPC boards); an empty value
  (`debug_load_cmds =`) disables loading; any other debugger command can be listed.
- `debug_init_break` accepts any GDB breakpoint spec (`tbreak loop`, `break main.cpp:13`,
  `tbreak Reset_Handler`). Debug adapters have a limited number of hardware breakpoints: put
  further initial breakpoints in `debug_extra_cmds`.
- `debug_init_cmds` replaces the whole default init sequence. The documented GDB form uses the
  placeholders `$DEBUG_PORT`, `$INIT_BREAK` and `$LOAD_CMDS`:
  ```ini
  debug_init_cmds =
      target extended-remote $DEBUG_PORT
      $INIT_BREAK
      monitor reset halt
      $LOAD_CMDS
      monitor init
      monitor reset halt
  ```
  Defaults per tool are in `platformio/debug/config` in platformio-core; copy the default and
  change it rather than writing from scratch.
- `debug_extra_cmds` are passed to the debugger after `debug_init_cmds`: the safe place for your
  own settings. To save session breakpoints use `save breakpoints .gdbinit` in the Debug Console
  and load them with `source .gdbinit`.

## Custom debug server
`debug_server` is multiline: the first line is the server executable, the next lines are its
arguments. Use it with `debug_tool = custom`:
```ini
[env:debug_openocd]
debug_tool = custom
debug_server =
    ${platformio.packages_dir}/tool-openocd/openocd
    -f
    ${platformio.packages_dir}/tool-openocd/scripts/board/stm32f103zet6_warship.cfg
```
`debug_port` is the port of the remote target (serial device or network address such as
`localhost:3333`; detected automatically if omitted). The documented J-Link example sets
`debug_tool = custom`, `debug_port = :2331`, a `debug_server` that starts `JLinkGDBServerCL`, and
its own `debug_init_cmds`.

## Verify
- [ ] Second debug start without code changes skips flashing (`modified` mode).
- [ ] Attach-only config (`manual`) connects without loading firmware.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): the debug option pages,
`pio debug` reference and the custom debug tool page. Confirmed: load mode values and default,
`--load-mode`, `debug_load_cmds` forms and `preload` meaning, `debug_init_break` default and
examples, `debug_init_cmds` placeholders, `debug_extra_cmds` and the save-breakpoints note,
`debug_server` format, `debug_port` examples. Removed as unconfirmed: the J-Link SWO monitor
command, the bootloader-plus-app `add-symbol-file` recipe, the two-ELF load example and the claim
that `debug_port` alone can replace `debug_server`.
Method: documentation only; no commands were run.
