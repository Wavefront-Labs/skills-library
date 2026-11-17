---
id: computing-software.firmware-embedded-development.arduino.avr-isr-macro-and-vectors
name: avr-isr-macro-and-vectors
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-isr, isr-macro, interrupt-vectors, isr-nonblock, isr-naked, isr-alias, atomic-block, badisr-vect, avr, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write AVR interrupt handlers with avr-libc: ISR() vector names, ISR_BLOCK/NOBLOCK/NAKED/ALIASOF, BADISR_vect, atomic access to shared data, and Arduino-core vector conflicts."
sources:
  - https://www.nongnu.org/avr-libc/user-manual/group__avr__interrupts.html
  - https://www.nongnu.org/avr-libc/user-manual/group__util__atomic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AVR ISR macro and vectors

## Basics
```cpp
#include <avr/interrupt.h>
ISR(TIMER1_COMPA_vect) { PORTB ^= _BV(PB5); }
```
Vector names come from the device header: `INT0_vect`, `PCINT0_vect`,
`TIMER1_COMPA_vect`, `TIMER0_OVF_vect`, `USART_RX_vect`, `ADC_vect`, `WDT_vect`, `TWI_vect`.
With a vector name that does not exist the handler is never installed, so when that interrupt is
enabled the default action is to **reset the device**. Check names against the device header.

## Attributes
- `ISR(x)` = `ISR_BLOCK`: global interrupts are disabled by the AVR hardware on entry.
- `ISR(x, ISR_NOBLOCK)`: re-enables interrupts at entry, allowing nesting. Use sparingly; the same
  interrupt can re-enter if its flag is set again.
- `ISR(x, ISR_NAKED)`: no prologue/epilogue; you must save registers and end with `reti()`. For
  tiny handlers or crash capture.
- `ISR(x, ISR_ALIASOF(y_vect))`: share a handler between vectors (e.g. PCINT groups).
- `EMPTY_INTERRUPT(x_vect)`: just `reti`; declares a vector that needs no code so it does not reach
  `BADISR_vect` (e.g. `EMPTY_INTERRUPT(ADC_vect);`).
- `ISR(BADISR_vect)`: catch-all for enabled interrupts with no handler, instead of the default reset.

## Shared data
```cpp
#include <util/atomic.h>
volatile uint32_t ticks;                 // written in ISR
uint32_t getTicks() { uint32_t t; ATOMIC_BLOCK(ATOMIC_RESTORESTATE) { t = ticks; } return t; }
```
Multi-byte reads are not atomic on an 8-bit CPU; without the block you can read a torn value when
the ISR updates between byte reads.

## Keep handlers short
Set flags in the ISR and do the work in the main loop.

## Arduino core conflicts
The Arduino core and its libraries define some vectors themselves; defining the same vector again
gives a duplicate-definition link error. Check the core and library sources before reusing a vector.

## Verify
- [ ] Build has no vector-name warnings.
- [ ] Shared multi-byte variables accessed only in atomic blocks outside ISRs.

## Checked
2026-11-01. Confirmed on the avr-libc interrupts page: ISR attributes ISR_BLOCK, ISR_NOBLOCK, ISR_NAKED, ISR_ALIASOF, EMPTY_INTERRUPT, BADISR_vect and the default reset action; and on the util/atomic page: ATOMIC_BLOCK(ATOMIC_RESTORESTATE). Removed: compiler warning text and flag, cycle-count overhead, 16-bit TEMP register note, per-library vector list, and the ATmega328P datasheet source (text not readable).
Method: documentation only; no commands were run.
