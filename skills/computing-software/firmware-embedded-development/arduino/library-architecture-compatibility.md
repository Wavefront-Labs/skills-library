---
id: computing-software.firmware-embedded-development.arduino.library-architecture-compatibility
name: library-architecture-compatibility
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-library, library-architectures, architectures-field, arduino-arch-avr, portable-library, architecture-specific-code, precomputed-library, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Make an Arduino library work across AVR, SAMD, ESP32, RP2040 and Renesas cores: the architectures field, ARDUINO_ARCH_* guards, and portable Wire/SPI/timer usage."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/library-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/sketch-build-process.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library architecture compatibility

**Goal:** a library that compiles and behaves the same on every core it claims, and is hidden
or warned about on cores it doesn't support.

## The `architectures` field
```
architectures=avr,samd
```
The default `*` claims all. Names are the architecture folder names of the platforms. A warning is shown when
the library is compiled for a board whose architecture is not on the list, and the field is one factor in
resolving which library matches an `#include`. Claim only what CI actually builds.

## Architecture guards
The build defines `ARDUINO_ARCH_XXX` (XXX is the architecture folder name of the board's platform,
for example `ARDUINO_ARCH_AVR`) and a board macro `ARDUINO_<BOARD>` (from `build.board`):
```cpp
#if defined(ARDUINO_ARCH_AVR)
  // AVR-specific code
#elif defined(ARDUINO_ARCH_SAM)
  // SAM-specific code
#else
  #error "This library only supports boards with an AVR or SAM processor."
#endif
```
An `#error` gives a clear message instead of a hard-to-read compile failure. Isolate such code in one
small port file; keep the rest portable.

## Portability traps
| Trap | Portable approach |
|---|---|
| `int` is 16-bit on AVR, 32-bit elsewhere | use `int16_t`/`uint32_t` |
| direct port registers (`PORTB`) | `digitalWrite` or per-arch port file |
| SPI settings | always wrap in `SPI.beginTransaction(SPISettings(...))` / `endTransaction()` |
| hardware timers (`TCCR1A`, `TimerOne`) | per-arch backend or use `millis()`/`micros()` |
| `attachInterrupt(pin, ...)` pin numbering | use `digitalPinToInterrupt(pin)` |

## Precompiled libraries
`precompiled=true` (or `full`) with `src/{build.mcu}/libfoo.a` (for example `src/cortex-m4/`) ships binaries per
CPU; `dot_a_linkage=true` links the library's objects as an archive. See the `precompiled-arduino-libraries` skill.

## Verify
- [ ] `arduino/compile-sketches` matrix covers every listed architecture.
- [ ] Examples run on at least one real board per architecture before release.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs on master (commit 2026-10-22).

Confirmed: `architectures` defaults to `*`, is a comma-separated list, takes part in library resolution and triggers a warning when compiling for a board whose architecture is not listed; `ARDUINO_ARCH_XXX` comes from the architecture folder name; the compile recipes pass `-DARDUINO_{build.board}`; `precompiled` and `dot_a_linkage` fields with `src/{build.mcu}` layout. Removed unconfirmed claims: the Library Manager filtering remark, the example architecture list and every row of the portability table that no document covers (Wire buffer size, analogWrite details, PROGMEM and F() behaviour, ESP32 IRAM_ATTR, native USB serial).

Method: documentation only; no commands were run.
