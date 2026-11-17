---
id: computing-software.firmware-embedded-development.iot-protocols.cbor-encoding
name: cbor-encoding
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [cbor-encoding, iot-payloads, cbor, rfc8949, major-type, cddl, iot-protocols]
level: practitioner
status: docs-checked
description: "CBOR encoding: Use CBOR as compact binary JSON."
sources:
  - https://www.rfc-editor.org/rfc/rfc8949
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CBOR encoding

**Goal:** Use CBOR as compact binary JSON.

## Steps
1. The initial byte holds a 3-bit major type (high-order bits) and 5-bit additional information: 0 unsigned int, 1 negative int (value is -1 minus the argument), 2 byte string, 3 text string (UTF-8), 4 array, 5 map, 6 tag, 7 simple/float
2. Additional information below 24 is the argument itself; 24, 25, 26 and 27 mean the argument follows in 1, 2, 4 or 8 bytes in network byte order; 28 to 30 are reserved; 31 means indefinite length
3. `{"t":22.5}` encodes as A1 61 74 FB 40 36 80 00 00 00 00 00 (map of 1, text "t", double 22.5); the same value can also use a half or single float (major type 7, additional information 25 or 26)
4. Arrays, maps, byte strings and text strings can use indefinite length: start with additional information 31 (for an array 0x9F) and end with the "break" stop code 0xFF
5. Describe schemas with CDDL, the Concise Data Definition Language of RFC 8610 (listed in RFC 8949's references)

## Gotcha
Maps with text keys cost bytes on every message; use small integer keys agreed in a schema table when airtime matters, as SenML does.

## Verify
- [ ] Round trip equals source
- [ ] Size less than JSON
- [ ] Output validates against the CDDL schema

## Checked

2026-11-03. Confirmed in RFC 8949: major types table, additional information rules for 24 to 27, 28 to 30 and 31, indefinite-length encoding and the break stop code (0xFF, as 0b111_11111), RFC 8610 reference. The worked encoding of {"t":22.5} was verified by hand against these rules. Removed: the library list (TinyCBOR, QCBOR, cbor2), which the RFC does not cover.
Method: documentation only; no commands were run.
