---
id: computing-software.firmware-embedded-development.arduino.versioned-config-records
name: versioned-config-records
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [config-versioning, settings-migration, struct-versioning, magic-number, crc-record, eeprom-layout, arduino, firmware-embedded-development]
level: practitioner
status: draft
description: "Store settings so firmware updates do not misread them: magic, version and length header, CRC, defaulting new fields, migration functions, and double-buffered writes."
sources:
  - https://docs.arduino.cc/learn/built-in-libraries/eeprom/
  - https://www.nongnu.org/avr-libc/user-manual/group__util__crc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Versioned config records

Adding a field to a settings struct shifts every byte after it. Old firmware data read with the new
layout produces garbage settings, which on a device in the field can mean a bricked radio config.

## Record layout
```cpp
struct CfgHeader { uint16_t magic; uint8_t version; uint8_t len; };   // len = payload size
struct CfgV2 {                       // append-only: never reorder or remove fields
  uint16_t rate_s;                   // v1
  uint8_t  mode;                     // v1
  int16_t  temp_offset_c10;          // v2
};
struct CfgRecord { CfgHeader h; CfgV2 p; uint16_t crc; };
const uint16_t CFG_MAGIC = 0xA55A; const uint8_t CFG_VER = 2;
```

## Load with migration
```cpp
#include <EEPROM.h>
#include <util/crc16.h>
uint16_t crc16(const uint8_t *d, size_t n){ uint16_t c=0xFFFF; while(n--) c=_crc16_ccitt_update(c,*d++); return c; }

bool loadCfg(CfgV2 &out) {
  CfgV2 def = {60, 0, 0}; out = def;
  CfgHeader h; EEPROM.get(0, h);
  if (h.magic != CFG_MAGIC || h.len > sizeof(CfgV2)) return false;          // blank or foreign
  uint8_t buf[sizeof(CfgV2)]; for (uint8_t i = 0; i < h.len; i++) buf[i] = EEPROM.read(sizeof h + i);
  uint16_t crc; EEPROM.get(sizeof h + h.len, crc);
  uint8_t tmp[sizeof h + sizeof(CfgV2)]; memcpy(tmp, &h, sizeof h); memcpy(tmp + sizeof h, buf, h.len);
  if (crc != crc16(tmp, sizeof h + h.len)) return false;                   // corrupt
  memcpy(&out, buf, h.len);          // older, shorter payload: new fields keep defaults
  if (h.version < 2) { /* migrate semantics if a v1 field changed meaning */ }
  return true;
}
```
Save always writes the current version with `len = sizeof(CfgV2)` and a CRC over header+payload,
using `EEPROM.put` (which only writes changed bytes on AVR).

## Rules
- **Append-only** fields; deprecated fields stay as reserved bytes.
- Use fixed-width types (`uint16_t`, not `int`, which is 2 bytes on AVR and 4 on ARM/ESP) and
  `__attribute__((packed))` or explicit padding if records are shared between architectures.
- Semantic changes (units, meaning) bump the version and need a migration step, not just a
  default.
- **Double buffer** for power-loss safety: two slots with a sequence counter; write the older slot,
  then on load pick the valid one with the highest sequence.
- Downgrades: newer data read by older firmware has `len` larger than it knows; read only its
  own length and ignore the rest, or refuse and use defaults.

## Verify
- [ ] Data written by version N loads correctly in N+1 with new fields defaulted.
- [ ] Corrupting one byte falls back to the other slot or defaults.
