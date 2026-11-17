---
id: computing-software.firmware-embedded-development.arduino.eeprom-wear-and-persistent-storage
name: eeprom-wear-and-persistent-storage
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino, eeprom, eeprom-write, eeprom-update, wear-leveling, flash-endurance, 100000-cycles, avr, atmega328p, esp32-preferences, nvs, littlefs, spiffs, crc, checksum, power-loss, brownout, non-volatile-storage, firmware-embedded-development]
level: practitioner
status: draft
description: "Persist settings on Arduino without wearing out EEPROM/flash: EEPROM.update() over write(), wear-leveling across addresses, CRC-checked records, and the ESP32 NVS/Preferences alternative."
sources:
  - https://docs.arduino.cc/learn/built-in-libraries/eeprom
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EEPROM wear and persistent storage on Arduino

**Goal:** store settings that survive power loss, without wearing out the storage
in weeks because you wrote to the same address every loop.

## The core mistake
`EEPROM.write(addr, val)` on AVR costs ~3.3ms and, more importantly, the underlying
cell is rated for roughly 100,000 erase/write cycles. Write once a second to the
same address and you hit that limit in about 28 hours. `EEPROM.update(addr, val)`
reads first and only writes if the value changed — always prefer it. If you must
write unconditionally (e.g. a counter), you need wear leveling, not `update()`.

## Wear leveling by hand (AVR EEPROM)
For a value that changes often (a counter, a running total), rotate across a block
of addresses instead of one cell:
1. Reserve N addresses (e.g. 32 bytes) for one logical value.
2. Keep a small "current slot" pointer, itself wear-leveled by storing it as a
   sequence number you can find by scanning for the highest valid CRC, not by
   writing the pointer location every time.
3. Write new value + a 1-byte sequence counter + a CRC8 to the next slot; on boot,
   scan all slots and take the one with the highest sequence number whose CRC
   matches. This divides wear by N and tolerates a power loss mid-write (the
   previous valid slot is still intact).
4. A simpler approximation for low-frequency saves (once per hour or on a specific
   event, not every loop) often doesn't need this at all — just use `update()` and
   accept ~100k writes as years of headroom. Don't build wear leveling you don't need.

## Power-loss safety
A write interrupted by brownout/power loss leaves a corrupt record. Always store a
CRC (or at minimum a magic byte + length) alongside the data and validate on read;
never trust EEPROM contents by default on boot. Fall back to a documented default
struct if validation fails, and log/flag that a reset-to-default happened.

## Platform differences
- **AVR (Uno/Nano)**: true byte-addressable EEPROM, `<EEPROM.h>`, blocking writes.
- **ESP32/ESP8266**: there is no real EEPROM; `EEPROM.h` there emulates it inside a
  flash page cached in RAM — you must call `EEPROM.commit()` or nothing is
  persisted, and every `commit()` erases and rewrites the whole page (worse
  endurance per logical byte than AVR). For anything beyond a couple of scalars on
  ESP32, use `Preferences` (NVS, wear-leveled key/value store) or LittleFS instead —
  both already handle wear leveling and partial-write safety for you.
- **RP2040/SAMD**: no EEPROM; typically emulated in flash similarly — check the
  core's docs before assuming AVR-style semantics.

## Verify
- [ ] Confirmed which platform: real EEPROM (AVR) vs flash-emulated (ESP32/8266) vs none.
- [ ] Any value written more than ~daily uses `update()` or explicit wear leveling, not raw `write()`.
- [ ] Every persisted record has a CRC/magic byte checked on load, with a safe default on mismatch.
- [ ] On ESP32, `EEPROM.commit()` is called after every write batch, or `Preferences`/NVS is used instead.
- [ ] Pulled power mid-write in a bench test; boot still produces a valid (even if default) config.
