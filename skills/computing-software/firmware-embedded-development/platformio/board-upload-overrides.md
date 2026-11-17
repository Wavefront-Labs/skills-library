---
id: computing-software.firmware-embedded-development.platformio.board-upload-overrides
name: board-upload-overrides
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [board-upload, board-upload-maximum-size, maximum-ram-size, offset-address, flash-size, platformio-ini, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Override board upload fields in platformio.ini: maximum_size and maximum_ram_size for the size check, how the check fails, and linker-script consistency for bootloader slots."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/index.html
  - https://docs.platformio.org/en/latest/platforms/creating_board.html
  - https://github.com/platformio/platformio-core/blob/develop/platformio/builder/tools/pioupload.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# board_upload overrides

Fields under `upload` in the board manifest feed the size check and uploader settings. Override
them per env with `board_upload.<field>`.

## Size limits
```ini
[env:app_with_bootloader]
board = nucleo_l476rg
board_upload.maximum_size = 458752        ; 512 KB minus 64 KB bootloader
board_upload.maximum_ram_size = 98304     ; SRAM1 only, SRAM2 reserved
board_build.ldscript = linker/app_at_0x08010000.ld
```
- After the program is built, PlatformIO prints RAM and Flash usage against `maximum_ram_size` and
  `maximum_size`. If `maximum_size` is 0 or unset the check is skipped.
- Program size above `maximum_size` stops the build with "Error: The program size (N bytes) is
  greater than maximum allowed (M bytes)". Data size above `maximum_ram_size` only prints a
  warning.
- The check compares the built firmware with the numbers you give, it does not read the linker
  script. Keep the numbers equal to what the linker script allows, otherwise the check lies.
- Placing the application after a bootloader is a linker-script and firmware matter: the script
  must put `FLASH` at the application address and the application must set the vector table
  offset. Upload offset handling is platform-specific (see the platform page and its board JSON).

## Inspect
```sh
pio boards nucleo_l476rg --json-output    # manifest defaults, includes the "upload" object
pio run -e app_with_bootloader -t size    # print size information
pio run -e app_with_bootloader -t envdump # dump the build environment
```

## Gotchas
- Reduced `maximum_size` but forgot the linker script: the binary links against full flash and can
  overwrite data or config pages.
- ESP32 partition tables decide app size; set `maximum_size` to match the app partition.

## Verify
- [ ] Size-check limits equal the linker script regions.
- [ ] Uploaded app lands at the intended address (read back or boot via the bootloader).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19) and platformio-core
`pioupload.py` (develop). Confirmed: `board_upload.maximum_size` override example, the size
check skip when `maximum_size` is 0, the exact error text for program overflow and warning-only
behaviour for RAM, `envdump` target (targets page) and `size` target (built-in target list in the build actions page), manifest
`upload.maximum_size` and `maximum_ram_size` fields. Removed as unconfirmed:
`offset_address`, `flash_size`, `speed`, `wait_for_upload_port`, `use_1200bps_touch`,
`require_upload_port`, the `checkprogsize` target name and the "region FLASH overflowed"
message.
Method: documentation only; no commands were run.
