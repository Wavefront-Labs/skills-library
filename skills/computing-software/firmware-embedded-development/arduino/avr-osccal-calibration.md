---
id: computing-software.firmware-embedded-development.arduino.avr-osccal-calibration
name: avr-osccal-calibration
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [osccal, internal-rc-oscillator, 8mhz-internal, clock-calibration, uart-baud-error, timer2-32khz-reference, avr, arduino, firmware-embedded-development]
level: advanced
status: draft
description: "Calibrate the AVR internal RC oscillator via OSCCAL: factory accuracy, measuring against a 32 kHz crystal or UART, storing per-chip values in EEPROM, and safe step limits."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://ww1.microchip.com/downloads/en/Appnotes/Atmel-2555-Internal-RC-Oscillator-Calibration-for-tinyAVR-and-megaAVR-Devices_ApplicationNote_AVR053.pdf
  - https://github.com/MCUdude/MiniCore
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oscillator calibration (OSCCAL)

Running an ATmega328P/ATtiny on its internal 8 MHz RC oscillator (no crystal) saves parts and
power, but the 328P datasheet specifies factory calibration at only +/-10% (8 MHz, 3 V, 25 C), and
user calibration can reach +/-1%. UART needs < ~2%.

## Register
`OSCCAL` (8-bit). Higher value = higher frequency; on the 328P the range is split into two
overlapping halves (0-127 and 128-255), so stepping across 127/128 jumps frequency. Factory value
is loaded at reset for the operating voltage it was calibrated at.

Rules from AVR053:
- Change in small steps (datasheet: do not change by more than ~2% per step when the CPU runs from
  it) and let it settle.
- Do not calibrate above the rated frequency (e.g. tuning to 8.8 MHz then running EEPROM/flash
  writes may fail; datasheet says keep below 8.8 MHz for EEPROM/flash write).

## Measuring against a reference
**32.768 kHz crystal on Timer2 (asynchronous, TOSC pins):** count CPU cycles (Timer1 at clk/1)
during N Timer2 overflows, compare to expected (8 MHz x N x 256 / 32768), adjust OSCCAL by binary
search or stepping, repeat until within target. AVR053 provides this algorithm.

**UART reference:** host sends a known byte stream (e.g. 0x55 at known baud); measure bit time with
Timer1 input capture on RX, adjust until bit time matches. Used by some bootloaders (TinySafeBoot
style autobaud).

**Jig reference:** production tester outputs a 1 kHz square wave; firmware counts cycles per period
and stores the best OSCCAL.

## Storing the value
Calibrate once per chip at production (or first boot with a reference), save to EEPROM, and write
it to `OSCCAL` at the very beginning of `setup()`/`main()`:
```c
uint8_t cal = eeprom_read_byte((uint8_t*)E2END);   // last EEPROM byte
if (cal != 0xFF) OSCCAL = cal;
```
MiniCore/ATTinyCore offer bootloader/sketch options that load OSCCAL from EEPROM.

## Temperature and voltage
The RC drifts with voltage and temperature. Battery devices running from 3.6 V down to 2.4 V may
need calibration at mid-range or periodic recalibration against a 32 kHz crystal.

## Verify
- [ ] Measured CPU clock (CKOUT fuse or toggling pin) within +/-1% after calibration.
- [ ] UART at the target baud error-free across the device's voltage range.
