---
id: computing-software.firmware-embedded-development.arduino.littlefs-on-esp-and-rp2040
name: littlefs-on-esp-and-rp2040
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-littlefs, littlefs, esp32-littlefs, rp2040-flash-filesystem, data-folder-upload, partition-scheme, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Use LittleFS in Arduino on ESP32, ESP8266 and RP2040: partition/filesystem size, uploading a data folder, mount and format, power-loss behaviour, and migrating off SPIFFS."
sources:
  - https://github.com/espressif/arduino-esp32/tree/master/libraries/LittleFS
  - https://arduino-pico.readthedocs.io/en/latest/fs.html
  - https://arduino-esp8266.readthedocs.io/en/latest/filesystem.html
  - https://github.com/littlefs-project/littlefs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LittleFS on ESP and RP2040

LittleFS is a power-loss-safe, wear-levelling filesystem for NOR flash. It replaced SPIFFS
(deprecated, no directories, slow) in the ESP8266, ESP32 and RP2040 Arduino cores.

## Size the filesystem
- **ESP32:** Tools > Partition Scheme (or `-b esp32:esp32:esp32:PartitionScheme=default`), or a
  custom `partitions.csv` in the sketch folder with a `spiffs` subtype partition (LittleFS uses the
  same subtype, label `spiffs` by default).
- **ESP8266:** Tools > Flash Size, e.g. "4MB (FS:2MB OTA:~1019KB)".
- **RP2040 (Earle core):** Tools > Flash Size, e.g. "2MB (Sketch: 1MB, FS: 1MB)".

## Use
```cpp
#include <LittleFS.h>
void setup() {
  if (!LittleFS.begin(true)) { Serial.println("mount failed"); return; }  // ESP32: true = format on fail
  File f = LittleFS.open("/cfg.json", "w"); f.print("{\"rate\":10}"); f.close();
  f = LittleFS.open("/cfg.json", "r"); String s = f.readString(); f.close();
  Serial.printf("used %u / %u\n", LittleFS.usedBytes(), LittleFS.totalBytes());
}
```
ESP8266/RP2040 `begin()` takes no format argument; call `LittleFS.format()` explicitly. ESP8266
uses `LittleFS.info(fsinfo)` for sizes.

## Uploading a `data/` folder
- IDE 2.x: community plugins (`arduino-littlefs-upload` for ESP32/ESP8266/RP2040), command palette
  "Upload LittleFS to ...". The IDE 1.x "ESP32 Sketch Data Upload" tools are not supported in 2.x.
- CLI: build an image with `mklittlefs -c data -p 256 -b 4096 -s <size> fs.bin` (block/page sizes per
  core) and flash it at the partition offset with `esptool.py write_flash <offset> fs.bin`; RP2040
  `picotool load fs.bin -o <fs start>`.
- PlatformIO: `board_build.filesystem = littlefs` and `pio run -t uploadfs`.

## Behaviour to know
- Writes are copy-on-write; a power cut during write leaves the old file intact, never a corrupted
  filesystem. Close files to commit.
- Small files waste a full block (4 KB) each; many tiny files fill the FS quickly.
- Uploading a new sketch does not erase the filesystem; changing partition layout does.
- Opening files in ISRs or from multiple tasks without care is unsafe on ESP32 (VFS locking is per
  file).

## Migrating from SPIFFS
SPIFFS images are not readable by LittleFS. Ship firmware that reads the old SPIFFS data once,
writes it to LittleFS (needs both partitions or a temporary copy in RAM), then formats.

## Verify
- [ ] Power-cut test during writes always remounts cleanly.
- [ ] `totalBytes()` matches the chosen partition scheme.
