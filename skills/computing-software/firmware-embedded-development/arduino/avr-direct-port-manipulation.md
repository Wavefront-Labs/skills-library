---
id: computing-software.firmware-embedded-development.arduino.avr-direct-port-manipulation
name: avr-direct-port-manipulation
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-registers, direct-port-manipulation, ddrx, portx, pinx, digitalwrite-overhead, atomic-pin-toggle, atmega328p, firmware-embedded-development]
level: practitioner
status: draft
description: "Replace slow digitalWrite/digitalRead on AVR Arduinos with DDRx/PORTx/PINx register access: pin mapping, atomicity, toggling via PINx and keeping code readable."
sources:
  - https://docs.arduino.cc/retired/hacking/software/PortManipulation/
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AVR direct port manipulation

**Goal:** fast, simultaneous pin operations on ATmega328P/2560 boards where `digitalWrite`
(~3-5 us, 50+ cycles with lookup tables and PWM checks) is too slow or not simultaneous.

## Registers per port (B, C, D on the Uno)
| Reg | Function |
|---|---|
| `DDRx` | direction: 1 = output |
| `PORTx` | output value; for inputs, 1 = enable pull-up |
| `PINx` | read input levels; **writing 1 toggles** the PORTx bit |
Uno mapping: D0-D7 = PORTD 0-7, D8-D13 = PORTB 0-5, A0-A5 = PORTC 0-5. Mega differs
completely: use the board's pin mapping table or `digitalPinToPort()`/`digitalPinToBitMask()`.

## Examples
```cpp
DDRB |= _BV(DDB5);            // D13 output
PORTB |= _BV(PORTB5);         // high
PORTB &= ~_BV(PORTB5);        // low
PINB = _BV(PINB5);            // toggle in 1 cycle (single SBI on the I/O register)
bool b = PIND & _BV(PIND2);   // read D2
PORTD = (PORTD & 0x03) | (value << 2);   // write D2..D7 simultaneously, keep D0/D1 (serial)
```

## Atomicity
`PORTB |= _BV(5)` compiles to a single `SBI` instruction (atomic) only when the address is in
the low I/O space and the mask is a constant. Read-modify-write of whole ports (`PORTD = ...`),
or variable masks, are several instructions: an ISR changing another pin on the same port in
between gets its change overwritten. Wrap in `ATOMIC_BLOCK(ATOMIC_RESTORESTATE)` from
`<util/atomic.h>` or `noInterrupts()`/`interrupts()`.

## Keep it maintainable
- Define names: `#define LED_PORT PORTB` / `#define LED_BIT PORTB5`, or use a fast-IO library
  (`digitalWriteFast` resolves constant pins at compile time to the same SBI/CBI).
- Guard AVR-only code with `#if defined(ARDUINO_ARCH_AVR)` and provide a fallback.
- Don't touch PORTD bits 0/1 when using Serial, or PORTB bits used by SPI while SPI runs.

## Verify
- [ ] Logic analyser: pin toggles at the expected rate (e.g. ~2.6 MHz loop with PINx toggles at
      16 MHz vs ~100 kHz with digitalWrite).
- [ ] Serial still works after port-wide writes (D0/D1 preserved).
