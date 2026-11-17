---
id: computing-software.firmware-embedded-development.arduino.external-i2c-eeprom-and-fram
name: external-i2c-eeprom-and-fram
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [fram, i2c-eeprom, 24lc256, mb85rc256v, page-write, ack-polling, wire-buffer-limit, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Use external I2C EEPROM (24LCxx) and FRAM (MB85RC) from Arduino: addressing, page-write boundaries, write-cycle ACK polling, Wire buffer limits, and when FRAM is worth it."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/24AA256-24LC256-24FC256-Data-Sheet-20001203W.pdf
  - https://www.fujitsu.com/uk/Images/MB85RC256V-DS501-00017-3v0-E.pdf
  - https://docs.arduino.cc/language-reference/en/functions/communication/wire/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# External I2C EEPROM and FRAM

## Parts
| | 24LC256 EEPROM | MB85RC256V FRAM |
|---|---|---|
| Size | 32 KB | 32 KB |
| Address | 0x50-0x57 (A2..A0) | 0x50-0x57 |
| Write time | up to 5 ms per page | none (bus speed) |
| Endurance | 1 000 000 cycles | 10^12 cycles |
| Page | 64 bytes | no pages |
Both use a 16-bit memory address after the device address (small parts like 24C02 use 8-bit).

## EEPROM write with page boundaries and ACK polling
```cpp
#include <Wire.h>
const uint8_t EE = 0x50; const uint8_t PAGE = 64;
void eeWrite(uint16_t addr, const uint8_t *d, size_t n) {
  while (n) {
    size_t chunk = PAGE - (addr % PAGE);            // never cross a page boundary
    if (chunk > n) chunk = n;
    if (chunk > 30) chunk = 30;                      // AVR Wire buffer 32 bytes incl. 2 address bytes
    Wire.beginTransmission(EE);
    Wire.write(addr >> 8); Wire.write(addr & 0xFF); Wire.write(d, chunk);
    Wire.endTransmission();
    do { Wire.beginTransmission(EE); } while (Wire.endTransmission() != 0);   // ACK polling
    addr += chunk; d += chunk; n -= chunk;
  }
}
void eeRead(uint16_t addr, uint8_t *d, size_t n) {
  while (n) { size_t c = n > 32 ? 32 : n;
    Wire.beginTransmission(EE); Wire.write(addr >> 8); Wire.write(addr & 0xFF); Wire.endTransmission(false);
    Wire.requestFrom(EE, (uint8_t)c); for (size_t i = 0; i < c; i++) d[i] = Wire.read();
    addr += c; d += c; n -= c; }
}
```
Crossing a page boundary wraps to the start of the same page and silently overwrites data. Add a
timeout to the ACK polling loop in production.

## FRAM
Same protocol, no page or delay: write any length (still limited by the Wire buffer per
transaction). Ideal for counters, ring-buffer logs, and frequent state saves. Adafruit_FRAM_I2C
library handles details. FRAM reads are destructive internally but auto-restored; endurance
counts reads too on some parts (10^12+).

## Practical notes
- Write-protect (WP) pin: tie to GND for writes or drive from a GPIO to protect against runaway code.
- Pull-ups 4.7 k at 100-400 kHz; FRAM supports 1 MHz Fm+.
- Brown-out during an EEPROM page write can corrupt that page; use record CRCs and two copies.
- Libraries: `SparkFun_External_EEPROM` auto-detects size/page and handles buffer splitting;
  `I2C_eeprom` (Rob Tillaart).

## Verify
- [ ] Write/read test across a page boundary returns identical data.
- [ ] Measured write throughput matches expectation (EEPROM: ~64 bytes per 5 ms).
