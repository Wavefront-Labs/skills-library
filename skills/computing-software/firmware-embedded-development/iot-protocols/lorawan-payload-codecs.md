---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-payload-codecs
name: lorawan-payload-codecs
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-payload-codecs, lorawan-network-servers, lorawan, payload-codec, decodeuplink, cayenne-lpp, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN payload codecs: Decode compact binary payloads server-side."
sources:
  - https://www.thethingsindustries.com/docs/integrations/payload-formatters/
  - https://www.chirpstack.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN payload codecs

**Goal:** Decode compact binary payloads server-side.

## Steps
1. Pack data with fixed binary layout, e.g. int16 temperature in 0.01 C, uint8 battery
2. ChirpStack v4 codec: function decodeUplink(input) returns { data: {...} } from input.bytes and input.fPort
3. TTN uses the same signature plus encodeDownlink and decodeDownlink
4. Use Cayenne LPP or CBOR for self-describing data
5. Keep a version byte as the first field
6. Share codecs via the LoRaWAN Alliance Payload Codec API repo

## Gotcha
Using floats as text or JSON over LoRaWAN wastes airtime; keep payloads under ~12 bytes at higher SF.

## Verify
- [ ] Unit test the codec with sample bytes
- [ ] Version byte present
- [ ] Decoded fields match scale
