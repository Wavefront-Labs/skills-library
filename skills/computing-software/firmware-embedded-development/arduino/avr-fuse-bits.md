---
id: computing-software.firmware-embedded-development.arduino.avr-fuse-bits
name: avr-fuse-bits
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-registers, avr-fuses, cksel, sut, ckdiv8, bootrst, bootsz, bodlevel, eesave, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Read ATmega328P fuse bytes safely: clock source (CKSEL/SUT/CKDIV8), boot section and reset vector, brown-out level, EESAVE, and which fuses need care."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AVR fuse bits (ATmega328P)

**Goal:** the right clock, boot behaviour and brown-out protection programmed into the chip. Other AVR parts differ: read that part's datasheet.

## Fuses are active-low
In the fuse tables a value of **0 means programmed** and 1 means unprogrammed. Fuse values are latched when the device enters programming mode and on power-up, so a change takes effect after leaving programming mode (EESAVE takes effect as soon as it is programmed). Chip erase does not change fuse bits; fuse bits are locked if lock bit LB1 is programmed, so program fuses before lock bits.

## Low fuse: clock
- `CKSEL3..0`: clock source. Ranges from the datasheet: 1111-1000 low power crystal, 0111-0110 full swing crystal, 0101-0100 low frequency crystal, 0011 internal 128 kHz RC, 0010 calibrated internal RC, 0000 external clock; 0001 is reserved.
- `SUT1..0`: start-up time. The factory value gives the maximum start-up time for the default clock source.
- `CKDIV8` (bit 7) programmed = divide the system clock by 8. Factory state: calibrated internal 8 MHz RC with CKDIV8 programmed, giving 1 MHz.
- `CKOUT` (bit 6) programmed outputs the system clock on PORTB0.

## High fuse
- `BOOTRST` programmed: the reset vector points to the boot loader reset address instead of 0x0000. Factory state is unprogrammed.
- `BOOTSZ1..0`: boot size; factory value (both programmed) gives the maximum boot size.
- `EESAVE` programmed: EEPROM is preserved through chip erase (factory: unprogrammed).
- `SPIEN` is programmed at the factory and is not accessible in serial programming mode.
- `DWEN` enables debugWIRE. `RSTDISBL` is the external reset disable fuse (see the datasheet's alternate functions of Port C). Treat both with care.
- `WDTON` keeps the watchdog always on.

## Extended fuse: brown-out
`BODLEVEL2..0`: `111` brown-out detector disabled; `101` threshold typically 2.7 V (2.5 to 2.9 V); `100` typically 4.3 V (4.0 to 4.6 V); `110`, `011`, `010` and `001` are reserved. Factory state is all unprogrammed (1).

## Verify
- [ ] Each fuse byte matches the design table, read against the datasheet's active-low convention.
- [ ] Clock checked after changing CKSEL (CKOUT on PORTB0 can help with bring-up).

## Checked
2026-11-01. Confirmed against the ATmega328P datasheet (7810D-AVR-01/15): fuse byte tables 27-4 to 27-7 with factory states, latching of fuses, device clocking options table 8-1, BODLEVEL coding table 28-5, CKOUT on PORTB0. Removed: Uno-specific fuse hex values, 0xFF/0xE2 clock values, the Optiboot boot size, recovery procedures (external clock, high-voltage rescue), the avrdude read-back command and the 2.7 V versus 4.3 V frequency advice, none of which that datasheet states. The fusecalc site was not read and was dropped.
Method: documentation only; no commands were run.
