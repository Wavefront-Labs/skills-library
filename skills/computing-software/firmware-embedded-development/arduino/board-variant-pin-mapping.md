---
id: computing-software.firmware-embedded-development.arduino.board-variant-pin-mapping
name: board-variant-pin-mapping
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-core, pins-arduino-h, variant, digital-pin-to-port, led-builtin, num-digital-pins, custom-board-variant, boards-local-txt, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Create an Arduino board variant for a custom PCB: pins_arduino.h/variant.cpp pin tables, LED_BUILTIN and peripheral pin defines, and packaging it as a boards.txt entry."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/ArduinoCore-avr/blob/master/variants/standard/pins_arduino.h
  - https://github.com/arduino/ArduinoCore-samd/blob/master/variants/arduino_zero/variant.cpp
  - https://github.com/espressif/arduino-esp32/blob/master/variants/esp32/pins_arduino.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board variant pin mapping

**Goal:** a custom board where `digitalWrite(5, HIGH)`, `Serial1`, `Wire` and `LED_BUILTIN`
map to the pins actually routed on your PCB.

## Where pin mapping lives
`variants/<name>/` in the core, selected by `<board>.build.variant=<name>` in `boards.txt`.
- **AVR:** `pins_arduino.h` with PROGMEM tables `digital_pin_to_port_PGM`,
  `digital_pin_to_bit_mask_PGM`, `digital_pin_to_timer_PGM`, `port_to_mode_PGM`, plus macros
  `NUM_DIGITAL_PINS`, `NUM_ANALOG_INPUTS`, `analogInputToDigitalPin`,
  `digitalPinToInterrupt`, `PIN_SPI_SS/MOSI/MISO/SCK`, `PIN_WIRE_SDA/SCL`, `LED_BUILTIN`.
- **SAMD (Arduino core):** `variant.cpp` with the `g_APinDescription[]` array and `variant.h` for the
  defines (`LED_BUILTIN`, SERCOM pads for the serial ports).
- **ESP32:** `variants/<board>/pins_arduino.h` with `static const uint8_t` pin numbers (GPIO numbers are
  used directly).

## Steps
1. Copy the variant of a board with the same MCU.
2. Re-number the tables to follow your silkscreen labels (Arduino pin N = whatever the PCB
   calls D<N>), keeping analog pins contiguous after digital.
3. Update peripheral defaults (`Serial` pins, SPI/I2C pins, `LED_BUILTIN`).
4. Add a `boards.txt` entry (copy the original, change `name`, `build.variant`,
   `build.board`, upload settings). For local experiments use `boards.local.txt` beside
   `boards.txt`, or ship your own **platform** (hardware folder or Boards Manager package index)
   referencing the base core (`build.core=arduino:arduino` style references let you reuse the core;
   `build.variant=arduino:standard` references another platform's variant).

## Gotchas
- Keep the timer and interrupt tables (`digital_pin_to_timer_PGM`, `digitalPinToInterrupt`) consistent
  with the pins your PCB actually routes.
- Libraries that use hard-coded pins (`#ifdef ARDUINO_AVR_UNO`) ignore your variant: define a
  unique `build.board` (becomes `ARDUINO_<VALUE>`) and patch or configure libraries.

## Verify
- [ ] A test sketch toggles every Arduino pin number in sequence; logic analyser confirms the
      physical pin order.
- [ ] Serial, SPI, Wire and analogRead examples work on the defined default pins.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 platform specification (commit 2026-10-22); ArduinoCore-avr variants/standard/pins_arduino.h (commit 2026-07-01); ArduinoCore-samd arduino_zero variant (commit 2026-09-10); arduino-esp32 variants/esp32 (commit 2026-10-20).

Confirmed: `variants/<name>/` selected by `build.variant` (variant references `VENDOR:VARIANT_ID`); AVR `pins_arduino.h` defines `NUM_DIGITAL_PINS`, `NUM_ANALOG_INPUTS`, `analogInputToDigitalPin`, `digitalPinToInterrupt`, `PIN_SPI_SS`, `PIN_WIRE_SDA`, `LED_BUILTIN` and the PROGMEM tables `port_to_mode_PGM`, `port_to_output_PGM`, `digital_pin_to_port_PGM`, `digital_pin_to_bit_mask_PGM`, `digital_pin_to_timer_PGM`; SAMD `variant.cpp` has the `g_APinDescription[]` array and `variant.h` defines `LED_BUILTIN` and the SERCOM pads; the ESP32 variant `pins_arduino.h` uses `static const uint8_t` GPIO numbers; `build.board` becomes `ARDUINO_<value>`; `boards.local.txt` and platform references (`build.core=arduino:arduino`). Removed unconfirmed claims: the STM32duino bullet and wiki source, the `PinDescription` field list, the PWM and interrupt table consequences, and the `boards.local.txt` update remark.

Method: documentation only; no commands were run.
