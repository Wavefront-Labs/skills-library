---
id: computing-software.firmware-embedded-development.stm32.open-drain-and-pull-configuration
name: open-drain-and-pull-configuration
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, open-drain, gpio-pull-up, push-pull, wired-or, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Choose STM32 GPIO output type and pulls correctly: push-pull vs open-drain, internal pull strength limits, I2C and wired-OR buses, level shifting and safe reset states."
sources:
  - https://www.st.com/resource/en/application_note/an4899-stm32-microcontroller-gpio-hardware-settings-and-lowpower-consumption-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open-drain and pull configuration

## Registers
- `OTYPER`: 0 push-pull, 1 open-drain.
- `PUPDR`: 00 none, 01 pull-up, 10 pull-down.
- HAL: `GPIO_MODE_OUTPUT_PP` / `GPIO_MODE_OUTPUT_OD`, `GPIO_MODE_AF_PP` / `GPIO_MODE_AF_OD`,
  `.Pull = GPIO_NOPULL / GPIO_PULLUP / GPIO_PULLDOWN`.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## When open-drain
- I2C SDA/SCL (`GPIO_MODE_AF_OD`), SMBus, 1-Wire.
- Shared interrupt or reset lines (wired-OR/AND): several devices pull low, one resistor pulls high.
- Driving a signal into a higher-voltage domain on a five-volt-tolerant (FT) pin with an external
  pull-up to 5 V (pin must be FT, not TT/analog, and internal pull-up must be off).
- Bidirectional bit-banging without changing pin direction: write 1 to release, read IDR.

## Internal pulls are weak
Internal pull-ups are roughly 30-50 kohm. For I2C at 100/400 kHz you need external 2.2-4.7 kohm;
internal pulls give slow edges and NACKs above a few kHz. Fine for buttons and keeping inputs
defined.

## Push-pull everywhere else
Faster edges, no resistor current. A push-pull output tied to another driver (bus conflict)
can burn the pin; use open-drain or series resistors when two drivers may overlap.

## Reset and boot states
After reset, pins are inputs (analog mode on L4/G4/U5 to save power, floating input on F1/F4),
except debug pins. External devices see a floating line until init: add pull resistors to
enable/reset lines that must be in a defined state at power-up (e.g. MOSFET gate pulldown).

## Low power
Floating inputs leak; unused pins to analog mode. A pull-up on a pin held low externally burns
3.3 V / 40 k = ~80 uA.

## Verify
- [ ] I2C rise time measured (< 300 ns for 400 kHz) with chosen resistors.
- [ ] Power-up waveform on enable lines shows a defined level before firmware init.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
