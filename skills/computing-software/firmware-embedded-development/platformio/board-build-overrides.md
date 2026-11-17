---
id: computing-software.firmware-embedded-development.platformio.board-build-overrides
name: board-build-overrides
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [board-build, board-build-mcu, board-build-f-cpu, board-build-ldscript, board-build-filesystem, board-build-embed-files, platformio-ini, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Override board manifest build fields from platformio.ini: board_build.f_cpu, mcu, ldscript, flash_mode, partitions, filesystem and embed files, and verifying effective values."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/index.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/board_build.f_cpu.html
  - https://docs.platformio.org/en/latest/platforms/espressif32.html
  - https://docs.platformio.org/en/latest/scripting/examples/override_board_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# board_build overrides

Any option declared in a board's JSON manifest can be overridden per environment with
`board_{OBJECT.PATH}`, for example `board_build.f_cpu` for `build.f_cpu`, without writing a custom
board.

## Common overrides
```ini
[env:bluepill]
platform = ststm32
board = bluepill_f103c8
board_build.mcu = stm32f103cbt6          ; 128 KB variant
board_upload.maximum_size = 131072       ; keep size check in sync
board_build.f_cpu = 72000000L
board_build.ldscript = linker/STM32F103CB_FLASH.ld

[env:esp32]
platform = espressif32
board = esp32dev
board_build.f_cpu = 160000000L
board_build.f_flash = 80000000L
board_build.flash_mode = qio
board_build.partitions = partitions_custom.csv
board_build.filesystem = littlefs
board_build.embed_txtfiles = src/certs/ca.pem
```
- `f_cpu` is a C-like long integer with an `L` suffix (16 MHz is `16000000L`). It does not change the
  real clock settings on the hardware: set it to match a clock you already changed.
- `board_build.mcu` is the MCU type the compiler uses to recognise the architecture; valid values
  depend on the platform (see the Boards table of the platform page).
- `ldscript` is a path to a linker script used instead of the framework's, for example when the
  application needs a special memory section for a bootloader.
- `board_build.partitions` (ESP32) selects a partition CSV. Defaults are `default.csv` for Arduino
  and `partitions_singleapp.csv` for ESP-IDF. A SPIFFS partition must have Type `data` and SubType
  `spiffs`.
- `board_build.filesystem` (ESP32) accepts `spiffs` (default), `littlefs` and `fatfs`; the image is
  uploaded with the `uploadfs` target (`buildfs` builds it).
- `embed_files` and `embed_txtfiles` (ESP32) embed files into flash `.rodata`; the `embed_txtfiles`
  ones are null-terminated. Symbol names are built from the file path, for example
  `_binary_src_certs_ca_pem_start` for `src/certs/ca.pem`. With ESP-IDF the symbol names must not
  contain the path (`_binary_ca_pem_start`) and the files are also listed in `CMakeLists.txt`.

## Inspect the effective values
```sh
pio project config --json-output          # parsed platformio.ini
pio run -e esp32 -t envdump               # dump the current build environment
pio boards esp32dev --json-output         # manifest defaults
```
An extra script can change a manifest value with `env.BoardConfig().update("build.hwids", [...])`
(a pre script). Such changes do not apply to `pio device monitor`.

## When to make a custom board instead
More than a few overrides, different debug or upload configuration, or the same hardware used in
many projects: create `boards/<id>.json` in the project (see custom board definitions).

## Gotchas
- Changing `board_build.mcu` without the matching `board_upload.maximum_size` and
  `maximum_ram_size` makes size checks wrong.
- Overrides only work for options the platform's build scripts read; check with `envdump` that
  yours has an effect.

## Verify
- [ ] `envdump` shows the overridden values.
- [ ] Map file confirms memory layout matches the real chip.

## Checked
2026-10-26 against platformio-docs (develop branch, last commit 2026-09-19) and platformio-core
source. Confirmed: the `board_{OBJECT.PATH}` override rule and the f_cpu, mcu, ldscript,
f_flash, flash_mode examples; ESP32 partitions defaults, filesystem values, embed options and
symbol naming; `BoardConfig().update` and the monitor limitation; `envdump` target;
`--json-output` on `pio boards` and `pio project config`. Removed as unconfirmed:
`board_build.arduino.memory_type`, "ldscript paths are relative to the project dir", the
`BoardConfig().get` usage, the full-erase advice for partition offsets and the STM32 clock-tree
remark.
Method: documentation only; no commands were run.
