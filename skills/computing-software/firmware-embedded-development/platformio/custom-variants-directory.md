---
id: computing-software.firmware-embedded-development.platformio.custom-variants-directory
name: custom-variants-directory
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [variants-dir, board-build-variant, pins-arduino-h, variant-cpp, custom-pinout, arduino-variant, platformio, firmware-embedded-development]
level: advanced
status: draft
description: "Give a PlatformIO Arduino project a custom pin mapping: board_build.variants_dir and variant, pins_arduino.h/variant.cpp contents per core, and keeping it with the project."
sources:
  - https://docs.platformio.org/en/latest/platforms/creating_board.html
  - https://github.com/stm32duino/Arduino_Core_STM32/wiki/Add-a-new-variant-(board)
  - https://github.com/espressif/arduino-esp32/tree/master/variants
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom variants directory

Arduino cores map pin numbers (`D2`, `A0`, `LED_BUILTIN`, `SDA`) to MCU pins in a **variant**
folder. Custom hardware needs its own variant; PlatformIO lets you keep it in the project.

## Config
```ini
[env:acme]
platform = espressif32
board = esp32-s3-devkitc-1          ; or your custom board JSON
framework = arduino
board_build.variants_dir = variants  ; folder in the project
board_build.variant = acme_s3        ; subfolder name
```
```
project/
  variants/acme_s3/pins_arduino.h
  src/main.cpp
```
`board_build.variant` overrides the `build.variant` field from the board manifest; a custom board
JSON can also set `"variant": "acme_s3"` while the ini sets only `variants_dir`.

## What goes in a variant
- **ESP32:** `pins_arduino.h` with `static const uint8_t TX = 43; RX = 44; SDA = 8; SCL = 9;
  SS/MOSI/MISO/SCK; LED_BUILTIN; A0..; T0..` and `USB_VID/PID` for native USB boards. Copy the
  closest variant from the core's `variants/` folder and edit.
- **STM32duino:** `variant_<NAME>.h` + `variant_<NAME>.cpp` (digital pin array `digitalPin[]`,
  `analogInputPin[]`), `PeripheralPins.c` (pin to peripheral/AF map, generated from CubeMX data),
  `boards_entry.txt`, and the `ldscript.ld`; plus `SystemClock_Config()` for your crystal.
- **AVR:** `pins_arduino.h` with the `PROGMEM` port/bit/timer tables.
- **SAMD:** `variant.h` + `variant.cpp` with `g_APinDescription[]` and SERCOM instances.

## Practical advice
- Start from the reference board you derived the hardware from and change only what differs.
- Keep pin names in the schematic and the variant identical (net labels -> macro names).
- Define board-specific peripherals (`Serial1` pins, `Wire1`) in the variant so libraries work
  unchanged.
- Check: `pio run -v` should show `-I.../variants/acme_s3`; a missing folder falls back silently to
  the board's default variant on some platforms, so verify a macro value at runtime.

## Gotchas
- Core upgrades change variant structure (STM32duino 2.x reorganised folders); pin the platform and
  framework version (`platform_packages`) for products.
- Two definitions of the same macro (variant and your code) cause silent overrides; keep pin
  constants only in the variant.

## Verify
- [ ] `LED_BUILTIN`, `SDA/SCL` and `Serial` pins print the expected GPIO numbers at boot.
- [ ] Every connector pin exercised with a loopback or scope.
