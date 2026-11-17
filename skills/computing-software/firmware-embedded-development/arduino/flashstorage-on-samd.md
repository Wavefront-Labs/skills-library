---
id: computing-software.firmware-embedded-development.arduino.flashstorage-on-samd
name: flashstorage-on-samd
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [flash-storage-samd, flashstorage, samd21-nvm, eeprom-emulation, flash-wear, reflash-erases-data, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Persist settings on SAMD21/SAMD51 boards without EEPROM: FlashStorage and FlashStorage_SAMD, EEPROM emulation, erase-on-upload behaviour, wear limits and validity markers."
sources:
  - https://github.com/cmaglie/FlashStorage
  - https://github.com/khoih-prog/FlashStorage_SAMD
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FlashStorage on SAMD

SAMD21 boards (Zero, MKR, Nano 33 IoT, Seeeduino XIAO) have no EEPROM. Store data in a reserved
row of internal flash.

## FlashStorage (cmaglie)
```cpp
#include <FlashStorage.h>
typedef struct { uint32_t magic; uint16_t version; uint16_t rate; char name[16]; uint32_t crc; } Cfg;
FlashStorage(cfg_store, Cfg);       // reserves an aligned flash area in the sketch image

Cfg cfg;
void setup() {
  cfg = cfg_store.read();
  if (cfg.magic != 0xC0FFEE01 || crc32(&cfg, offsetof(Cfg, crc)) != cfg.crc) {
    cfg = Cfg{0xC0FFEE01, 1, 10, "default", 0};
    cfg.crc = crc32(&cfg, offsetof(Cfg, crc));
    cfg_store.write(cfg);            // erases the row then writes
  }
}
```
`FlashStorage_SAMD` (khoih-prog) is based on it, supports SAMD21 and SAMD51 boards and adds
emulated-EEPROM access including `EEPROM.commit()`.

## Things to know
- **The storage is erased each time a new sketch is uploaded** (both library READMEs say so).
  Settings survive resets and power cycles, not reflashes. Use external EEPROM/FRAM or a fixed address region excluded from upload if they must
  survive firmware updates.
- Endurance: the FlashStorage README warns that typical flash survives only about 10000 write
  cycles to the same block and tells you to keep `write()` calls well below that for the life of
  the product; the chip's datasheet gives the real rating. Write only on change, never in `loop()`
  periodically.
- Brown-out during write corrupts the record: keep a magic + CRC and fall back to defaults, or
  alternate between two FlashStorage instances with a sequence number.
- EEPROM emulation `commit()` writes the whole emulated area to flash; call it rarely, never in a loop.
- Both READMEs advise a real EEPROM where the chip has one.

## Alternatives
- External I2C EEPROM/FRAM (survives reflash, high endurance).

## Checked
2026-11-01. Confirmed against the cmaglie/FlashStorage and khoih-prog/FlashStorage_SAMD READMEs: the
FlashStorage macro with read/write, erase on sketch upload, the 10000-cycle warning, SAMD21/SAMD51
support, EEPROM.commit() writing the whole area. Removed unconfirmed figures (row and block sizes,
per-row endurance ratings, bossac behaviour, NVMCTRL and SmartEEPROM notes) and the datasheet source.
Method: documentation only; no commands were run.

## Verify
- [ ] Settings survive 100 power cycles; corrupted record falls back to defaults.
- [ ] Write count per day estimated against endurance for product life.
