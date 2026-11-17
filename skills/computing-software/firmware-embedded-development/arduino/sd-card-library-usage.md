---
id: computing-software.firmware-embedded-development.arduino.sd-card-library-usage
name: sd-card-library-usage
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-sd, sdfat, sd-card-logging, spi-sd, fat32, card-detect, flush, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Log to SD cards from Arduino reliably: SD vs SdFat, wiring and level shifting, CS and SPI speed, flush/sync for power loss, file naming, and diagnosing begin() failures."
sources:
  - https://docs.arduino.cc/libraries/sd/
  - https://github.com/greiman/SdFat
  - https://www.sdcard.org/downloads/formatter/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD library usage

## Library choice
- **SD** (bundled): simple, FAT16/FAT32, 8.3 filenames, ~600 bytes RAM buffer.
- **SdFat** (Greiman): faster, long filenames, exFAT (cards > 32 GB), better error codes, pre-
  allocation (`preAllocate`) for low-latency logging. SD is a wrapper around an old SdFat.
- ESP32 core: `SD` (SPI) and `SD_MMC` (4-bit SDMMC, much faster).

## Wiring
- SD cards are 3.3 V only. On 5 V boards use a module with a level shifter (74LVC125/HC4050) and
  regulator, not a bare breakout.
- SPI: MOSI, MISO, SCK, CS. On Uno hardware SPI is 11/12/13; pin 10 must stay OUTPUT even if CS is
  elsewhere (or SPI drops into slave mode).
- Other SPI devices on the bus must have their CS high before `SD.begin()`; a floating CS on another
  device corrupts transfers.

## Basic logging
```cpp
#include <SD.h>
File logf;
void setup() {
  pinMode(10, OUTPUT);
  if (!SD.begin(4)) { Serial.println(F("SD init failed")); while (1) {} }
  logf = SD.open("LOG.CSV", FILE_WRITE);         // appends
}
void loop() {
  logf.print(millis()); logf.print(','); logf.println(analogRead(A0));
  static uint32_t last; if (millis() - last > 5000) { logf.flush(); last = millis(); }
}
```
Data is only safe on the card after `flush()` or `close()`. Each flush writes the directory entry
and FAT; flushing every line is slow and wears the card. Flush on a time interval, and on a
power-fail signal if available.

## Diagnosing `begin()` failure
- Card formatted wrong: use the SD Association formatter (FAT32 for <= 32 GB). exFAT needs SdFat.
- CS pin wrong, or other device on SPI not deselected.
- SPI too fast for wiring: SdFat `SdSpiConfig(cs, SHARED_SPI, SD_SCK_MHZ(4))`.
- Insufficient supply current: cards draw 100-200 mA write bursts; 3.3 V regulators on Uno's 3V3 pin
  (50-150 mA) are marginal. Add a bulk capacitor (10-100 uF) at the card.
- SdFat `sd.initErrorHalt(&Serial)` prints the error code.

## Gotchas
- Long write latencies (up to 100-250 ms) happen when the card erases internally; buffer samples in
  RAM or use SdFat's pre-allocated contiguous files with `writeSector`.
- Removing the card while open corrupts the FAT; use a card-detect pin and close files first.
- Too many open files exhaust RAM on AVR (each File has a 512-byte cache shared or not by library).

## Verify
- [ ] 24 h logging test with random power cuts leaves a readable file losing at most one flush
  interval.
- [ ] Worst-case write latency measured and covered by buffering.
