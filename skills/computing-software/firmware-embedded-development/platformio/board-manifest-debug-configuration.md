---
id: computing-software.firmware-embedded-development.platformio.board-manifest-debug-configuration
name: board-manifest-debug-configuration
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [board-debug-config, board-json-debug, openocd-target, jlink-device, svd-path, onboard-tools, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make a custom PlatformIO board debuggable: the board JSON debug section (default_tools, onboard_tools, openocd_target, jlink_device, svd_path), and checking with pio debug."
sources:
  - https://docs.platformio.org/en/latest/platforms/creating_board.html
  - https://github.com/platformio/platform-ststm32/blob/develop/platform.py
  - https://github.com/platformio/platform-ststm32/blob/develop/boards/nucleo_l476rg.json
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_speed.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug configuration in board manifests

When you create `boards/<id>.json` for custom hardware, `pio debug` only works if the `debug`
section tells the platform how to start a debug server. The fields below are the ones the
`ststm32` platform reads; other platforms read their own set, so check that platform's
`platform.py` and an existing board JSON.

## Example (STM32)
```json
{
  "build": { "core": "stm32", "cpu": "cortex-m4", "mcu": "stm32l476rgt6",
             "f_cpu": "80000000L", "product_line": "STM32L476xx" },
  "debug": {
    "default_tools": ["stlink"],
    "onboard_tools": ["stlink"],
    "jlink_device": "STM32L476RG",
    "openocd_target": "stm32l4x",
    "svd_path": "STM32L476.svd"
  },
  "frameworks": ["arduino", "cmsis", "stm32cube", "zephyr"],
  "name": "Acme L476 Sensor",
  "upload": { "maximum_ram_size": 98304, "maximum_size": 1048576,
              "protocol": "stlink", "protocols": ["stlink", "jlink", "cmsis-dap", "blackmagic"] },
  "url": "https://acme.example/l476",
  "vendor": "Acme"
}
```

## Fields (as read by platform-ststm32)
- Tools are generated only for links listed in `upload.protocols` among `blackmagic`, `jlink`,
  `stlink` and `cmsis-dap`.
- `openocd_target` - name of the OpenOCD `target/<name>.cfg`; the generated command uses
  `interface/<link>.cfg`, `transport select swd` and that target file.
- `openocd_board` - if present it wins: the server loads `board/<name>.cfg` instead, and
  `openocd_target` and `openocd_extra_args` are not used.
- `openocd_extra_args` - list of extra OpenOCD arguments appended in the target-based case.
- `jlink_device` - J-Link device name, required for the `jlink` tool (the platform asserts it).
- `default_tools` and `onboard_tools` - mark which tools are the default and which are on the
  board itself.
- `svd_path` - SVD file for the peripheral view. In `platformio.ini` use `debug_svd_path` (a file
  path) to set your own.

## Overriding without editing the board
`platformio.ini`: `debug_tool = cmsis-dap`, `debug_server = ...` (custom command),
`debug_svd_path`, `debug_speed = 4000` (kHz; `auto` and `adaptive` are J-Link only). Useful when
the board JSON comes from a platform you do not control.

## Check
```sh
pio debug -e myenv -v                      # verbose, shows the server command line
pio debug -e myenv --interface=gdb -- -x .pioinit
```

## Gotchas
- A wrong `openocd_target` family gives flash driver errors even when attach seems fine.
- Clone chips with a different IDCODE may need `openocd_extra_args` or a custom target script.
- A missing SVD file leaves the peripheral view empty but debugging still works.

## Verify
- [ ] `pio debug` attaches and flashes with the default tool and with each listed protocol.
- [ ] Peripheral registers appear in the IDE debug view.

## Checked
2026-10-26 against platform-ststm32 `platform.py` and `boards/nucleo_l476rg.json` (develop
branch) and platformio-docs (develop, last commit 2026-09-19). Confirmed: the debug field names
and their effect on the generated OpenOCD and J-Link server commands, `openocd_board`
precedence, the `jlink_device` requirement, `debug_speed` values, `debug_svd_path`,
`pio debug --interface=gdb -- <args>`. Removed as unconfirmed: `pyocd_target`,
`openocd_extra_pre_target_args`, the "svd resolved from misc/svd" rule, the CPUTAPID example and
the `monitor targets` command.
Method: documentation only; no commands were run.
